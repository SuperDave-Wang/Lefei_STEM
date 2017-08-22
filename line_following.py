# -*- coding: utf-8 -*-
import  RPi.GPIO as gpio
import  time
import  sys

def init():  #定义初始化GPIO引脚的函数
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(12,gpio.OUT)
    gpio.setup(16,gpio.OUT)
    gpio.setup(18,gpio.OUT)
    gpio.setup(22,gpio.OUT)
    gpio.setup(13,gpio.OUT)
    gpio.setup(15,gpio.IN)
    gpio.setup(33,gpio.IN)
    gpio.setup(35,gpio.IN)
    gpio.setup(36,gpio.IN)
    gpio.setup(37,gpio.IN)
    gpio.setup(38,gpio.OUT)
    gpio.setup(40,gpio.OUT)
    gpio.output(38, True)
    gpio.output(40, True)
##    left=gpio.PWM(38,20)
##    right=gpio.PWM(40,20)
##    left.start(100)
##    right.start(100)

def forward(t):  #定义前进的函数
    init()  #初始化引脚
    gpio.output (12, True)  #让右电机逆转
    gpio.output (16, False)  #让右电机不顺转
    gpio.output (22, True)  #让左电机顺转
    gpio.output (18, False)  #让左电机不逆转
    time.sleep(t)  #等待时间t
    gpio.cleanup()  #清除引脚的输出

def backward(t):  #定义后退的函数
    init()  #初始化引脚
    gpio.output (12, False)  #让右电机不逆转
    gpio.output (16, True)  #让右电机顺转
    gpio.output (22, False)  #让左电机不顺转
    gpio.output (18, True)  #让左电机逆转
    gpio.setup(7,gpio.OUT)  
    gpio.output(7,True)
    time.sleep(t)  #等待时间t
    gpio.cleanup()  #清除引脚的输出

def turn_right(t):  #定义右转的函数
    init()  #初始化引脚
    gpio.output (12, False)  #让右电机不逆转
    gpio.output (16, False)  #让右电机不顺转
    gpio.output (22, True)  #让左电机 顺转
    gpio.output (18, False)  #让左电机不逆转
    time.sleep(t)  #等待时间t
    gpio.cleanup()  #清除引脚的输出

def turn_left(t):  #定义左转的函数
    init()  #初始化引脚
    gpio.output (12, True)  #让左电机逆转
    gpio.output (16, False)  #让左电机不顺转
    gpio.output (22, False)  #让右电机不顺转
    gpio.output (18, False)  #让右电机不逆转
    time.sleep(t)  #等待时间t
    gpio.cleanup()  #清除引脚的输出


def pivot_turn_right(t):  #定义右转的函数
    init()  #初始化引脚
    gpio.output (12, False)  #让右电机不逆转
    gpio.output (16, True)  #让右电机不顺转
    gpio.output (22, True)  #让左电机 顺转
    gpio.output (18, False)  #让左电机不逆转
    time.sleep(t)  #等待时间t
    gpio.cleanup()  #清除引脚的输出

def pivot_turn_left(t):  #定义左转的函数
    init()  #初始化引脚
    gpio.output (12, True)  #让左电机逆转
    gpio.output (16, False)  #让左电机不顺转
    gpio.output (22, False)  #让右电机不顺转
    gpio.output (18, True)  #让右电机不逆转
    time.sleep(t)  #等待时间t
    gpio.cleanup()  #清除引脚的输出
    
def  stop(t):
    init()
    gpio.output (12, False)  #让左电机不逆转
    gpio.output (16, False)  #让左电机不顺转
    gpio.output (22, False)  #让右电机不顺转
    gpio.output (18, False)  #让右电机不逆转
    time.sleep(t)  #等待时间t
    gpio.cleanup()  #清除引脚的输出

def line_following():
    for i in range(0, 10000):
        init()
        if gpio.input(37) == False and gpio.input(36) == False and gpio.input(35) == False and gpio.input(33) == False:
            forward(0.001)
        elif gpio.input(37) == True or gpio.input(36) == True or gpio.input(35)==True or gpio.input(33)==True : 
            stop(1)

        init()  
        while gpio.input(36) == True: 
            pivot_turn_right(0.1)
            init()
            if gpio.input(36) == False:
                break       
        while gpio.input(35)==True: 
            pivot_turn_right(0.2)
            init()
            if gpio.input(35) == False:
                break
        while gpio.input(37)==True:
            pivot_turn_left(0.1)
            init()
            if gpio.input(37) == False:
                break        
        while gpio.input(33) == True: 
            pivot_turn_left(0.2)
            init()
            if gpio.input(33) == False:
                break
    init()
    stop(3)

line_following()

    



