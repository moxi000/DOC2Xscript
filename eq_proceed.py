import sys
import re
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class MarkdownProcessor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DOC2X-MD-Eq-Proceeder")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("拖拽文件到此或点击按钮选择文件", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("QLabel { border: 2px dashed #aaa; }")
        self.label.setAcceptDrops(True)
        layout.addWidget(self.label)

        self.uploadButton = QPushButton("上传文件", self)
        self.uploadButton.clicked.connect(self.openFileDialog)
        layout.addWidget(self.uploadButton)

        author_info = QLabel("Author：Moxi\nMail：1139164959@qq.com", self)
        author_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_info)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.processFile(file_path)

    def openFileDialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择Markdown文件", "", "Markdown Files (*.md)")
        if file_path:
            self.processFile(file_path)

    def processFile(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            pattern = r'(\\\[([\s\S]*?)\\\])\s*\((.*?)\)'
            
            def replace_with_tag(match):
                equation = match.group(2)
                tag = match.group(3)
                return f'\\[{equation}\\tag{{{tag}}}\\]'

            new_content = re.sub(pattern, replace_with_tag, content)

            output_path = file_path.replace('.md', '_processed.md')
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            self.label.setText(f"处理完成，文件保存为: {output_path}")
        except Exception as e:
            self.label.setText(f"处理文件时出错: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    processor = MarkdownProcessor()
    processor.show()
    sys.exit(app.exec())
