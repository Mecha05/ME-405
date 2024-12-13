'''!@file                         encoder_romi.py
     @brief                       A driver for reading from Quadrature Encoders on the Romi
     @details                     A class that reads the encoder data from the encoders on the 
                                  Romi motors. The file includes only the Encoder_Romi class.
     @author                      Cole Lunde and Nate Hempstead
     @date                        December 13, 2024
'''
from pyb import Timer

class Encoder_romi:
    '''@brief                     Interface with qudrature econders
       @details                   The object is initialized, has an update method
                                  that updates all the necessary values, a get_position method
                                  that returns the position of the encoder, a get_delta method
                                  that reutrns the delta from the last call of update, a zero
                                  method that zeros the position of the encoder.
    '''
    
    def __init__(self, EN_tim, CH_A_Pin, CH_B_Pin):
        '''!@brief                 constructs an encoder object
            @details               The __init__ method creates the object assigning encoder timer object
                                  to the self variable, sets the pins of the encoder timer from the given
                                  arguments, and sets the counter as the counter of the encoder timer. It
                                  also sets the autoreload value and sets the position and old count to 0.
            @param EN_tim         A timer object to use for the encoder object
            @param CH_A_Pin       A pin object to be assigned to channel 1 of the encoder object
            @param CH_B_Pin       A pin object to be assigned to channel 2 of the encoder object
        '''
        # Assign timer and pins based on given arguments
        self.EN_tim = EN_tim
        self.EN1 = EN_tim.channel(1, pin=CH_A_Pin, mode=Timer.ENC_AB)
        self.EN2 = EN_tim.channel(2, pin=CH_B_Pin, mode=Timer.ENC_AB)
        self.EN_counter = EN_tim.counter()
        self.AR = 65535
        self.postion = 0
        self.count_old = 0
        
    def update(self):
        '''!@brief              Updates encoder position and delta
            @details            The update method gets the new count and calculates the delta from the new
                                and old count before resetting the old count to the new count. The method 
                                also updates delta properly if rollover has occurred in either direction.
                                It then adds the delta to the position to update the position.
        '''
        # Read the new count, calculate delta, and reset the old count
        self.count_new = self.EN_tim.counter()
        self.delta = self.count_new - self.count_old
        self.count_old = self.count_new
        # Update delta if rollover has occurred
        if self.delta > ((self.AR+1)/2):
            self.delta = self.delta - (self.AR+1)
        if self.delta < (-(self.AR+1)/2):
            self.delta = self.delta + (self.AR+1)
        self.position += self.delta
        

    def get_position(self):
        '''!@brief              Gets the most recent encoder position
            @details            The method simply returns the position when the method is called.
            @return             The current position of the encoder
        '''
        return self.position

    def get_delta(self):
        '''!@brief              Gets the most recent encoder delta
            @details            The method simply returns the delta when the method is called.
            @return             The current delta of the encoder
       '''
        return self.delta

    def zero(self):
        '''!@brief             Resets the encoder position to zero
            @details           Sets the position variable to zero when called.
        '''
        self.position = 0