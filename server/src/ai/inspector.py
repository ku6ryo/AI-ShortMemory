from ai.base import AiBase

class Inspector(AiBase):
    def gen_role_description(self):
        return "\n".join([
          "あなたは面接官です。",
          "話し相手がどのような人か、なにができるのかを聞き出します。"
        ])