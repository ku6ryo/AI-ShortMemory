import openai
import uuid
from relational.repository import Repository
from gpt.gpt import get_embeddings
from vector.chroma import ChromaClient

class Assistant():

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.repo = Repository()
        self.chroma = ChromaClient()

    def gen_role_description(self):
        return "You are a smart AI assistant."

    def respond(self, message: str):
        records = self.repo.getMessages(10)[::-1]
        u_res_id = self.repo.add(self.id, 1, message)
        print("loading...")

        messages_to_send = [
          { "role": "system", "content": self.gen_role_description() }
        ]
        for r in records:
          if (r.role == 1):
            roleStr = "user"
          else:
            roleStr = "assistant"
          messages_to_send.append({ "role": roleStr, "content": r.text })
        messages_to_send.append({ "role": "user", "content": message })

        ai_res = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages_to_send
        )
        ai_response = ai_res["choices"][0]["message"]["content"]
        ai_res_id = self.repo.add(self.id, 0, ai_response)

        user_emb = get_embeddings(message)
        ai_emb = get_embeddings(ai_response)

        self.chroma.add(
            embeddings=[user_emb, ai_emb],
            metadatas=[{ "role": 1, }, { "role": 0 }],
            ids=[u_res_id, ai_res_id],
        )
        """
        self.chroma.collection.query(
            query_embeddings=[user_emb],
            n_results=3,
        )
        """
        return ai_response