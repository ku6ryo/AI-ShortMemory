import openai
import uuid
from relational.repository import Repository
from gpt.gpt import get_embeddings
from vector.chroma import ChromaClient

class AiBase():

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.repo = Repository()
        self.chroma = ChromaClient()
        self.num_responded = 0
        self.max_history_length = 10
        self.history_text_length_limit = 1000
        self.interval_to_summarize = 4

    def gen_role_description(self):
        return "You are a smart AI assistant."
    
    def get_conversation_history(self):
        records = self.repo.getMessages(self.id, self.max_history_length)[::-1]
        gpt_messages = []
        total_text_len = 0
        for r in records:
          if (total_text_len + len(r.text) > self.history_text_length_limit):
            break
          if (r.role == 1):
            roleStr = "user"
          else:
            roleStr = "assistant"
          gpt_messages.append({ "role": roleStr, "content": r.text })
        return gpt_messages
    
    def summarize_hisotry(self):
        records = self.repo.getMessages(self.id, 10)[::-1]
        max_len = 1000
        messages = []
        total_text_len = 0
        for r in records:
          if (total_text_len + len(r.text) > max_len):
            break
          if (r.role == 1):
            m = f"user: {r.text}"
          else:
            m = f"assistant: {r.text}"
          messages.append(m)
        original_text = "\n".join(messages)
        res = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[{ "role": "system", "content": "You are an AI bot who summarize given text." }, { "role": "user", "content": f"{original_text}\n\nSummary:"}],
        )
        return res["choices"][0]["message"]["content"]

    def respond(self, message: str):
        self.num_responded += 1

        """
        summary = self.summarize_hisotry()
        summary_emb = get_embeddings(summary)
        summary_cnt_retrieve = 1
        summaries_text = ""
        if (self.chroma.collection.count() >= summary_cnt_retrieve):
            res = self.chroma.collection.query(
                query_embeddings=[summary_emb],
                n_results=summary_cnt_retrieve,
            )
            ids = res["ids"][0]
            summaries = self.repo.getSummaries(ids)
            for s in summaries:
                summaries_text += s.text + "\n"
        print("summaries_text: ", summaries_text)
        """

        role_description = self.gen_role_description()
        """
        if (summaries_text):
          role_description += f"\n\nWhat you've talked about previously.:\n{summaries_text}"
        """

        messages_to_send = [
          { "role": "system", "content": role_description },
        ]
        history = self.get_conversation_history()
        for m in history:
          messages_to_send.append(m)
        messages_to_send.append({ "role": "user", "content": message })

        ai_res = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages_to_send
        )
        ai_response = ai_res["choices"][0]["message"]["content"]

        u_res_id = self.repo.addMessage(self.id, 1, message)
        ai_res_id = self.repo.addMessage(self.id, 0, ai_response)

        if (self.num_responded % self.interval_to_summarize == self.interval_to_summarize - 1):
          summary = self.summarize_hisotry()
          summary_id = self.repo.addSummary(self.id, summary)
          print("summary: ", summary)
          summary_emb = get_embeddings(summary)
          self.chroma.add(
              embeddings=[summary_emb],
              metadatas=[{ "count": self.num_responded }],
              ids=[summary_id],
          )
        return ai_response