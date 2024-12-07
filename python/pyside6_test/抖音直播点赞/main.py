import asyncio
import json
import re

import aiohttp
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QApplication, QPlainTextEdit
from PySide6.QtCore import Signal


class MyWindow(QWidget):
    finished = Signal(int)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.curl_bash_input = QPlainTextEdit()
        self.curl_bash_input.setMinimumHeight(500)
        self.curl_bash_input.setPlaceholderText('curl(bash)')
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText('重发次数, 最大1000')
        self.btn = QPushButton('')

        self.layout.addWidget(self.curl_bash_input)
        self.layout.addWidget(self.count_input)
        self.layout.addWidget(self.btn)

        self.btn.clicked.connect(self.dy_like)
        self.finished.connect(lambda x: QMessageBox.information(self, '完成', f'共点赞{x}次' + (', 次数用光, 稍等再试', '')[bool(x)]))

    def dy_like(self):
        count = self.count_input.text()

        try:
            if (n := int(count)) > 1000:
                QMessageBox.warning(self, '未执行', '重发次数过多, 最大1000')
                return

            asyncio.run(self.__dy_like(n))

        except Exception as e:
            QMessageBox.warning(self, 'error', str(e))

    async def __dy_like(self, n):
        url, header, per_count = self.get_url_header(self.curl_bash_input.toPlainText())

        async with aiohttp.ClientSession(headers=header) as session:
            tasks = [self.like(session, url) for _ in range(n)]
            resps = await asyncio.gather(*tasks)

            ok_count = 0
            for resp_text in resps:
                try:
                    data = json.loads(resp_text)['data']
                    print(data)

                    if data and data.get('message') != '手速太快了，请休息一下吧~':
                        ok_count += 1

                except Exception as e:
                    print(resp_text)

        self.finished.emit(per_count * ok_count)

    def get_url_header(self, src_text_curl_bash):
        url = re.findall(r"curl '(.*?)' ", src_text_curl_bash)[0]

        per_count = re.findall(r"&count=(.*?)&", src_text_curl_bash)[0]
        tmp = re.findall(r"  -H '(.*?)'", src_text_curl_bash)
        tmp2 = [i.split(': ') for i in tmp]
        header = {i[0]: i[1] for i in tmp2}

        return url, header, int(per_count)

    async def like(self, session, url):
        async with session.post(url=url, data='{}') as response:
            return await response.text()


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
