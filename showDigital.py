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

# 引脚对应的GPIO口
#          0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12
gpioPin = [0, 15,16,18,29,31,32,33,35,36,37,38,40]

# 第一个数字使用12号引脚
commonNegativePins = [12,9,8,6]
# 数字对应数码管符号
numberToChars = ['abcdef','bc','abged','abgcd','bcfg','afgcd','acdefg','abc','abcdefg','abcdfg']
# 数码管上字符对应的引脚
charPinMap = \
{
    'e':1,
    'd':2,
    'c':4,
    'g':5,
    'b':7,
    'f':10,
    'a':11,
    'dp':3
}

def clear():
    for pin in range(1,13):
        gpio = gpioPin[pin]
        if pin not in commonNegativePins:
            GPIO.output(gpio, False)
        else:
            # 避免闪烁，在显示数字前输出高电平，关闭显示
            GPIO.output(gpio, True)

# no表示显示第几个数字(1-4),num(0-9),showDotPoint是否显示点(True,False)
def showDigit(no, num, showDotPoint):
    if num <0 or num>9:
        return False

    clear()
    numChars = numberToChars[num]
    for i in range(len(numChars)):
        char = numChars[i]
        pin = charPinMap[char]
        GPIO.output(gpioPin[pin], True)
    if showDotPoint:
        pointPin = charPinMap['dp']
        GPIO.output(gpioPin[pointPin], True)

    # 输出低电平
    negativePin = commonNegativePins[no-1]
    GPIO.output(gpioPin[negativePin], False)

def init():
    for pin in range(1,13):
        gpio = gpioPin[pin]
        GPIO.setup(gpio, GPIO.OUT)
        GPIO.output(gpio, False)

init()
try:
    t = 0.005
    while True:
        showDigit(1, int(time.strftime("%H",time.localtime(time.time()))) / 10, False)
        time.sleep(t)
        showDigit(2, int(time.strftime("%H",time.localtime(time.time()))) % 10, True)
        time.sleep(t)
        showDigit(3, int(time.strftime("%M",time.localtime(time.time()))) / 10, False)
        time.sleep(t)
        showDigit(4, int(time.strftime("%M",time.localtime(time.time()))) % 10, False)
        time.sleep(t)

except KeyboardInterrupt:
    print "Stop"

GPIO.cleanup()
