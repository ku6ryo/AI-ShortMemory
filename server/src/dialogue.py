from dotenv import load_dotenv
load_dotenv(verbose=True)
import os, openai
from ai.inspector import Inspector
from ai.kid import Kid

openai.api_key = os.environ.get("OPENAI_API_KEY")

ai_a = Kid()
ai_b = Inspector()

limit = 20
cnt = 0

prev_b_res = "こんにちは"
while(cnt < limit):
    cnt += 1
    a_res = ai_a.respond(prev_b_res)
    print ("A: " + a_res)
    b_res = ai_b.respond(a_res)
    print ("B: " + b_res)
    print ("====================")
    prev_b_res = b_res