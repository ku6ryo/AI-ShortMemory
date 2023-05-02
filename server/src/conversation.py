from dotenv import load_dotenv
load_dotenv(verbose=True)
import os, openai
from assistant import Assistant

openai.api_key = os.environ.get("OPENAI_API_KEY")

class AI_Fairy(Assistant):
    def gen_role_description(self):
        return "あなたは森の妖精です。ご主人様に仕えています。返答は短く返してください。"

class AI_Human(Assistant):
    def gen_role_description(self):
        return "あなたは妖精に興味のある人間です。あなたに話しかけてくるのは妖精です。"

fairy = AI_Fairy()
human = AI_Human()

limit = 10
cnt = 0

prev_human_res = "こんにちは"
while(cnt < limit):
    cnt += 1
    f_res = fairy.respond(prev_human_res)
    print ("fairy: " + f_res)
    h_res = human.respond(f_res)
    print ("human: " + h_res)
    print ("====================")
    prev_human_res = h_res