import openai

def get_embeddings(text: str):
  res = openai.Embedding.create(input=text, model="text-embedding-ada-002")
  embeddings = res['data'][0]['embedding']
  return embeddings