import chromadb
from dotenv import load_dotenv
load_dotenv(verbose=True)
from chromadb.config import Settings
import openai
import os
import sys
from relational.repository import Repository

client = chromadb.Client(Settings(persist_directory="db"))
collection = client.create_collection("sample_collection")

openai.api_key = os.environ.get("OPENAI_API_KEY")

repo = Repository()
print("db ready")
cnt = 0
for line in sys.stdin:
  cnt += 1
  id = repo.add(1, line)
  print("loading...")

  openai.ChatCompletion.create(
    engine="davinci",
    prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=["\n", " Human:", " AI:"]
  )

  res = openai.Embedding.create(input=line, model="text-embedding-ada-002")
  embeddings = res['data'][0]['embedding']
  print(id, line)

  # Add docs to the collection. Can also update and delete. Row-based API coming soon!
  collection.add(
      embeddings=[embeddings], # we embed for you, or bring your own
      metadatas=[], # filter on arbitrary metadata!
      ids=[id], # must be unique for each doc 
  )

  if cnt > 3:
    res = openai.Embedding.create(input=line, model="text-embedding-ada-002")
    embeddings = res['data'][0]['embedding']
    results = collection.query(
        query_embeddings=[embeddings],
        n_results=3,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )
    print(results)