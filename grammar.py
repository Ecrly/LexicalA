'''
啊...好累啊
今天一定要把语法分析写完
不然什么都做不完了
'''

import re
import pandas as pd
import numpy as np
from lexial import Parser
from setting import *

Letter = ''.join([chr(i) for i in range(97,123)])
Letter += Letter.upper()
Letter += "'" + "_"
'''
啊~我好困，现在把最近本的写完了
接下来要写一下C语言文法了
'''

# 文法的预处理，识别出emmmm...你懂得
def get_word(line, i):
    c = ''
    if line[i] in Letter:
        c += line[i]
        i += 1
        while i < len(line) and line[i] in Letter:
            c += line[i]
            i += 1
        return c, i
    elif line[i] in ' \n\t':
        c += line[i]
        i += 1
        while i < len(line) and line[i] in ' \n\t':
            c += line[i]
            i += 1
        if(i < len(line)):
            return get_word(line, i)
        else:
            return 1, -1
    # 判断推导符
    elif line[i: i + 2] == '->':
        i += 2
        return get_word(line, i)
    elif line[i: i + 2] == '++' or (line[i:i+2] == '--'):
        return line[i: i + 2], i + 2
    else:
        return line[i], i+1

# 计算First集
def Cfirst(VT, a, A, B, First, R):
    if (a in R) or (len(First[a])!=0):
        return
    R.append(a)
    wait = []
    for i in range(len(A)):
        if a == A[i]:
            # 如果右侧第一个是终结符，就把他加入First中
            if B[i][0] in VT and B[i][0] not in First[a]:
                First[a].append(B[i][0])
            # 否则等待计算他的Fist集
            else:
                wait.append(i)
    for i in wait:
        # 求B[i][0]的First
        Cfirst(VT, B[i][0], A, B, First, R)
        for b in First[B[i][0]]:
            if b not in First[a]:
                First[a].append(b)
        j = 0
        # 如果能推导出空符，需要把后面的First集加入
        while('$' in First[B[i][j]]):
            j += 1
            if(j > len(B[i])):
                break
            if(B[i][j] in VT and B[i][j] not in First[a]):
                First[a].append(B[i][j])
                break
            else:
                Cfirst(VT, B[i][j], A, B, First, R)
                for b in First[B[i][j]]:
                    if b not in First[a]:
                        First[a].append(b)
    R.remove(a)

# 计算Follow集
def Cfollow(VT, b, A, B, First, Follow, R):
    if ((b in R) or (len(Follow[b]) != 0 and Follow[b][0] != '#')):
        return
    R.append(b)
    wait=[]
    # 在'->'右边找b
    for i in range(len(B)):
        if(b in B[i]):
            J = []
            for j in range(len(B[i])):
                if B[i][j] == b:
                    J.append(j)
            # 判断b在右侧出现的位置
            for m in range(len(J)):
                # 如果出现在最后面，需要把响应A的Follow集加入
                if(J[m] == (len(B[i]) - 1)):
                    wait.append(A[i])
                # 否则需要看一下他右面第一个是否是终结符
                else:
                    k = J[m] + 1
                    # 如果是终结符，并且不再Follow集中，就把他扔进去
                    # 其实应该是把他的First集扔进去，但是终结符的First集中只有她自己
                    if(B[i][k] in VT):
                        if(B[i][k] not in Follow[b]):
                            Follow[b].append(B[i][k])
                    # 如果不是终结符，需要把他的First集中除了空都加进去
                    else:
                        for c in First[B[i][k]]:
                            if((c not in Follow[b]) and (c != '$')):
                                Follow[b].append(c)
                        # 如果能推导出空来
                        while('$' in First[B[i][k]]):
                            k += 1
                            if(k == len(B[i])):
                                wait.append(A[i])
                                break
                            if(B[i][k] in VT):
                                if(B[i][k] not in Follow[b]):
                                    Follow[b].append(B[i][k])
                                break
                            else:
                                for c in First[B[i][k]]:
                                    if ((c not in Follow[b]) and (c != '$')):
                                        Follow[b].append(c)

    # 把之前需要被加入Follow的非终结符计算一遍
    for i in wait:
        Cfollow(VT, i, A, B, First, Follow, R)
        for a in Follow[i]:
            if(a not in Follow[b]):
                Follow[b].append(a)
    R.remove(b)

# 计算Predict集以构造分析婊
def Cpredict(VT, A, B, First, Follow, P):
    # 这里是对'->'右边的进行分析，不要弄错咧~
    for i in range(len(B)):
        if(B[i][0] == '$'):
            P[i] = Follow[A[i]]
        elif B[i][0] in VT:
            P[i].append(B[i][0])
        else:
            if('$' not in First[B[i][0]]):
                for c in First[B[i][0]]:
                    P[i].append(c)
            else:
                for a in First[B[i][0]]:
                    if (a != '$'):
                        P[i].append(a)
                j = 0
                while('$' in First[B[i][j]]):
                    j += 1
                    if (j == len(B[i])):
                        for a in Follow[A[i]]:
                            if (a not in P[i]):
                                P[i].append(a)
                        break
                    if (B[i][j] in VT):
                        if (B[i][j] not in P[i]):
                            P[i].append(B[i][j])
                        break
                    for a in First[B[i][j]]:
                        if ((a != '$') and (a not in P[i])):
                            P[i].append(a)

# 构造分析婊
def Ctable(Predict, A, B):
    pass


f = open('c', 'r')
# 非终结符集合
VN = []
# 终结符
VT = []
# 存文法
P = []

# 文法的预处理（包括去空格，把|拆分成两行，识别‘->’等）
for line in f.readlines():
    p = []
    i = 0
    while(i < len(line)):
        a, i = get_word(line, i)
        if(a == '|'):
            P.append(p)
            a = p[0]
            p = []
            p.append(a)
        elif(i == -1):
            break
        else:
            p.append(a)
    P.append(p)

S = P[0][0]
A = []
B = []

# 筛选出非终结符到VN中
for i in range(len(P)):
    if P[i][0] not in VN:
        VN.append(P[i][0])
    A.append(P[i][0])
    B.append(P[i][1: len(P[i])])

# 筛选出终结符到VT中
for i in range(len(P)):
    for j in range(1, len(P[i])):
        if P[i][j] not in VN and P[i][j] not in VT:
            VT.append(P[i][j])
print("\n********************** 非终结符 ***************************\n")
print(VN)
print("\n********************** 终结符 ***************************\n")
print(VT)

First = {}
Follow = {}
Predict = []

# 求First集

for i in VN:
    First[i] = []

for i in VN:
    if len(First[i]) == 0:
        R = []
        Cfirst(VT, i, A, B, First, R)

print('\n********************** First ***************************\n')
print(First)

# 求Follow集

for i in VN:
    Follow[i] = []

Follow[S].append('#')

for i in VN:
    if len(Follow[i]) == 0 or i == S:
        R = []
        Cfollow(VT, i, A, B, First, Follow, R)
print('\n********************** Follow **************************\n')
print(Follow)

# 求Predict集
for i in A:
    Predict.append([])

# 构造分析婊
Cpredict(VT, A, B, First, Follow, Predict)
print(Predict)
VT.append('#')
VT.remove('$')

a = len(VN)
b = len(VT)
row = pd.Series(range(len(VN)), index=VN)
col = pd.Series(range(len(VT)), index=VT)
df = pd.DataFrame(index=VN, columns=VT)
i = np.zeros(a*b).reshape(a,b)
j = np.ones(a*b).reshape(a,b)
Table = (i-j).astype(int)
for i in range(len(Predict)):
    c = A[i]
    for d in Predict[i]:
        Table[row[c]][col[d]] = i
df = pd.DataFrame(Table,index = VN,columns = VT)


print('\n********************** 分析表 **************************\n')
print()
print(df)
for i in range(len(A)):
    print(i, "%s -> %s"% (A[i], B[i]))
with open("table.txt", 'w')as f:
    f.write(str(df))
    for i in range(len(A)):
        f.write(str(i) + " " + str(A[i])  + " -> " + str(B[i]) + '\n')


def analysis(a, b):
    # 分析过程
    Analysis = []
    Analysis.append('#')
    Analysis.append(S)
    # Input = ['i', '+', 'i', '*', 'i', '#']
    Input = ['INT', 'ID', '(', 'INT', 'ID', ')', '{','INT', 'ID', '=', 'DIGIT', ';' , 'CHAR', 'ID', '=' , 'CHARR', ';' , '}', '#']
    if a:
        a += '#'
        b += '#'
        Input = a
        Input_map = b
    Input.reverse()
    Input_map.reverse()

    i = 1
    j = len(Input) - 1
    step = 1
    while(1):
        if (i == -1 or j == -1):
            if (i == -1 and j == -1):
                print ("成功")
                break
            else :
                print ("语法分析错误")
                break
        print("第 %d 步：" % step)
        print("符号栈为：", Analysis)
        print("输入栈为：", Input)
        if(step > 400):
            break
        if Analysis[i] in VT:
            if(Analysis[i] == Input[j]):
                print("栈顶元素", Analysis[i], "匹配成功")
                Analysis.pop()
                Input.pop()
                i -= 1
                j -= 1
        else:
            c = Analysis.pop()
            i -= 1
            d = Input[j]
            if(df[d][c] == -1):
                print("第 %d 行语法分析错误!"% Input_map[j])
                break
            else:
                k = df[d][c]
                BO = B[k][:]
                b = " ".join(x for x in B[k])
                print("选用产生式：%s -> %s"% (A[k] ,b))
                BO.reverse()
                for m in BO:
                    if m != '$':
                        Analysis.append(m)
                        i += 1
        step += 1


parse = Parser()
with open(FILE, 'r', encoding='utf-8') as f:
    text = f.read()
Input, Input_map = parse.parser(text)
if Input == "wrong":
    print("词法分析错误")
else:
    print(Input)
    analysis(Input, Input_map)

