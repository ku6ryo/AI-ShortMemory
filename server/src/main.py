from dotenv import load_dotenv
load_dotenv(verbose=True)
import chromadb
from chromadb.config import Settings
import openai
import os
import sys
print(os.environ.get("OPENAI_API_KEY"))
print(os.environ.get("DATABASE"))
from relational.repository import Repository
from gpt.gpt import get_embeddings

client = chromadb.Client(Settings(persist_directory="storage/chromadb"))
collection = client.create_collection("sample_collection")

openai.api_key = os.environ.get("OPENAI_API_KEY")

repo = Repository()
print("db ready")
cnt = 0
for line in sys.stdin:
  cnt += 1
  records = repo.getMessages(10)[::-1]
  u_res_id = repo.add(1, line)
  print("loading...")

  messages_to_send = [
    {"role": "system", "content": "あなたは森の妖精です。ご主人様に仕えています。返答は短く返してください。"}
  ]
  for r in records:
    if (r.role == 1):
      roleStr = "user"
    else:
      roleStr = "assistant"
    messages_to_send.append({ "role": roleStr, "content": r.text })
  messages_to_send.append({ "role": "user", "content": line })
  print(messages_to_send)

  ai_res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages_to_send
  )
  ai_response = ai_res["choices"][0]["message"]["content"]
  ai_res_id = repo.add(0, ai_response)
  print(ai_response)

  user_emb = get_embeddings(line)
  ai_emb = get_embeddings(ai_response)

  # Add docs to the collection. Can also update and delete. Row-based API coming soon!
  collection.add(
      embeddings=[user_emb, ai_emb], # we embed for you, or bring your own
      metadatas=[{ "role": 1, }, { "role": 0 }], # filter on arbitrary metadata!
      ids=[u_res_id, ai_res_id], # must be unique for each doc 
  )

  if cnt > 3:
    results = collection.query(
        query_embeddings=[user_emb],
        n_results=3,
    ) 
    print(results)