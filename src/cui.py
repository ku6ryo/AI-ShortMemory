from dotenv import load_dotenv
load_dotenv(verbose=True)
from ai.base import AiBase

assistant = AiBase()

while(True):
  user_input = input("ASK  : ")
  res = assistant.respond(user_input)
  print("REPLY: ", res)
    
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
        res = chat_completion(
          messages=[{ "role": "system", "content": "You are an AI bot who summarize given text." }, { "role": "user", "content": f"{original_text}\n\nSummary:"}],
        )
        return res