import sys
import math
import PyQt5.QtCore
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, \
    QGridLayout, QFormLayout, QLineEdit, QTextEdit, QMainWindow
from s_aes import jiemi, jiami


# 十进制转二进制(默认8位)
def tenTotwo(number, bit=8):
    # 定义栈
    s = []
    binstring = ''
    while number > 0:
        # 余数进栈
        rem = number % 2
        s.append(rem)
        number = number // 2
    while len(s) > 0:
        # 元素全部出栈即为所求二进制数
        binstring = binstring + str(s.pop())
    while len(binstring) < bit:
        binstring = '0' + binstring
    return binstring


# 二进制转十进制
def twototen(str1):
    num = 0
    n = 0
    for i in range(len(str1)):
        a = str1[len(str1)-1-n]
        a = int(a)
        num = num + a*math.pow(2, n)
        n = n + 1
    return int(num)
# ui设计
app = QApplication(sys.argv)
# 加密ui
class jiamui(QWidget):
    switch_window1 = PyQt5.QtCore.pyqtSignal()
    switch_window2 = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        super(jiamui,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("加密")
        layout = QGridLayout()
        self.setGeometry(600, 300, 600, 600)


        pLabel = QLabel("明文")
        self.pLineEdit = QLineEdit(" ")
        keyLabel = QLabel("密钥")
        self.keyLineEdit = QLineEdit(" ")
        cipherLabel = QLabel("密文")
        self.cipherLineEdit = QLineEdit("")
        # layout.setSpacing(10)
        layout.addWidget(pLabel,1,0)
        layout.addWidget(self.pLineEdit,1,1)
        layout.addWidget(keyLabel, 2, 0)
        layout.addWidget(self.keyLineEdit, 2, 1)
        layout.addWidget(cipherLabel,3,0)
        layout.addWidget(self.cipherLineEdit,3,1)
        layout.setColumnStretch(1, 10)
        save_Btn = QPushButton('确定')
        cancle_Btn = QPushButton('取消')
        swich_btn = QPushButton("解密")
        swich_btn1 = QPushButton("破解")
        cancle_Btn.clicked.connect(QCoreApplication.quit)
        save_Btn.clicked.connect(self.addNum)
        swich_btn.clicked.connect(self.switch)
        swich_btn1.clicked.connect(self.switch1)
        layout.addWidget(save_Btn)
        layout.addWidget(cancle_Btn)
        layout.addWidget(swich_btn)
        layout.addWidget(swich_btn1)
        self.setLayout(layout)

    def addNum(self):
        p = self.pLineEdit.text()  # 获取文本框内容
        p = p.strip()
        if len(p) == 2:
            p1 = p[0]
            p2 = p[1]
            ascll1 = ord(p1)
            ascll2 = ord(p2)
            binascll1 = tenTotwo(ascll1)
            binascll2 = tenTotwo(ascll2)
            p = binascll1 + binascll2
        else:
            p = p.strip()
        key = self.keyLineEdit.text()
        key = key.strip()
        # 对明文进行加密
        ciphertext = jiami(p, key)
        self.cipherLineEdit.setText(ciphertext)
        print('---------------------------------------------------------')

    def switch(self):
        self.switch_window1.emit()

    def switch1(self):
        self.switch_window2.emit()



# 解密ui
class jiemiui(QWidget):
    switch_window2 = PyQt5.QtCore.pyqtSignal()
    switch_window3 = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        super(jiemiui,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("解密")
        layout = QGridLayout()
        self.setGeometry(600, 300, 600, 600)


        cipherLabel = QLabel("密文")
        self.cipherLineEdit = QLineEdit(" ")
        keyLabel = QLabel("密钥")
        self.keyLineEdit = QLineEdit(" ")
        pLabel = QLabel("明文")
        self.pLineEdit = QLineEdit("")
        # layout.setSpacing(10)
        layout.addWidget(cipherLabel,1,0)
        layout.addWidget(self.cipherLineEdit,1,1)
        layout.addWidget(keyLabel, 2, 0)
        layout.addWidget(self.keyLineEdit, 2, 1)
        layout.addWidget(pLabel,3,0)
        layout.addWidget(self.pLineEdit,3,1)
        layout.setColumnStretch(1, 10)
        save_Btn = QPushButton('确定')
        cancle_Btn = QPushButton('取消')
        swich_btn = QPushButton("加密")
        swich_btn1 = QPushButton("破解")
        cancle_Btn.clicked.connect(QCoreApplication.quit)
        save_Btn.clicked.connect(self.addNum)
        swich_btn.clicked.connect(self.switch)
        swich_btn1.clicked.connect(self.switch1)
        layout.addWidget(save_Btn)
        layout.addWidget(cancle_Btn)
        layout.addWidget(swich_btn)
        layout.addWidget(swich_btn1)
        self.setLayout(layout)

    def addNum(self):
        p1 = self.cipherLineEdit.text()  # 获取文本框内容
        key1 = self.keyLineEdit.text()
        key1 = key1.strip()
        # 生成子密钥 K1 和 K2
        # 对密文进行解密
        p1 = p1.strip()
        plaintext1 = jiemi(p1, key1)
        mingwen1 = plaintext1[0:7]
        mingwen2 = plaintext1[8:15]
        ascll1 = twototen(mingwen1)
        ascll2 = twototen(mingwen2)
        chr1 = chr(ascll1)
        chr2 = chr(ascll2)
        output = plaintext1 + 'ascall码对应字符为:' + chr1 + chr2
        self.pLineEdit.setText(output)
        print('--------------------------------------------------------')

    def switch(self):
        self.switch_window2.emit()

    def switch1(self):
        self.switch_window3.emit()


# 暴力破解ui
class pojieui(QWidget):
    switch_window3 = PyQt5.QtCore.pyqtSignal()
    switch_window4 = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        super(pojieui,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("破解")
        layout = QGridLayout()
        self.setGeometry(600, 300, 600, 600)


        cipherLabel = QLabel("明文")
        self.cipherLineEdit = QLineEdit(" ")
        keyLabel = QLabel("密文")
        self.keyLineEdit = QLineEdit(" ")
        pLabel = QLabel("密钥")
        self.pLineEdit = QLineEdit("")
        # layout.setSpacing(10)
        layout.addWidget(cipherLabel,1,0)
        layout.addWidget(self.cipherLineEdit,1,1)
        layout.addWidget(keyLabel, 2, 0)
        layout.addWidget(self.keyLineEdit, 2, 1)
        layout.addWidget(pLabel,3,0)
        layout.addWidget(self.pLineEdit,3,1)
        layout.setColumnStretch(1, 10)
        save_Btn = QPushButton('确定')
        cancle_Btn = QPushButton('取消')
        swich_btn = QPushButton("加密")
        swich_btn1 = QPushButton("破解")
        cancle_Btn.clicked.connect(QCoreApplication.quit)
        save_Btn.clicked.connect(self.addNum)
        swich_btn.clicked.connect(self.switch)
        swich_btn1.clicked.connect(self.switch1)
        layout.addWidget(save_Btn)
        layout.addWidget(cancle_Btn)
        layout.addWidget(swich_btn)
        layout.addWidget(swich_btn1)
        self.setLayout(layout)

    def addNum(self):
        p1 = self.cipherLineEdit.text()  # 获取文本框内容
        pw = self.keyLineEdit.text()
        pw = pw.strip()
        p1 = p1.strip()
        p = str(p1).strip()
        pw = str(pw).strip()
        key = 0
        output = ''
        for i in range(65536):
            key1 = tenTotwo(key, bit=16)
            ciphertext = jiami(p, key1)
            if ciphertext == pw:
                #self.pLineEdit.setText(key1)
                output += key1 + ' '
                key = key + 1
            else:
                key = key + 1
        print('密钥有', output)
        self.pLineEdit.setText(output)

    def switch(self):
        self.switch_window3.emit()

    def switch1(self):
        self.switch_window4.emit()


class Controller1:
    def __init__(self):
        self.jiami = jiamui()
        self.jiemi = jiemiui()
        self.pojie = pojieui()
        self.jiami.hide()
        self.jiemi.hide()
        self.pojie.hide()

    def show_jiamiui(self):
        self.jiami.switch_window1.connect(self.show_jiemiui)
        self.jiami.switch_window2.connect(self.show_pojieui)
        self.jiami.show()

    def show_jiemiui(self):
        self.jiami.close()
        self.jiemi.show()

    def show_pojieui(self):
        self.jiami.close()
        self.pojie.show()

class Controller2:
    def __init__(self, pic1):
        self.jiami = pic1.jiami
        self.jiemi = pic1.jiemi
        self.pojie = pic1.pojie

    def show_jiemiui_(self):
        self.jiemi.switch_window2.connect(self.show_jiamiui_)
        self.jiemi.switch_window3.connect(self.show_pojieui_)
        self.jiemi.hide()

    def show_jiamiui_(self):
        self.jiemi.close()
        self.jiami.show()

    def show_pojieui_(self):
        self.jiemi.close()
        self.pojie.show()


class Controller3:
    def __init__(self, pic1):
        self.jiami = pic1.jiami
        self.jiemi = pic1.jiemi
        self.pojie = pic1.pojie

    def show_pojieui__(self):
        self.pojie.switch_window3.connect(self.show_jiamiui__)
        self.pojie.switch_window4.connect(self.show_jiemiui__)
        self.pojie.hide()

    def show_jiamiui__(self):
        self.pojie.close()
        self.jiami.show()

    def show_jiemiui__(self):
        self.pojie.close()
        self.jiemi.show()


controller1 = Controller1()  # 控制器实例
controller2 = Controller2(controller1)
controller3 = Controller3(controller1)
controller1.show_jiamiui()
controller2.show_jiemiui_()
controller3.show_pojieui__()


sys.exit(app.exec_())