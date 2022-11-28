import random
import math
import numpy as np
import matplotlib.pyplot as plt
# 学习了numpy库，从之前的append到现在的np，整个程序好多地方需要更改,不过使编程思路更加明确了，不会出现超过等一些未知情况，减少错误
# 速度的比率
w  = 1             #速度权重应该随着迭代的增加不断较少   w = w - ( w_max - w_min )*(run/run_max)
c1 = 2             #同级中最优解方向的速度
c2 = 2             #同一个鸟最好的方向的速度
iter_max = 1000 #最大寻找个数
N=10            #种群个数
pbest=[]            #粒子经历的位置
v_x = np.ones((iter_max,N),float)
v_y = np.ones((iter_max,N),float)            #两个自由度速度
def cal(n):   #函数计算  n为第几代
    global x,y,z
    for i in range(len(x[n])):
        z[n][i]=(math.sin(x[n][i]*y[n][i])*math.sin(x[n][i]*y[n][i]) + math.cos(y[n][i])*math.cos(y[n][i]*x[n][i]))     #发生浅层拷贝还是深层拷贝的问题

def start(N=10):    #得到初始种群和可行域
    top_x = random.uniform(-10,10)
    low_x = random.uniform(-10,top_x)
    top_y = random.uniform(-8,8)
    low_y = random.uniform(-8,top_y)
    x = np.ones((iter_max,N),float)
    y = np.ones((iter_max,N),float) 
                       # x = [[] for i in range(iter_max)]   #每一个x的速度,这里0应该删除了，写了是方便测试的时候检测错误
                       # y = [[] for i in range(iter_max)]   #每一个y的速度
    for i in range(N):
        x[0][i]=random.uniform(low_x,top_x)
        y[0][i]=random.uniform(low_y,top_y)
    print('x的可行域为：(',low_x,',',top_x,')')
    print('y的可行域为：(',low_y,',',top_y,')')
    return low_x,top_x,low_y,top_y,x,y

def Pbest(n):  #这里传入的是总体的解值，关于解值的保存留着主函数去做
    global z
    max_jiaobiao = 1
    z_max = z[n]
    jiaobiao=np.linspace(1,1,len(z[0]))
    for i in range(len(z[0])):
        for ii in range(n):
            if z[ii][i]>z_max[i]:
                max_jiaobiao = ii
                z_max[i] = z[ii][i]
        jiaobiao[i] = max_jiaobiao
    return jiaobiao   #放回每一个第几代是最大值的下标的一维列表

def Gbest(n):  #这里传入最新一代的解  这里是一维，上一个函数为二维
    global z
    z_max = z[n][0]
    c = 1
    for i in range(len(z[n])):
        if z_max <z[n][i] :
            z_max = z[n][i]
            c = i
    return c   #返回最大值的下标

def boundary(n): #判断是否超过可行域  输入的x,y为这一代的值
    global x,y,low_x,top_x,low_y,top_y
    for i in range(len(x[n])):
        if x[n][i]>top_x :
            x[n][i] = top_x
        if x[n][i]<low_x :
            x[n][i] = low_x                        #   应该可以简化一点点，毕竟len(x)=len(y),为了少犯错多写了一些
    for i in range(len(x[n])):
        if y[n][i]>top_y :
            y[n][i] = top_y
        if y[n][i]<low_y :
            y[n][i] = low_y

global low_x,top_x,low_y,top_y,x,y,z
low_x,top_x,low_y,top_y,x,y=start(N)
z = np.ones((iter_max,N),float)
for i in range(iter_max):  # i为第几次寻找
    boundary(i)
    cal(i)       
    jiaobiao = Pbest(i)
    gbest = Gbest(i)
    DX=np.linspace(1,1,len(z[0]))
    DY=np.linspace(1,1,len(z[0]))
    for ii in range(N):   #ii为第一个到第N个的，同一次的飞行
        DX[ii] = w*v_x[i][ii]+c1*random.uniform(0,1)*(x[int(jiaobiao[ii])][ii]-x[i][ii])+c2*random.uniform(0,1)*(x[i][gbest]-x[i][ii])
        DY[ii] = w*v_y[i][ii]+c1*random.uniform(0,1)*(y[int(jiaobiao[ii])][ii]-y[i][ii])+c2*random.uniform(0,1)*(y[i][gbest]-y[i][ii])
    if i<iter_max-1 :
        v_x[i+1] = DX
        v_y[i+1] = DY
        x[i+1] = x[i] +DX*0.1
        y[i+1] = y[i] +DY*0.1
    boundary(i)
    w = 1 - math.sin((iter_max * 2) / ((iter_max+1) * math .pi))
for i in range(N):
    print('第',i+1,'个粒子在第',int(jiaobiao[i])+1,'次找到了最大值z=',z[int(jiaobiao[i])][i])
    print('坐标为(',x[int(jiaobiao[i])][i],',',y[int(jiaobiao[i])][i],')')
plt.figure()
plt.plot(x,y)
plt.xlabel('x')
plt.ylabel('y')
x_ticks = np.linspace(low_x,top_x,6)
plt.xticks(x_ticks)
y_ticks = np.linspace(low_y,top_y,6)
plt.yticks(y_ticks)
plt.xticks(x_ticks,[r'$x_min$',x_ticks[1],x_ticks[2],x_ticks[3],x_ticks[4],r'$x_max$'])
plt.yticks(y_ticks,[r'$y_min$',y_ticks[1],y_ticks[2],y_ticks[3],y_ticks[4],r'$y_max$'])
plt.show()
