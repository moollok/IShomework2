# S盒
s = [[9, 4, 10, 11],
     [13, 1, 8, 5],
     [6, 2, 0, 3],
     [12, 14, 15, 7]]
# 逆s盒
nis = [[10, 5, 9, 11],
       [1, 7, 8, 15],
       [6, 0, 2, 3],
       [12, 4, 13, 14]]
# 替换表
Replace = [[0, 0, 0, 0], [0, 0, 0, 1],
           [0, 0, 1, 0], [0, 0, 1, 1],
           [0, 1, 0, 0], [0, 1, 0, 1],
           [0, 1, 1, 0], [0, 1, 1, 1],
           [1, 0, 0, 0], [1, 0, 0, 1],
           [1, 0, 1, 0], [1, 0, 1, 1],
           [1, 1, 0, 0], [1, 1, 0, 1],
           [1, 1, 1, 0], [1, 1, 1, 1]]

# 轮常数
rcon1 = [1, 0, 0, 0, 0, 0, 0, 0]
rcon2 = [0, 0, 1, 1, 0, 0, 0, 0]


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


def XR_8(a, b):
    # a、b 分别是两个长度为 8 的数组，返回一个长度也为 8 的数组
    t = [0] * 8  # 结果数组
    for i in range(8):
        t[i] = a[i] ^ b[i]
    return t


# 字节替换
def SubBytes(temp):
    # temp 是一个长度为8的数组，进行S盒替换
    # 先计算出需要进行S盒替换的四位二进制数
    t1 = 2 * temp[0] + temp[1]
    t2 = 2 * temp[2] + temp[3]
    t3 = 2 * temp[4] + temp[5]
    t4 = 2 * temp[6] + temp[7]
    # 进行 S 盒替换
    num1 = s[t1][t2]
    num2 = s[t3][t4]
    # 将替换后的结果按四位四位赋值给temp
    for i in range(4):
        temp[i] = Replace[num1][i]
    for i in range(4):
        temp[i + 4] = Replace[num2][i]


def niSubBytes(temp):
    # temp 是一个长度为8的数组，进行S盒替换
    # 先计算出需要进行S盒替换的四位二进制数
    t1 = 2 * temp[0] + temp[1]
    t2 = 2 * temp[2] + temp[3]
    t3 = 2 * temp[4] + temp[5]
    t4 = 2 * temp[6] + temp[7]
    # 进行 S 盒替换
    num1 = nis[t1][t2]
    num2 = nis[t3][t4]
    # 将替换后的结果按四位四位赋值给temp
    for i in range(4):
        temp[i] = Replace[num1][i]
    for i in range(4):
        temp[i + 4] = Replace[num2][i]


# g函数
def g(temp, rcon):
    # temp 是一个长度为8的数组，rcon是轮常数
    t = temp.copy()  # temp是密钥，不能改动，复制一个新的
    # 进行循环左移
    for i in range(4):
        tt = t[i + 4]
        t[i + 4] = t[i]
        t[i] = tt
    # 进行 S 盒替换
    SubBytes(t)
    # 进行轮常数异或
    return XR_8(t, rcon)


def nig(temp, rcon):
    # temp 是一个长度为8的数组，rcon是轮常数
    t = temp.copy()  # temp是密钥，不能改动，复制一个新的
    # 进行循环左移
    for i in range(4):
        tt = t[i + 4]
        t[i + 4] = t[i]
        t[i] = tt
    # 进行 S 盒替换
    niSubBytes(t)
    # 进行轮常数异或
    return XR_8(t, rcon)


# 轮密钥加
def AddRoundKey(mingwen, key):
    for i in range(2):
        for j in range(8):
            mingwen[i][j] ^= key[i][j]


# 行变换
def ShiftRows(temp):
    # 第一字节的右半部分和第二字节的右半部分进行替换
    for i in range(4, 8):
        t = temp[0][i]
        temp[0][i] = temp[1][i]
        temp[1][i] = t


# 4位的异或
def OR_4(a, b):
    # a、b 分别是两个长度为 4 的数组，返回一个长度也为 4 的数组
    t = [0] * 4  # 结果数组
    for i in range(4):
        t[i] = a[i] ^ b[i]
    return t


def x_fx(f, a):
    # 进行有限域上的多项式除法运算，用于求解一个元素的逆元
    if a[0] == 0:
        for i in range(3):  # 定义一个长度为4的数组f表示一个3次多项式
            f[i] = a[i + 1]
    else:
        f[1] = a[2]
        f[2] = 0 if a[3] == 1 else 1
        f[3] = 1


def multiply(a, b):
    # 在有限域 GF(2^4) 上的多项式乘法运算
    # 记录下f^n
    f = [0] * 4
    x_fx(f, a)
    f2 = [0] * 4
    x_fx(f2, f)
    f3 = [0] * 4
    x_fx(f3, f2)
    # 现在需要根据多项式a和b开始异或
    result = [0] * 4  # 储存结果的系数
    if b[0] == 1:
        for i in range(4):
            result[i] ^= f3[i]
    if b[1] == 1:
        for i in range(4):
            result[i] ^= f2[i]
    if b[2] == 1:
        for i in range(4):
            result[i] ^= f[i]
    if b[3] == 1:
        for i in range(4):
            result[i] ^= a[i]
    return result


# 列混淆
def MixColumns(mingwen):
    rule = [0, 1, 0, 0]
    m00 = mingwen[0][:4]
    m10 = mingwen[0][4:]
    m01 = mingwen[1][:4]
    m11 = mingwen[1][4:]

    n00 = OR_4(m00, multiply(rule, m10))  # 乘法结果是1011
    n10 = OR_4(multiply(rule, m00), m10)  # 0101
    n01 = OR_4(m01, multiply(rule, m11))  # 0100
    n11 = OR_4(multiply(rule, m01), m11)  # 0010

    mingwen[0][:4] = n00
    mingwen[0][4:] = n10
    mingwen[1][:4] = n01
    mingwen[1][4:] = n11


# 逆列混淆
def niMixColumns(mingwen):
    rule = [1, 0, 0, 1]
    rule2 = [0, 0, 1, 0]
    m00 = mingwen[0][:4]
    m10 = mingwen[0][4:]
    m01 = mingwen[1][:4]
    m11 = mingwen[1][4:]

    n00 = OR_4(multiply(rule, m00), multiply(rule2, m10))  # 乘法结果是1011
    n10 = OR_4(multiply(rule2, m00), multiply(rule, m10))  # 0101
    n01 = OR_4(multiply(rule, m01), multiply(rule2, m11))  # 0100
    n11 = OR_4(multiply(rule2, m01), multiply(rule, m11))  # 0010

    mingwen[0][:4] = n00
    mingwen[0][4:] = n10
    mingwen[1][:4] = n01
    mingwen[1][4:] = n11


def jiami(mingwen_str, key_str):
    mingwen = [[int(mingwen_str[i * 8 + j]) for j in range(8)] for i in range(2)]
    key = [[int(key_str[i * 8 + j]) for j in range(8)] for i in range(2)]
    # print('明文', mingwen)
    # print('key', key)

    # 密钥扩展算法，由于只有三轮加密，第一轮只使用了原始key
    key1 = [[0] * 8 for _ in range(2)]
    key2 = [[0] * 8 for _ in range(2)]
    key1[0] = XR_8(key[0], g(key[1], rcon1))
    key1[1] = XR_8(key1[0], key[1])
    key2[0] = XR_8(key1[0], g(key1[1], rcon2))
    key2[1] = XR_8(key2[0], key1[1])

    # 第零轮
    # 轮密钥加
    AddRoundKey(mingwen, key)

    # 第一轮
    # 明文半字节代替
    SubBytes(mingwen[0])
    SubBytes(mingwen[1])
    # 明文的行移位
    ShiftRows(mingwen)
    # 明文的列混淆
    MixColumns(mingwen)
    # 明文的轮密钥加
    AddRoundKey(mingwen, key1)

    # 第二轮
    # 明文半字节代替
    SubBytes(mingwen[0])
    SubBytes(mingwen[1])
    # 明文的行移位
    ShiftRows(mingwen)
    # 明文的轮密钥加
    AddRoundKey(mingwen, key2)

    output = ''
    # 输出结果
    # print("密文为：")
    for i in range(2):
        for j in range(8):
            # print(mingwen[i][j], end=' ')
            output += str(mingwen[i][j])
    return output


def jiemi(miwen_str, key_str):
    miwen = [[int(miwen_str[i * 8 + j]) for j in range(8)] for i in range(2)]
    key = [[int(key_str[i * 8 + j]) for j in range(8)] for i in range(2)]
    # print('密文', miwen)
    # print('key', key)

    # 密钥扩展算法，由于只有三轮加密，第一轮只使用了原始key
    key1 = [[0] * 8 for _ in range(2)]
    key2 = [[0] * 8 for _ in range(2)]
    key1[0] = XR_8(key[0], g(key[1], rcon1))
    key1[1] = XR_8(key1[0], key[1])
    key2[0] = XR_8(key1[0], g(key1[1], rcon2))
    key2[1] = XR_8(key2[0], key1[1])

    # 第零轮
    # 轮密钥加
    AddRoundKey(miwen, key2)
    ShiftRows(miwen)
    niSubBytes(miwen[1])
    niSubBytes(miwen[0])
    AddRoundKey(miwen, key1)
    niMixColumns(miwen)
    ShiftRows(miwen)
    niSubBytes(miwen[1])
    niSubBytes(miwen[0])
    AddRoundKey(miwen, key)
    # 输出结果
    output = ''
    # print("明文为：")
    for i in range(2):
        for j in range(8):
            # print(miwen[i][j], end=' ')
            output += str(miwen[i][j])
    return output


def pojie(mingwen, miwen):
    output = ''
    key = 0
    for i in range(65536):
        key1 = tenTotwo(key, bit=16)
        ciphertext = jiami(mingwen, key1)
        if ciphertext == miwen:
            output += key1 + ' '
            key = key + 1
        else:
            key = key + 1
    print('密钥有', output)
    return output


if __name__ == "__main__":
    mingwen_str = "0110111101101011"
    key_str = "1010011100111011"
    miwen_str = "0000011100111000"
    a = jiami('0110111101101011', '1010011100111011')
    b = jiemi(miwen_str, key_str)
    c = pojie(mingwen_str, miwen_str)
    print(a)
    print(b)
