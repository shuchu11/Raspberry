'''
目標 : 車子前進 , 後退 , 左轉 , 右轉功能。
材料 : ( 馬達組*2 , P.s.分AB[ =左右]兩側輪組 )小車 , 感測器。
限制 : AB以PWM驅動

模擬程式 :  
1. 前進 : AB start CL 
2. 後退 : AB start CCL 
3. 左轉 : B start CL  >  AB start CL  >  A start CL   >  AB start CL  
4. 右轉 : A start CL  >  AB start CL  >  B start CL   >  AB start CL  

'''
from machine import Pin, PWM , time_pulse_us
import time
# ...........................................................................................................
# 設定 PWM 發射腳位
wheel_left = PWM( 1 , freq = 1000)  # GPIO 1 設為 PWM，頻率 1kHz
wheel_right = PWM( 2 , freq = 1000 ) # GPIO 2 設為 PWM，頻率 1kHz

# 設定超音波感測器腳位
TRIG = Pin(3, Pin.OUT)
ECHO = Pin(4, Pin.IN)

# 設定 LED 腳位
LED_1 = Pin(5, Pin.OUT) # ON if the detected dist < 5 cm
LED_2 = PWM(6, freq = 1000 ) # ON if the detected dist  > 5 cm && < 10 cm 

# ...........................................................................................................
# LED PWM lighter
def LED_PWM_ON(led) :
    for duty in range(0, 65536, 2048):  # gradually becomes brighter
        led.duty_u16(duty)  # 0~65535
        time.sleep(0.01)
    
# LED PWM darker
def LED_PWM_OFF(led) :
    for duty in range(65535, -1, -2048):  # gradually becomes darker
        led.duty_u16(duty)
        time.sleep(0.01)
# The car moves forward
def FORWARD( wheel_A , wheel_B ):
    for duty in range(0, 65536, 1024):  # both wheels gradually speed up forward
        wheel_A.duty_u16(duty)  # 0~65535
        wheel_B.duty_u16(duty)  # 0~65535
        time.sleep(0.02)   # unit : s

# The car moves backward
def BACK( wheel_A , wheel_B ):
    for duty in range(65535 , -1, -1024):  # both wheels gradually speed up backward
        wheel_A.duty_u16(duty)  # 0~65535
        wheel_B.duty_u16(duty)  # 0~65535
        time.sleep(0.02)    

# The car turns left to avoid obstacles and then moves forward.
def LEFT( wheel_A , wheel_B ):
    for duty in range(0, 65536, 2048):  # right wheel gradually speeds up
        wheel_B.duty_u16(duty)  # 0~65535
        time.sleep(0.02)
        
    FORWARD( wheel_A , wheel_B )
    
    for duty in range(0, 65536, 2048):  # left wheel gradually speeds up
        wheel_A.duty_u16(duty)  # 0~65535
        time.sleep(0.02)
        
    FORWARD( wheel_A , wheel_B )
        
# The car turns right to avoid obstacles and then moves forward.
def RIGHT( wheel_A , wheel_B ):
    for duty in range(0, 65536, 2048):  # left wheel gradually speeds up
        wheel_A.duty_u16(duty)  # 0~65535
        time.sleep(0.02)
        
    FORWARD( wheel_A , wheel_B )
    
    for duty in range(0, 65536, 2048):  # right wheel gradually speeds up
        wheel_B.duty_u16(duty)  # 0~65535
        time.sleep(0.02)
        
    FORWARD( wheel_A , wheel_B )

# measure the distance between the car and obstacle
def get_distance():
    # transmit 15µs wave to trigger sonicator
    TRIG.value(0)
    time.sleep_us(5)  
    TRIG.value(1)
    time.sleep_us(10) # unit : microsecond
    TRIG.value(0)
    
    '''
    # explainment to the func : 
    time_pulse_us(pin, pulse_level, timeout_us=1000000)
    pin : detected-pin ; pulse_level : measured-value ; timeout_us : Max detectable time(ms)
    '''
    # measure the time of Echo's high level signal  
    duration = time_pulse_us(ECHO, 1 ,30000) # max-waiting time 30ms
    
    
    # calculate the distance ( Speed of sound = 343 m/s, 1µs = 0.000343 m)
    distance = (duration * 0.0343) / 2
    return distance
# ...........................................................................................................
# main program

while True:
    # test 1 : led react to the return result
    # test 2 : The direction of car's movement react to the return result
    
    # Receive the value of the distance between the obstacle and the car.
    dist = get_distance()
    print("Distance:", dist, "cm")
     
    if dist < 5 :
        LED_1.value(1)  #  LED_1 on
        BACK( wheel_left , wheel_right )
        RIGHT( wheel_left , wheel_right )
    elif ( dist < 10 && dist > 5 ) :  # dectect the object ( < 10 cm)
        LED_PWM_ON(LED_2) #  LED_2 on
        LED_2.duty_u16(0)
        
        LEFT( wheel_left , wheel_right )
    else :
        LED.value(0)  #  LED off
    
    time.sleep(0.5)  # delay 0.5 s

























