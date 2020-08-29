import sys
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# 导入my_win.py中内容
from ui_base import *
from WJX_Autosubmit import *

class MyThread(QThread):
   def __init__(self, url, win, num):
        super(MyThread,self).__init__()
        self.wjx = WenJuanXing(url, win, num, self)
        self.flag = True
   def run(self):
       while self.flag:
           self.wjx.start_up()

class mainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run_click)
    def run_click(self):
        url = self.lineEdit.text()
        num = self.lineEdit_2.text()
        if url == '' or num == '':
            return
        thread = MyThread(url, self, num)
        thread.start()
        self.textBrowser.append("开始提交")
        self.pushButton.setEnabled(False)

if __name__ == '__main__':
    # 下面是使用PyQt5的固定用法
    app = QApplication(sys.argv)
    main_win = mainWin()
    main_win.show()
    QMessageBox.information(main_win,  # 使用infomation信息框
                            "提醒",
                            "吾爱发布，仅供交流")
    sys.exit(app.exec_())