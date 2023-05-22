
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from function import start
from PyQt5.QtCore import *

class func_thread(QThread):
    def __init__(self):
        super(func_thread, self).__init__()
    def start_function(self):
        global worktime, cleartime
        worktime = int(worktime.text())
        cleartime = int(cleartime.text())
        assert 30 <= worktime <= 240, 'The working time should be between 30 and 240' 
        assert 5 <= cleartime <= 120, 'Error the clearime should be between 5 and 120'
        start(worktime, cleartime)
    def run(self):
        self.start_function()

app = QApplication(sys.argv)
        
window = QWidget()
window.setWindowTitle('Time to Look far away')  # 设置窗口标题

work_label = QLabel('Work time/min')
work_label.setFont(QFont('Arial', 13))
worktime = QLineEdit('45')
worktime.setPlaceholderText('input work time')

clear_label = QLabel('Clear time/min')
clear_label.setFont(QFont('Arial', 13))
cleartime = QLineEdit('60')
cleartime.setPlaceholderText('input clear time')

mythread = func_thread()
def stop_btn_click():
    mythread.quit()
    # stop()
    sys.exit()
def start_btn_click():
    global form 
    start_notify = QLabel('已启动')
    form.addRow(start_notify)
    form.setAlignment(start_notify, Qt.AlignCenter)
    mythread.start()
start_btn = QPushButton()
start_btn.setText('开启通知')
start_btn.clicked.connect(start_btn_click)

stop_btn = QPushButton()
stop_btn.setText('停止通知')
stop_btn.clicked.connect(stop_btn_click)
form = QFormLayout()
form.addRow(work_label, worktime)
form.addRow(clear_label, cleartime)
form.addRow(start_btn)
form.addRow(stop_btn)
vbox = QVBoxLayout()
vbox.addLayout(form)
window.setLayout(vbox)
# 设置窗口大小
window.setGeometry(100, 100, 300, 200)

# 显示窗口
window.show()

# 运行应用程序的主循环
# app.exec_()
sys.exit(app.exec_())

