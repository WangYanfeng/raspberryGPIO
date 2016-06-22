#!/user/bin/env python
# encoding: utf-8

import RPi.GPIO as GPIO
import time

print "\t __a__"
print "\t|     |"
print "\tf     b"
print "\t|__g__|"
print "\t|     |"
print "\te     c"
print "\t|__d__| .dp"

GPIO.setmode(GPIO.BOARD)

# 74HC595引脚对应的GPIO口
STCP = 35
SHCP = 36
DS = 40
OE= 38
#MR接vcc

# 第一个数字使用12号引脚
commonNegativePins = [12,9,8,6]

# 数码管上字符对应的引脚
"""
Q7 Q6 Q5 Q4 Q3 Q2 Q1 Q0
a  b  c  d  e  f  g  dp
    'e':1  -> Q3
    'd':2  -> Q4
    'c':4  -> Q5
    'g':5  -> Q1
    'b':7  -> Q6
    'f':10 -> Q2
    'a':11 -> Q7
    'dp':3 -> Q0
"""
# 数字对应数码管符号
#               0         1         2         3         4         5         6         7         8         9
#              'abcdef'  'bc'      'abged'   'abgcd'   'bcfg'    'afgcd'   'acdefg'  'abc'     'abcdefg' 'abcdfg'
numberToBit = ['1111110','0110000','1101101','1111001','0110011','1011011','1011111','1110010','1111111','1111011']

def clear():
    for pin in range(7):
        sendBitData(False)
        GPIO.output(STCP, True)
        GPIO.output(STCP, False)

# 传送数据
def sendBitData(data):
    GPIO.output(DS, data)
    # 74HC595会在这个上升沿将DS引脚上的数据存入移位寄存器D0
    # 制造一次移位寄存器时钟引脚的上升沿（先拉低电平再拉高电平）
    GPIO.output(SHCP, False)
    GPIO.output(SHCP, True)

# no表示显示第几个数字(1-4),num(0-9),showDotPoint是否显示点(True,False)
def showDigit(no, num, showDotPoint):
    if num <0 or num>9:
        return False

    # 移位D0 -> D1 ->
    for i in range(7):
        if numberToBit[num][i] == '1':
            print numberToBit[num][i]
            sendBitData(True)
        elif numberToBit[num][i] == '0':
            print numberToBit[num][i]
            sendBitData(False)
    if showDotPoint:
        print "dp True"
        sendBitData(True)
    else:
        print "dp False"
        sendBitData(False)
# 移位寄存器的8位数据全部传输完毕后，制造一次锁存器时钟引脚的上升沿（先拉低电平再拉高电平）
    # 74HC595会在这个上升沿将移位寄存器里的8位数据复制到8位的锁存器中（锁存器里原来的数据将被替换）
    # 到这里为止，这8位数据还只是被保存在锁存器里，并没有输出到数码管上。
    # 决定锁存器里的数据是否输出是由“输出使能端口”OE决定的。当OE设置为低电平时，锁存器里数据才会被输出到Q0-Q7这8个输出引脚上。
    # 在我的硬件连接里，OE直接连接在了GND上，总是保持低电平，所以移位寄存器的数据一旦通过时钟上升沿进入锁存器，也就相当于输出到LED上了。
    GPIO.output(STCP, True)
    GPIO.output(STCP, False)
    GPIO.output(OE, False)

def init():
    GPIO.setup(STCP, GPIO.OUT)
    GPIO.setup(SHCP, GPIO.OUT)
    GPIO.setup(DS, GPIO.OUT)
    GPIO.setup(OE, GPIO.OUT)
    GPIO.output(STCP, False)
    GPIO.output(SHCP, False)
    GPIO.output(OE, True)

init()
try:
    for i in range(10):
        showDigit(1, i, False)
        time.sleep(1)
        clear()


except KeyboardInterrupt:
    print "Stop"

GPIO.cleanup()

