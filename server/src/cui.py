from dotenv import load_dotenv
load_dotenv(verbose=True)
import os, sys, openai
from ai.base import AiBase

openai.api_key = os.environ.get("OPENAI_API_KEY")

assistant = AiBase()

for line in sys.stdin:
  res = assistant.respond(line)
  print(res)