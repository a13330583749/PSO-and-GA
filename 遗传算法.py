from decimal import Decimal
import math
import random
import string
import re
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(suppress = True)
N = 50    #种群的规模
max = 500 #进化的最大代数
p1 = 0.9  #交叉概率
p2 = 0.1  #变异概率
# x为种群的列表
def bTod(n, pre=20): #把一个带小数的二进制数n转换成十进制
    if n<0 :
        flag0 = -1
    else:
        flag0 = 1
    n=abs(n)
    string_number1 = str(n) #number1 表示二进制数，number2表示十进制数
    for i in range(len(string_number1)):
            if string_number1[i]=='e':
                string_number1='{:.21f}'.format(n)   #网上找的format，差不多就是这样，把n搞错了
                break
    decimal = 0  #小数部分化成二进制后的值
    flag = False   
    for i in string_number1: #判断是否含小数部分
        if i == '.' :
            flag = True
            break
    if flag  : #若二进制数含有小数部分
        string_integer, string_decimal = string_number1.split('.') #分离整数部分和小数部分
        for i in range(len(string_decimal)):
            if string_decimal[i]=='e':
                break
            decimal += 2**(-i-1)*int(string_decimal[i])  #小数部分化成二进制
        number2 = int(str(int(string_integer, 2))) + decimal
        return round(number2, pre)*flag0
    else   : #若二进制数只有整数部分
        return (int(string_number1, 2))*flag0   #若只有整数部分 直接一行代码二进制转十进制
    
def dTob(n, pre=4): # 把十进制的浮点数n转换成二进制
    if n<0 :
        flag0 = -1
    else:
        flag0 = 1
    n=abs(n)
    string_number1 = str(n) #number1 表示十进制数，number2表示二进制数
    flag = False   
    for i in string_number1: #判断是否含小数部分
        if i == '.':
            flag = True
            break
    if flag:
        string_integer, string_decimal = string_number1.split('.') #分离整数部分和小数部分
        integer = int(string_integer)
        decimal = Decimal(str(n)) - integer
        l1 = [0,1]
        l2 = []
        decimal_convert = ""
        while True:  
           if integer == 0: break
           x,y = divmod(integer, 2)  #x为商，y为余数 
           l2.append(y)
           integer = x
        string_integer = ''.join([str(j) for j in l2[::-1]])  #整数部分转换成二进制 
        i = 0  
        while decimal != 0 and i < pre:  
            result = int(decimal * 2)  
            decimal = decimal * 2 - result  
            decimal_convert = decimal_convert + str(result)
            if (decimal_convert !=1 or decimal_convert !=0) and i==0:
                decimal_convert='1'
            i = i + 1
            decimal_convert_list = list(decimal_convert)
            if '-' in decimal_convert_list :
                decimal_convert_list.remove('-')
            decimal_convert = str(''.join(decimal_convert_list))
        string_number2 = string_integer + '.' + decimal_convert
        return float(float(string_number2))*flag0
    else: #若十进制只有整数部分
        l1 = [0,1]
        l2 = []
        while True:  
           if n == 0: break
           x,y = divmod(n, 2)  #x为商，y为余数 
           l2.append(y)
           n = x
        string_number = ''.join([str(j) for j in l2[::-1]])  
        return (int(string_number))*flag0

def cal(x):  #计算目标函数
    y=[]
    for i in range(len(x)):
        y.append( (math.cos(3*x[i]) + math.sin(x[i]**2))**(-2) )
    return y

def du(y):       #轮盘赌(传入解空间的十进制值）
    sum1 = sum2 = flag1 = flag2 = 0
    p=[]
    for i in range(len(y)):
        sum1 += y[i]
    for i in range(len(y)):
        sum2 += y[i]
        p.append((y[i]+sum2)/sum1)
    parent1 = random.random()
    parent2 = random.random()  #父代的概率值
    for i in range(len(y)):
        if parent1 >= p[i]:
            flag1 = i
        if parent2 >= p[i]:
            flag2 = i
    return flag1,flag2    #传出的是以选出来的两个父代的角标

def start():     #初始化
    up = random.uniform(-10,10)
    low = random.uniform(-10,up)
    print('x的可行域为：(',low,',',up,')')
    blanking = (up - low)/(N+1)
    x=[]
    for i in range(N):
        x.append(low+(i+1)*blanking)
    return up,low,x
    
def jiaocha(parent1,parent2):   #对两个父代进行交叉,要求输入二进制码
    p1_str = str(parent1)
    p2_str = str(parent2)       #想要在这里偷懒，结果交叉出来了两个小数点
    p1_list = list(p1_str)
    p2_list = list(p2_str)
    a_p1 = p1_list.index('.')
    a_p2 = p2_list.index('.')
    son1=[]
    son2=[]
    son1=p1_list[0:a_p1]
    son2=p2_list[0:a_p2]        #此处代码存在不严谨的地方，交叉不完全    编程思路还是不清晰   会不会出现换过来又换过去的情况
    for i in range(a_p1+1,int((len(p1_list)-a_p1)/3)):
        son1.append(p2_list[i])
        son2.append(p1_list[i])
    for i in range(int((len(p1_list)-a_p1)/3) , int((len(p1_list)-a_p1)*2/3) ):
        son1.append(p1_list[i])
    for i in range(int((len(p2_list)-a_p2)/3) , int((len(p2_list)-a_p2)*2/3) ):
        son2.append(p2_list[i])
    for i in range(int((len(p1_list)-a_p1)*2/3) ,int(len(p1_list)-a_p1)):
        if i>=len(p1_list) or i>=len(p2_list):
            break
        son1.append(p2_list[i])
        son2.append(p1_list[i])
    for i in range(len(son1)):
        if son1[i] == '.':
            son1[i] = '1'
    for i in range(len(son2)):
        if son2[i] == '.':
            son2[i] = '0'
    son1.insert(a_p1,'.')
    son2.insert(a_p2,'.')
    return float(''.join(son1)),float(''.join(son2))  #返回值为浮点型的二进制数

def bianyi(p1,p2):    #对两个父代进行变异,要求输入二进制码   变异不完全
    p1_str = str(p1)
    p2_str = str(p2)
    p1_list = list(p1_str)
    p2_list = list(p2_str)
    for i in range(3):
        change1=random.randint(0,len(p1_list)-1)
        if p1_list[change1] == '1':
            p1_list[change1] = '0'
        elif p1_list[change1] == '0':
            p1_list[change1] = '1'
    for i in range(3):
        change2=random.randint(0,len(p2_list)-1)
        if p2_list[change2] == '1':
            p2_list[change2] = '0'
        elif p2_list[change2] == '0':
            p2_list[change2] = '1'
    return float(''.join(p1_list)),float(''.join(p2_list))   #返回值为浮点型的二进制数

def jingying(y):      #得到最好的N组解的下标
    yy=sorted(y)     #学到新的函数
    yyy=yy[-1:-(N+1)]    #修改
    best=[] #最好的脚本存储
    for i in range(N):
        for ii in range(len(y)):
            if yy[i] == y[ii]:
                best.append(ii)
                break   # 修改的这些
    return best

def boundary(most_x,up,low):   # 可行域的判断
    for i in range(len(most_x)):
        if most_x[i]>up:
            most_x[i] = up
        elif most_x[i]<low :
            most_x[i] = low
    return most_x    

up,low,x=start()   #得到的x是等间隔分开的
for c in range(max):
    x_binary=[]
    most=[] #子代和父代的种群集合
    best_x=[] #新的一代
    son=[]   #子代x的值
    y=cal(x)
    for i in range(N):   # 得到x的二进制码
        x_binary.append(dTob(x[i],21))
    for i in range(N):   #产生2N个子代
        flag1,flag2=du(y)   #父代的两个角标值
        P=random.random() #根据概率判断发生交叉还是变异
        if P<=p1 :        #交叉
            son1_binary,son2_binary = jiaocha(x_binary[flag1],x_binary[flag2]) 
        else  :             #变异
            son1_binary,son2_binary = bianyi(x_binary[flag1],x_binary[flag2])
        son.append(bTod(son1_binary))
        son.append(bTod(son2_binary))   #将十进制的子代x存入列表中
    most_x = x + son
    most_x = boundary(most_x,up,low) # 是否出可行域
    most = cal(most_x)   #y为父代的解值       有一些是带e的，有一些没有
    best=jingying(most)  #得到最高的排序下标    感觉好奇怪，是什么的下标
    for i in range(N):
        best_x.append(most_x[best[i]])
    x = best_x
    best_y = cal(x)     
    #print(best)    #收敛速度过快   输出为第一高的值
plt.figure
plt.plot(best_y)
plt.show()
#交叉和变异对于解的影响太小，所以收敛不到想要的极值点，或者是速度太快
