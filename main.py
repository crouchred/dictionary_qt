from time import time
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit,  QHBoxLayout, QPushButton, QVBoxLayout, QGridLayout, QTextBrowser
from PyQt6.QtGui import QIcon, QFont, QPixmap
import sys
import requests
from requests.exceptions import ReadTimeout,ConnectionError
from lxml import etree
import json

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("cxy大字典")
        self.setGeometry(900,200,400,600)
        self.create_widget()

    def create_widget(self):
        box = QGridLayout()

        btn = QPushButton("确定")
        btn.clicked.connect(self.search)

        self.line_edit = QLineEdit(self)
        self.line_edit.returnPressed.connect(self.search)

        self.text_en = QTextBrowser()
        self.text_de = QTextBrowser()

        box.addWidget(self.line_edit,0,0)
        box.addWidget(btn, 0,1)
        box.addWidget(self.text_de,1,0)
        box.addWidget(self.text_en,2,0)
        self.setLayout(box)

    def search(self):
        text = self.line_edit.text()
        en_res = Translate().get_en_en(text) 
        de_res = Translate().get_de(text)
        self.text_en.setText(en_res)
        self.text_de.setText(de_res)

class Translate:

    retry = 3
    timeout = 3
    de_mapping = {
            'a2': 'ä',
            'u2': 'ü',
            's2': 'ß',
            'o2': 'ö',
            'A2': 'Ä',
            'U2': 'Ü',
            'S2': 'ẞ',
            'O2': 'Ö',
        }

    def get_en_en(self, text):
        try:
            r = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/{}".format(text), verify=False, timeout=self.timeout)
        except (ReadTimeout,ConnectionError):
            return "en网络超时" 
        data = json.loads(r.text)
        if isinstance(data,dict):
            return ""
        meanings = data[0]['meanings']
        text = ""
        for meaning in meanings:
            text += meaning['partOfSpeech'] + "\n"
            for defination in meaning.get('definitions'):
                text += defination['definition']  + "\n"
            text += "\n"
        return text
        

    def get_en_cn(self, text):
        try:
            r = requests.get("https://apii.dict.cn/mini.php?q={}".format(text), timeout=self.timeout)
        except (ReadTimeout,ConnectionError):
            return "en网络超时" 
        html = etree.HTML(r.text)
        data = html.xpath('//*[@id="e"]/text()')
        return '\n\n'.join(data) + "\n https://dict.youdao.com/w/eng/{}/".format(text)

    def get_de(self, text):
        for k,v in self.de_mapping.items():
            if k in text:
                text = text.replace(k,v)
        try:
            r = requests.get("https://www.godic.net/dicts/de/{}".format(text), timeout=self.timeout)
        except (ReadTimeout,ConnectionError):
            return "de网络超时" 
        html = etree.HTML(r.text)
        spans = html.xpath('//*[@id="ExpFCChild"]/span')
        #spans = html.xpath('//*[@id="ExpFCChild"]')
        texts = html.xpath('//*[@id="ExpFCChild"]/text()')
        res = ""
        for span in spans:
            if span.get("class") in ['cara', 'exp']:
                if span.text:
                    res += span.text + "\n"
        print("----\n")
        for text in texts:
            res += text + "\n"
        return res + "\n https://www.godic.net/dicts/de/{}".format(text)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

def test_de():
    for Wort in ["Wort", "hallo", "Tiergarten", "Universita2t"]:
        print(Translate().get_de(Wort))

def test_en():
    #print(Translate().get_en_cn("lunch"))
    print(Translate().get_en_en("lunch"))

if __name__=="__main__":
    main()
    #test_de()
    #test_en()