FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

EXPOSE 8000
ENV TRANSFORMERS_CACHE="/cache/"
CMD [ "python3", "-m" , "uvicorn", "backend:app","--host", "0.0.0.0"]

