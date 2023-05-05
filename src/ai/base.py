import uuid
from relational.repository import Repository
from gpt.gpt import chat_completion, count_token

class AiBase():

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.person_to_talk_to_id = str(uuid.uuid4())
        self.repo = Repository()
        self.num_responded = 0
        self.max_history_length = 100
        self.history_token_limit = 2000

    def set_topic(self, topic: str):
        self.topic = topic

    def gen_role_description(self):
        return "You are an AI assistant."
    
    def gen_system_message(self):
        role_description = self.gen_role_description()
        message = f"{role_description}"
        if (self.topic):
          message += f" The topic is {self.topic}."
        return message
    
    def get_conversation_history(self, limit = 100):
        records = self.repo.getMessages(self.id, limit)[::-1]
        gpt_messages = []
        total_tokens = 0
        for r in records:
            if (total_tokens + r.tokens > self.history_token_limit):
              break
            if (r.user_id == self.id):
              roleStr = "assistant"
            else:
              roleStr = "user"
            total_tokens += r.tokens
            gpt_messages.append({ "role": roleStr, "content": r.text })
        return gpt_messages

    def respond(self, message: str):
        self.num_responded += 1
        messages_to_send = [
          { "role": "system", "content": self.gen_system_message() },
        ]
        history = self.get_conversation_history(self.max_history_length)
        for m in history:
          messages_to_send.append(m)
        messages_to_send.append({ "role": "user", "content": message })
        ai_response = chat_completion(messages_to_send)

        self.repo.addMessage(self.id, self.person_to_talk_to_id, message, count_token(message))
        self.repo.addMessage(self.id, self.id, ai_response, count_token(ai_response))
        return ai_response