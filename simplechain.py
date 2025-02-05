from langchain.chains.llm import LLMChain
from langchain_community.llms.ctransformers import CTransformers
from langchain_core.prompts import PromptTemplate


class AIChatbot():
    def __init__(self):
        """Khởi tạo chatbot với mô hình ngôn ngữ và prompt template."""
        self.prompt = self.create_prompt()
        self.llm=self.load_llm()
        self.llm_chain = self.create_simple_chain()
    def load_llm(self):
        """Tải mô hình LLaMA từ tệp GGUF."""
        return CTransformers(
            model="../lbs/vinallama-7b-chat_q5_0.gguf",
            model_type="llama",
            max_new_tokens=1024,
            temperature=0.01
        )

    def create_prompt(self):
        """Tạo PromptTemplate cho chatbot."""
        template = """<|im_start|>system
        Bạn là một trợ lí AI hữu ích. Hãy trả lời người dùng một cách chính xác.
        <|im_end|>
        <|im_start|>user
        {question}<|im_end|>
        <|im_start|>assistant"""
        return PromptTemplate(template=template, input_variables=["question"])

    def create_simple_chain(self):
        """Tạo LLMChain để xử lý câu hỏi."""
        return LLMChain(prompt=self.prompt, llm=self.llm)

    def get_response(self, question):
        """Nhận câu trả lời từ chatbot dựa trên câu hỏi đầu vào."""
        return self.llm_chain.invoke({"question": question})

"""
if __name__ == "__main__":
        bot = AIChatbot()
        question = "Xin chào"
        response = bot.get_response(question)
        print("Câu trả lời:", response)
"""