import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# 导入my_win.py中内容
from ui_base import *
from wjx import *

class MyThread(QThread):
   def __init__(self, url):
       super(MyThread,self).__init__()
       self.wjx = WenJuanXing(url)
       self.nums = 0
       self.mian_win = None
       self.istop = False
       self.postNums = 0

   def run(self):
        while True:
            PostNum = 0
            for i in range(self.nums):
                if self.istop:
                    return
                self.wjx.set_post_url()
                result = self.wjx.post_data()
                print(result.content.decode())

                if int(result.text[0:2]) in [10]:  # 循环10次，调用10次Auto_WjX函数
                    print('[ Response : %s ]  ===> 提交成功！！！！' % result.text[0:2])
                    self.mian_win.log.append('[ Response : %s ]  ===> 提交成功！！！！' % result.text[0:2])
                    PostNum += 1
                else:
                    print('[ Response : %s ]  ===> 提交失败！！！！' % result.text[0:2])
                    self.mian_win.log.append('[ Response : %s ]  ===> 提交失败！！！！' % result.text[0:2])
                time.sleep(2)  # 设置休眠时间，这里要设置足够长的休眠时间
                self.postNums = PostNum
            print('脚本运行结束，成功提交%s份调查报告' % PostNum)  # 总结提交成功的数量，并打印
            self.mian_win.log.append('脚本运行结束，成功提交%s份调查报告' % PostNum)
            self.mian_win.pushButton_run.setText('run')
            self.mian_win.lineEdit_num.setEnabled(True)
            break

# 创建mainWin类并传入Ui_MainWindow
class mainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainWin, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_run.clicked.connect(self.run_click)
        self.pushButton_set.clicked.connect(self.set_answer)
        self.pushButton_next.clicked.connect(self.next_title)
        self.pushButton_run.setEnabled(False)
        self.lineEdit_num.setEnabled(False)
        self.pushButton_next.setEnabled(False)
        self.lineEdit_answer.setEnabled(False)
        self.url = ''
        self.index = 1
        self.nums = 0
        self.answer_list = []
        self.title_list = []
        self.work = MyThread('')
        self.isStop = 0
        self.log.append('********提示：先看使用说明，不看我也没办法********')

    def run_click(self):
        if self.pushButton_run.text() == 'run':
            self.pushButton_run.setText('stop')
            self.lineEdit_num.setEnabled(False)
            self.nums = int(self.lineEdit_num.text())
            self.work.nums = self.nums
            self.work.wjx.submit_data = self.answer_list
            self.work.mian_win = self
            self.work.start()
        else:
            self.work.istop = True
            self.log.append('脚本停止，已经成功提交%s份调查报告' % (self.work.postNums + 1))
            self.pushButton_run.setText('run')
            self.lineEdit_num.setEnabled(True)

    def set_answer(self):
        self.url = self.lineEdit_url.text()
        if len(self.url) > 0:
            self.work = MyThread(self.url)
            response = self.work.wjx.get_response()
            self.title_list = self.work.wjx.get_title_list(response.text)
            title = '第1题：' + self.title_list[0]['title']+'    在下方输入答案'
            self.log.setText(title)
            self.pushButton_set.setEnabled(False)
            self.lineEdit_url.setEnabled(False)
            self.pushButton_next.setEnabled(True)
            self.lineEdit_answer.setEnabled(True)
        else:
            self.log.append("input url first")

    def next_title(self):
        ans = self.lineEdit_answer.text()
        self.answer_list.append(ans)
        if self.index >= len(self.title_list):
            self.pushButton_next.setEnabled(False)
            self.log.setText('答案设置完成， 填写次数运行')
            self.pushButton_run.setEnabled(True)
            self.lineEdit_answer.clear()
            self.lineEdit_answer.setEnabled(False)
            self.lineEdit_num.setEnabled(True)
            return
        title = '第'+str(self.index + 1)+'题：' + self.title_list[self.index]['title'] + '在下方输入答案'
        self.log.setText(title)
        self.lineEdit_answer.clear()
        self.index += 1

if __name__ == '__main__':
    # 下面是使用PyQt5的固定用法
    app = QApplication(sys.argv)
    main_win = mainWin()
    main_win.show()
    QMessageBox.information(main_win,  # 使用infomation信息框
                            "提醒",
                            "吾爱发布，仅供交流")
    sys.exit(app.exec_())