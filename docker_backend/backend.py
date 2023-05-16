from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import sqlite3

#uvicorn backend:app --reload


origins = [
    "http://localhost:3000",
    "https://wd400.github.io/",
    "*"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def get_neigh(lang):
    embeddings=np.load(f'def_embeddings_{lang}.npy')
    neigh = NearestNeighbors(n_neighbors=200,  metric='cosine',algorithm='brute',n_jobs=-1)
    neigh.fit(embeddings)
    return neigh

def db_data(lang):
    connection = sqlite3.connect(f"database_{lang}.db")
    cursor = connection.cursor()
    db_data = cursor.execute("SELECT id,word,definition FROM dictionary").fetchall()
    cursor.close()
    connection.close()
    
    db_data.sort(key=lambda x:x[0])
    return [ row[1:] for row in db_data]


#https://huggingface.co/models?language=fr&library=sentence-transformers&sort=downloads
fr_model = SentenceTransformer('inokufu/flaubert-base-uncased-xnli-sts')
en_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

fr_db_data=db_data('fr')
fr_neigh=get_neigh("fr")

en_db_data=db_data('en')
en_neigh=get_neigh("en")

class Definition(BaseModel):
    definition: str
    lang:str

@app.post("/")
async def root(definition:Definition):
    if len(definition.definition)>200:
        return []
    if definition.lang=="fr":
        nearest_defs=fr_neigh.kneighbors([fr_model.encode(definition.definition)], 200, return_distance=False)
        print(max(nearest_defs[0]),len(fr_db_data))
        return [fr_db_data[x] for x in nearest_defs[0]]
    else:
        nearest_defs=en_neigh.kneighbors([en_model.encode(definition.definition)], 200, return_distance=False)
        return [en_db_data[x] for x in nearest_defs[0]]
        #nearest_defs=neigh.kneighbors([model.encode(definition.definition)], 200, return_distance=False)
    
