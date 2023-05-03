import os
import uuid
import chromadb
from chromadb.config import Settings

class ChromaClient:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.client = chromadb.Client(Settings(persist_directory=os.environ.get("CHROMADB_DIR")))
        self.collection = self.client.create_collection(self.id)
    
    def add(self, embeddings, metadatas, ids):
        self.collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )