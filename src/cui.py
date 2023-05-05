from dotenv import load_dotenv
load_dotenv(verbose=True)
from ai.base import AiBase

assistant = AiBase()

while(True):
  user_input = input("ASK  : ")
  res = assistant.respond(user_input)
  print("REPLY: ", res)