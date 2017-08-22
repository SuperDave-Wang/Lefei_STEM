 # -*- coding: utf-8 -*-
import  RPi.GPIO as gpio    #导入所有模块
import  time
import  sys
import  pygame
import  random
import os
import atexit



pygame.init()  #pygame窗口初始化
screen = pygame.display.set_mode([320,240])
background = pygame.Surface(screen.get_size())
background.fill ([0,0,0])
delay = 100
interval = 50
pygame.key.set_repeat(delay, interval)

def init():  #定义初始化GPIO引脚的函数
    gpio.setmode(gpio.BOARD)
    gpio.setup(12,gpio.OUT)
    gpio.setup(16,gpio.OUT)
    gpio.setup(18,gpio.OUT)
    gpio.setup(22,gpio.OUT)
    gpio.setup(13,gpio.OUT)
    gpio.setup(38,gpio.OUT)
    gpio.setup(40,gpio.OUT)
    gpio.output (38, True)
    gpio.output (40, True)
    gpio.setup(15,gpio.IN)
    gpio.setup(33,gpio.IN)
    gpio.setup(35,gpio.IN)
    gpio.setup(36,gpio.IN)
    gpio.setup(37,gpio.IN)
    gpio.setwarnings(False)

def  stop(t):
    init()
    gpio.output (12, False)  #让左电机不逆转
    gpio.output (16, False)  #让左电机不顺转
    gpio.output (22, False)  #让右电机不顺转
    gpio.output (18, False)  #让右电机不逆转
    time.sleep(t)  #等待时间t
    gpio.cleanup()  #清除引脚的输出

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

def output_ultrasonic_wave():
    init()
    gpio.output(13,True)
    time.sleep(0.00001)
    gpio.output(13,False)
    while gpio.input(15) == False:
        pass
    t1 = time.time()
    gpio.cleanup()
    return t1

def distance():
    init()
    gpio.setwarnings(False)   
    t1 = output_ultrasonic_wave()
    init()
    gpio.setwarnings(False)
    while gpio.input(15) == True:
        pass
    t2 = time.time()
    t  = t2 - t1
    distance = t * 34000 / 2
    gpio.cleanup()
    return distance

def auto_drive():
    v = 0
    while v < 100:
        forward(0.05)
        d = distance()
        if  d < 40:
            stop(1)
            backward(1)
            turn = random.randint(1, 2)
            if turn == 1:
                turn_left(1.5)
            else:
                turn_right(1.5)
        gpio.cleanup()
        v += 1

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

def steer(j):
    for i in range(0,j):
        atexit.register(gpio.cleanup)
        gpio.setwarnings(False)   
        gpio.setmode(gpio.BOARD)  
        gpio.setup(31, gpio.OUT)
        gpio.output(31, False)
        p = gpio.PWM(31, 50) #50HZ  
        p.start(2.5) ##p.start(2.5) # initial position
        p.ChangeDutyCycle(6.5) #turn left for 80 degrees
        time.sleep(0.2)
        atexit.register(gpio.cleanup)
        p.ChangeDutyCycle(2.5) #turn back
        time.sleep(0.2)
        atexit.register(gpio.cleanup)
        gpio.cleanup()

def main():
    gpio.setwarnings(False)
    for event in pygame.event.get():  #当接收到一个事件时
        if event.type == pygame.QUIT:  #如果这个事件是按下叉叉
            sys.exit()  #退出程序
        elif event.type == pygame.KEYDOWN:  #如果这个事件是按下某个按键
            if event.key ==pygame.K_w:  #如果这个按键是W
                forward(0.05)  #前进0.05秒
            elif event.key ==pygame.K_s:  #如果这个按键是S
                backward(0.05)  #后退0.05秒
            elif event.key ==pygame.K_a:  #如果这个按键是A
                pivot_turn_left(0.05)  #左转0.05秒
            elif event.key ==pygame.K_d:  #如果这个按键是D
                pivot_turn_right(0.05)  #右转0.05秒
            elif event.key ==pygame.K_b:
                stop(1)
                break
            elif event.key ==pygame.K_o:
                auto_drive()
            elif event.key ==pygame.K_l:
                line_following()
            elif event.key ==pygame.K_h:
                steer(1)
            
while True:  #创建一个无限循环
    main()
                   

                

