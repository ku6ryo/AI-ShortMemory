from dotenv import load_dotenv
load_dotenv(verbose=True)
import os, sys, openai
from assistant import Assistant

openai.api_key = os.environ.get("OPENAI_API_KEY")

assistant = Assistant()

for line in sys.stdin:
  res = assistant.respond(line)