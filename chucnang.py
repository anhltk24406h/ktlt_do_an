from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QHBoxLayout, QLabel, QVBoxLayout
from PyQt6 import QtCore

from models.prepare_vector_db import VectorDBProcess
from models.qabot import QABotProcessAnswer
from models.simplechain import AIChatbot

from ui.duanmonhoc import Ui_MainWindow

class chucnang(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.selected_file_path = ""
        self.questions = []
        self.vector_db_processor = VectorDBProcess()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.lineEditInputAnswer.setText("Xin chào, tôi có thể giúp gì cho bạn nè?")
        self.pushButtonSubmitext.clicked.connect(self.handle_user_input)
        self.pushButtonopenfile.clicked.connect(self.handle_file_selection)
        self.pushButtonScrolldown.clicked.connect(self.scrolldown_UIprocessing)
        self.pushButtonRefresh.clicked.connect(self.refresh_functionprocessing)

    # Question input and UI interaction
    # Lỗi logic: tổ chức button sai
    def handle_user_input(self):
        question = self.lineEditInputQuestion.text()
        if question:
            self.labelinputQuestion.setText(question)
            self.questions.append(question)
            print(self.questions)
            self.lineEditInputQuestion.clear()


        # Response with file or without file
        """
        if self.selected_file_path is None:
            self.response_process_without_file()
        else:
        """
        self.response_process_with_file()

    # Adding question
    def handle_file_selection(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self.MainWindow,
            "Chọn File PDF",
            "",
            "PDF Files (*.pdf)"
        )
        self.pushButtonopenfile.setIcon(
            QIcon("D:\\CodeArchive\\KTLT\\Duanmonhoc\\images\\ic_processing.png"))

        # Kiểm tra nếu file_path rỗng
        if not file_path:
            self.pushButtonopenfile.setIcon(
                QIcon("D:\\CodeArchive\\KTLT\\Duanmonhoc\\images\\ic_pdf-file.png"))
            return

        if file_path:
            try:
                    """
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    """

                    """
                    # Cắt tên file nếu quá dài (trên 25 ký tự)
                    file_name = file_path.split('/')[-1]
                    if len(file_name) > 25:
                        file_name = file_name[:22] + "..."
                    """
                    # Lưu đường dẫn file
                    self.selected_file_path = file_path

                    #Xử lý vectorDB từ đường dẫn
                    self.vector_db_processor.create_db_from_files(file_path)

                    # Đổi icon của nút pushButtonopenfile thành icon file PDF
                    self.pushButtonopenfile.setIcon(
                        QIcon("D:\\CodeArchive\\KTLT\\Duanmonhoc\\images\\ic_pdf-file.png"))
            #Bắt lỗi file pdf
            except Exception as e:
                QMessageBox.critical(self.MainWindow, "Lỗi", f"Không thể mở file: {str(e)}")

    # Chatbot with file
    def response_process_with_file(self):
        if self.questions:
            question = self.questions[-1]
        else:
            question = ""
        qa_bot = QABotProcessAnswer()
        response = qa_bot.get_answer(question)
        self.questions.append(response)
        self.lineEditInputAnswer.setText(f"response")

    # Chatbot without file
    def response_process_without_file(self):
        if self.questions:
            question=self.questions[-1]
        else:
            question=""
        print(question)
        # Gọi class AIChatbot
        simplechat = AIChatbot()
        response = simplechat.get_response(question)
        self.questions.append(response)
        self.lineEditInputAnswer.setText(f"response")
        print(response)

    def scrolldown_UIprocessing(self):
        pass

    def refresh_functionprocessing(self):
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Xác nhận tạo mới hội thoại!")
        dlg.setText("Bạn có muốn tạo mới hội thoại không?")
        dlg.setIcon(QMessageBox.Icon.Question)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        dlg.setStandardButtons(buttons)
        if dlg.exec() == QMessageBox.StandardButton.Yes:
            self.labelinputQuestion.setText("Đang chờ câu hỏi")
            self.questions.clear()
            self.pushButtonopenfile.setIcon(
            QIcon("D:\\CodeArchive\\KTLT\\Duanmonhoc\\images\\ic_add-button.png"))
            self.lineEditInputAnswer.setText("Xin chào, tôi có thể giúp gì cho bạn nè?")
            self.selected_file_path = None
            # self.vector_db_processor.clear_database()
