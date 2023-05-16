import sys
import time
import sqlite3
from xml.etree import ElementTree as ET
import re

from wikitextparser import remove_markup, parse

PARTS_OF_SPEECH = {
    "nom",
    "nom commun",
    "adjectif",
    "verbe",
    "pronom",
    "adverbe",
    "préposition",
    "conjonction",
    "interjection",
}

"""
wget https://dumps.wikimedia.org/frwiktionary/latest/frwiktionary-latest-pages-articles.xml.bz2
"""

def pprint(title,e):
    print(title,"***DEBUT*****",e,"******FIN*******")
    return e

def replace_template(raw_template):
    
    name=raw_template.name

    if name in ("lien","siècle2","petites capitales","smcp","pc","nobr"):
        return parse(raw_template.arguments[0].value).plain_text(replace_templates=replace_template)

    if name in ('er','re','e'):
        return name

    if name=="lexique":
        return "("+", ".join(x.value for x in raw_template.arguments[:-1])+")"

    if name=="variante ortho de":
        return "Variante orthographique de "+raw_template.arguments[0].value
        
    if name=="unité":
        qty,unit = raw_template.arguments
        
        unit=parse(unit.value).plain_text(replace_templates=replace_template)
        
        qty=parse(qty.value).plain_text(replace_templates=replace_template)
  
        return qty+" "+unit
    if name=="w":
        return parse(raw_template.arguments[-1].value).plain_text(replace_templates=replace_template)
        
        
    if name=="exemple":
        return ""
    if name=="fchim":
        return ''.join([x.value for x in raw_template.arguments])
        
    return ""

def cleanwikicode(wikicode):
    parsed=parse(wikicode)
    templates= {x.name for x in parsed.templates}
    if "variant de" in templates or "variante de" in templates:
        return ""
    return parsed.plain_text(
 replace_templates=replace_template)


bad_prefixes={
    "*",
    "+",
    ",",
    " ",
    ".",
    ";",
    "—",
    "/",
    ":",
    "?",
    "#",
    "…",
    "&",
    "'",
    "!",
    "\""}

def clean_prefix(definition:str):
    for i,character in enumerate(definition):
        if character in bad_prefixes:
            continue
        return definition[i:]
    return ""
    


def main():
    connection = sqlite3.connect("database_fr2.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS dictionary
                             (
                                 id INTEGER PRIMARY KEY,
                                 word TEXT,
                                 lexical_category TEXT,
                                 definition TEXT
                             );""")
    cursor.execute("DELETE from dictionary")
    #cursor.execute("BEGIN TRANSACTION")
    start_time = time.time()
    doc = ET.iterparse(sys.argv[1])
    index = 0
    words = 0
    count = 0

    for event, elem in doc:

        if "page" in elem.tag:
            title = elem.find(
                ".//{http://www.mediawiki.org/xml/export-0.10/}title"
            ).text


            if title.startswith("Wiktionnaire:") or title.startswith("Modèle:") or title.startswith("Conjugaison:") or title.startswith("Catégorie:") or title.startswith("Aide:"):
                continue

            content = (
                elem.find(".//{http://www.mediawiki.org/xml/export-0.10/}revision")
                .find(".//{http://www.mediawiki.org/xml/export-0.10/}text")
                .text
            )

            try:
                for section in parse(content).sections:
                    templates = section.templates
                    if templates:
                        # Get argument 1 which is part of speech and check for value
                        template_arguments = templates[0].arguments
                        part_of_speech = template_arguments[0].value
                        if part_of_speech.lower() in ("nom de famille",):
                            continue
                        
                        # Skip sections not french since some translations are also present
                        if (
                            len(template_arguments) > 1
                            and template_arguments[1].value != "fr"
                        ):
                            continue
                    #    print(template_arguments)
                        if len(template_arguments) > 2 and template_arguments[2].value=="flexion":
                            continue
                        # Validate parts of speech. There is also nom proper so just check if nom is there
                        if any(
                            part in PARTS_OF_SPEECH
                            for part in part_of_speech.lower().split()
                        ):
                
                     #       print(title)
                 #           print(section.lists()[0].items+[x.items for x in section.lists()[0].get_lists("#")])
             #               print([y for x in section.lists()[0].get_lists("#") for y in x.items])
                            meanings = [
                                clean_prefix(cleanwikicode((re.sub("<ref[^>]*?>.*?</ref>",'',item))).strip().replace('()',''))
                                for item in section.lists()[0].items+[y for x in section.lists()[0].get_lists("#") for y in x.items]
                            ]   # Get list of meanings and remove markup for display
  
                          

                       #     print(section.lists()[0].fullitems)
                       #     print("###")
                            

                            #TODO:remove list
                            meanings=filter(lambda x: x not in ('','.','…','….','et ,') and not re.match("^\([^\(]*\)\.?$", x) and not re.match(r"^\([^)]*\)[. ]*$",x),meanings)
                       #     print([ x.items for x in section.lists()[0].get_lists()])
                    #        print(meanings)
                    #        print("####################################")
                            for meaning in meanings:

                                
                                cursor.execute(
                                    "INSERT INTO dictionary VALUES (?, ?, ?, ?)",
                                    (index, title, part_of_speech, meaning),
                                )
                                index += 1
            except (Exception, IndexError) as e:
                
                elem.clear()
                continue

            # https://stackoverflow.com/questions/12160418/why-is-lxml-etree-iterparse-eating-up-all-my-memory
            elem.clear()
            words += 1
            count += 1

            if count > 10000:
                count = 0
                cursor.execute("COMMIT")
                connection.commit()
                cursor.execute("BEGIN TRANSACTION")
             #   print(f"Tag count {tag_count}")
                print(
                    f"Processing {words} words and {index} meanings took {time.time()-start_time} seconds"
                )
    cursor.execute("COMMIT")
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Processing {words} words took {time.time()-start_time} seconds")


if __name__ == "__main__":
    main()
