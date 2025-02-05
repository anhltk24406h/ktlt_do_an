import os
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.llms.ctransformers import CTransformers
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from numpy.f2py.crackfortran import verbose


class QABotProcessAnswer():
    def __init__(self):
        # Khởi tạo các biến
        self.llm_chain=None
        self.db=None
        self.response=None
        self.llm=None
        self.prompt=None

        #Khởi tạo các hàm
        self.load_llm()
        self.read_vector_db()
        self.create_prompt()
        self.create_qa_chain()
    def load_llm(self):
        """Tải mô hình LLaMA."""
        self.llm = CTransformers(
            model="../lbs/vinallama-7b-chat_q5_0.gguf",
            model_type="llama",
            max_new_tokens=1024,
            temperature=0.01
        )
        return self.llm

    def read_vector_db(self):
        """Đọc vector database từ FAISS."""
        embedding_model = GPT4AllEmbeddings(model_file="../lbs/all-MiniLM-L6-v2-f16.gguf")
        self.db = FAISS.load_local(
            "../vectorstorage/db_faiss",
            embedding_model,
            allow_dangerous_deserialization=True
        )

    def create_prompt(self):
        template = """<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n
            {context}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant"""
        self.prompt=PromptTemplate(template=template, input_variables=["context", "question"])

    def create_qa_chain(self):
        self.llm_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.db.as_retriever(search_kwargs={"k": 3}, max_tokens_limit=512),
            return_source_documents=False,
            verbose=True,
            chain_type_kwargs={'prompt': self.prompt}
        )
    # def get_answer(self,question):
    #     return self.llm_chain.invoke({"query": question})
        print(self.llm_chain)

    def get_answer(self,question):
        """Trả lời câu hỏi của người dùng."""
        if self.llm_chain is None:
            raise ValueError("Lỗi: Hệ thống chưa được khởi tạo đúng cách. Vui lòng kiểm tra lại.")
        return self.llm_chain.invoke({"query": question})

    # Chạy thử chương trình (nhớ kiểm tra dòng 17)

if __name__ == "__main__":
        bot = QABotProcessAnswer()
        question = "Sự trung thực là gì??"
        response = bot.get_answer(question)
        print("Câu trả lời:", response)


"""
Đường dẫn file
model_file = "../lbs/vinallama-7b-chat_q5_0.gguf"
vector_db_path = "../vectorstorage/db_faiss"
"""