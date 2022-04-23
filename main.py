from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit,  QHBoxLayout, QPushButton, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QIcon, QFont, QPixmap
import sys
import requests
from lxml import etree

from cv2 import line

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("cxy大字典")
        self.setGeometry(200,200,700,400)
        self.create_widget()

    def create_widget(self):
        box = QGridLayout()

        btn = QPushButton("确定")
        btn.clicked.connect(self.search)

        self.line_edit = QLineEdit(self)
        self.line_edit.returnPressed.connect(self.search)

        self.label = QLabel("文本")

        box.addWidget(self.line_edit,0,0)
        box.addWidget(btn, 0,1)
        box.addWidget(self.label,1,0)
        self.setLayout(box)

    def search(self):
        text = self.line_edit.text()
        en_res = get_en(text)
        self.label.setText(en_res)

def get_en(text):
    r = requests.get("https://apii.dict.cn/mini.php?q={}".format(text))
    html = etree.HTML(r.text)
    data = html.xpath('//*[@id="e"]/text()')
    return '\n\n'.join(data)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__=="__main__":
    #get_en("lunch")
    main()