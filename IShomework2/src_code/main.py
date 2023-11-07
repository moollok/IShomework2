import sys
import math
import PyQt5.QtCore
from PyQt5.QtCore import*
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, \
    QGridLayout, QFormLayout, QLineEdit, QTextEdit, QMainWindow


# 十进制转二进制(默认8位)
def tenTotwo(number, bit = 8):
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


# 通用置换函数
def permute(input_str, table):
    output_str = ""
    for bit_position in table:
        output_str += input_str[bit_position - 1]
    return output_str


# 循环左移函数
def ls(key, n):
    # 将密钥分成两段并循环左移 n 位
    left_half = key[:5]
    right_half = key[5:]
    shifted_left = left_half[n:] + left_half[:n]
    shifted_right = right_half[n:] + right_half[:n]
    return shifted_left + shifted_right


# 子密钥生成
def generate_key(k, p10_table, p8_table):
    # 执行 P10 置换
    p10_key = permute(k, p10_table)
    # 对结果进行左移操作和P8置换，得到 K1
    k1 = permute(ls(p10_key, 1), p8_table)
    # 再次对上一步结果进行左移操作h和P8置换，得到 K2
    k2 = permute(ls(ls(p10_key, 1), 2), p8_table)
    return k1, k2


# S-DES 的 F 函数
def F(right_half, k):
    # 对右半部分进行 E/P 扩展置换
    expanded = permute(right_half, ep_table)
    # 对结果与 K1 进行异或操作
    xored = '{0:08b}'.format(int(expanded, 2) ^ int(k, 2))
    # 将结果分为两组，并根据 S-box 进行替换
    s0_input = xored[:4]
    s1_input = xored[4:]
    # 根据S盒规则行列查找
    s0_row = int(s0_input[0] + s0_input[-1], 2)
    s0_col = int(s0_input[1:-1], 2)
    s1_row = int(s1_input[0] + s1_input[-1], 2)
    s1_col = int(s1_input[1:-1], 2)
    s0_output = '{0:02b}'.format(sbox0[s0_row][s0_col])
    s1_output = '{0:02b}'.format(sbox1[s1_row][s1_col])
    # 对两个输出串进行 P4 置换得到最终结果
    s_output = s0_output + s1_output
    return permute(s_output, p4_table)


# 加密过程
def encrypt(p, k1, k2):
    # 执行初始置换
    p = permute(p, ip_table)
    # 进行两轮 Feistel 加密
    l0 = p[:4]
    r0 = p[4:]
    l1 = r0
    # 第一轮的P4
    f_result = F(r0, k1)
    # p41和L0异或
    r1 = '{0:04b}'.format(int(l0, 2) ^ int(f_result, 2))
    # 第二轮的P4
    f_result = F(r1, k2)
    # p42和L1异或
    r2 = '{0:04b}'.format(int(l1, 2) ^ int(f_result, 2))
    # 逆置换并返回结果(左边R2右边R1)
    return permute(r2 + r1, ip_ni_table)


# 解密过程
def decrypt(c, k1, k2):
    # 执行初始置换
    c = permute(c, ip_table)
    # 进行两轮 Feistel 解密（注意子密钥的使用顺序）
    r2 = c[:4]
    l2 = c[4:]
    # 第一轮的P4
    f_result = F(l2, k2)
    # p41和R2异或
    l1 = '{0:04b}'.format(int(r2, 2) ^ int(f_result, 2))
    # 第二轮的P4
    f_result = F(l1, k1)
    # p42和R1异或
    r1 = '{0:04b}'.format(int(l2, 2) ^ int(f_result, 2))
    # 逆置换并返回明文
    return permute(r1 + l1, ip_ni_table)


# 测试

# 密钥key、明文p、各个置换、S盒
#key = "1010000010"
p10_table = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
p8_table = (6, 3, 7, 4, 8, 5, 10, 9)
p4_table = (2, 4, 3, 1)
#p = "10110101"
ip_table = (2, 6, 3, 1, 4, 8, 5, 7)
ep_table = (4, 1, 2, 3, 2, 3, 4, 1)
ip_ni_table = (4, 1, 3, 5, 7, 2, 8, 6)
sbox0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 0, 2]
]

sbox1 = [
    [0, 1, 2, 3],
    [2, 3, 1, 0],
    [3, 0, 1, 2],
    [2, 1, 0, 3]
]


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
        self.setGeometry(600, 600, 400, 400)


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
        if len(p) == 1:
            ascll = ord(p.strip())
            binascll = tenTotwo(ascll)
            p = binascll
        else:
            p = p.strip()
        key = self.keyLineEdit.text()
        key = key.strip()
        # 生成子密钥 K1 和 K2
        k1, k2 = generate_key(key, p10_table, p8_table)
        # 对明文进行加密
        ciphertext = encrypt(p, k1, k2)
        self.cipherLineEdit.setText(ciphertext)
        # 对密文进行解密
        plaintext = decrypt(ciphertext, k1, k2)
        print('明文： ', p)
        print('密钥： ', key)
        print("子密钥k1：", k1)
        print("子密钥k2：", k2)
        print("密文：", ciphertext)
        print('解密后的明文：', plaintext)
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
        self.setGeometry(600, 600, 400, 400)


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
        k1, k2 = generate_key(key1, p10_table, p8_table)
        # 对密文进行解密
        p1 = p1.strip()
        plaintext1 = decrypt(p1, k1, k2)
        # 对明文进行加密
        ciphertext1 = encrypt(plaintext1, k1, k2)
        ascll = twototen(plaintext1)
        chr1 = chr(ascll)
        output = plaintext1 + '  ascall码对应字符为:' + chr1
        self.pLineEdit.setText(output)
        print('密文： ', p1)
        print('密钥： ', key1)
        print("子密钥k1：", k1)
        print("子密钥k2：", k2)
        print("明文：", plaintext1)
        print('加密后的密文：', ciphertext1)
        print('--------------------------------------------------------')

    def switch(self):
        self.switch_window2.emit()

    def switch1(self):
        self.switch_window3.emit()


# 解密ui
class pojieui(QWidget):
    switch_window3 = PyQt5.QtCore.pyqtSignal()
    switch_window4 = PyQt5.QtCore.pyqtSignal()
    def __init__(self):
        super(pojieui,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("破解")
        layout = QGridLayout()
        self.setGeometry(600, 600, 400, 400)


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
        for i in range(1024):
            key1 = tenTotwo(key, bit=10)
            k1, k2 = generate_key(key1, p10_table, p8_table)
            ciphertext = encrypt(p, k1, k2)
            if ciphertext == pw:
                self.pLineEdit.setText(key1)
                break
            else:
                key = key + 1

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
