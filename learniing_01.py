## 1. 控制 LED 開關（數位輸出）
'''
from machine import Pin
import time

# 初始化GPIO 1腳位
led = Pin(1, Pin.OUT)

# 開啟 LED
led.value(1)
time.sleep(1)

# 關閉 LED
led.value(0)
time.sleep(1)
'''

```
## 2. LED 閃爍程式
```
'''
from machine import Pin
import time

led = Pin(1, Pin.OUT)

while True:
    led.value(1)  # 開啟 LED
    time.sleep(1)
    led.value(0)  # 關閉 LED
    time.sleep(1)
'''

```
##  3. 使用 PWM 控制 LED 亮度
'''
from machine import Pin, PWM
import time

led = PWM(1, freq=1000)  # GPIO 2 設為 PWM，頻率 1kHz

for _ in range(2):
    for duty in range(0, 65536, 1024):  # 逐漸變亮
        led.duty_u16(duty)  # 0~65535
        time.sleep(0.02)
    for duty in range(65535, -1, -1024):  # 逐漸變暗
        led.duty_u16(duty)
        time.sleep(0.02)
print("led off")

'''
## 4. 操作多個led
'''
from machine import Pin,PWM
import time

# 初始化 led1
led1 = Pin(1,Pin.OUT)
# 初始化 led2
led2 = Pin(2,Pin.OUT)
# 初始化 led3
led3 = Pin(3,Pin.OUT)

led1.value(1)
led2.value(1)
led3.value(1)
time.sleep(3)

led1.value(0)
led2.value(0)
led3.value(0)

'''

## 5. 多顆led同時亮(陣列法)
'''
from machine import Pin
import time

# 初始化 led
pos = [1,2,3]
leds =  [ Pin(th,Pin.OUT) for th in pos ]

for i in leds:
    i.value(1)
time.sleep(3)
for i in leds:    
    i.value(0)
    
'''
