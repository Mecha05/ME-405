'''!@file                         encoder_romi.py
     @brief                       A driver for controlling the motors on the Romi
     @details                     A class that sets the duty cycle of the motors on the Romi
                                  The file includes only the MotorDriver class.
     @author                      Cole Lunde and Nate Hempstead
     @date                        December 13, 2024
'''
from pyb import Pin, Timer

class MotorDriver:
    '''!@brief                    A driver class for one motor of the Romi.
        @details                  Objects of this class can be used to apply PWM to a motor
                                  on the Romi robot
   '''
        
    def __init__ (self, EFF_tim, EFF_pin, DIR_pin, EN_pin):
        '''!@brief                Initializes and returns an object associated with a Romi motor.
            @details
        '''
        self.EFF_CH1 = EFF_tim.channel(1, Timer.PWM, pin = EFF_pin)
        self.DIR = Pin(DIR_pin, mode = Pin.OUT_PP)
        self.EN = Pin(EN_pin, mode = Pin.OUT_PP)
        self.EN.low()
        self.DIR.low()

    def set_duty (self, duty):
        '''!@brief                Set the PWM duty cycle for the DC motor.
            @details              This method sets the duty cycle to be sent to the Romi motor
                                  Positive values cause effort in forward direction, negative values
                                  in the reverse direction.
        @param duty               A signed number holding the dutycycle of the PWM signal sent to the
                                  Romi motor.
        '''
        if duty >= 0:
            self.DIR.low()
            self.EFF_CH1.pulse_width_percent(duty)
        else:
            self.DIR.high()
            self.EFF_CH1.pulse_width_percent(-duty)

    def enable (self):
        '''!@brief                Enable one motor of the romi
            @details              This method sets the enable pin associated with one
                                  the romi motor high in order to enable that motor.
        '''
        self.EN.high()
    
    def disable (self):
        '''!@brief                Disable one motor of the romi
            @details              This method sets the enable pin associated with one
                                  the romi motor low in order to disable that motor.
        '''
        self.EN.low()

if __name__ == '__main__':

    # Create a timer object to use for motor control for motors A and B
    tim_L = Timer(1, freq = 20_000)
    tim_R = Timer(8, freq = 20_000)

    # Create an L6206 driver object. You will need to modify the code to facilitate
    # passing in the pins and timer objects needed to run the motors.
    mot_L = MotorDriver(tim_L, Pin.cpu.A8, Pin.cpu.C0, Pin.cpu.C1)
    mot_R = MotorDriver(tim_R, Pin.cpu.C6, Pin.cpu.A10, Pin.cpu.B3)

    # Enable the L6206 driver
    mot_L.enable()
    mot_R.enable()
   
    
