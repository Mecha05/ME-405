'''!@file                          closedloopright.py
    @brief                         A closed loop to control the right motor
    @details                       A proportional integral controller loop with a method
                                   that uses kp and ki to return a desired duty cycle for 
                                   the right motor
    @author                        Cole Lunde and Nate Heampstead
    @date                          December 13, 2024
'''

class ClosedLoopRight:
    '''!@brief                          Proportional integral controller for the right motor 
        @details                        A class to control the right motor using a proportional integral 
                                        controller to intake a desired reference velocity of the motor
                                        and a measured velocity of the motor from the encoder class. 
                                        The controller uses Kp and Ki to calculate and return the duty
                                        cycle.
    '''
    
    def __init__(self):
        '''!@brief                      Creates an object of the closedloopleft class.
            @details                    Initializes the object of the closedloopright class by setting 
                                        the values of Kp and Ki and sets the integral to zero.
        '''
        # Set the Kp and Ki values
        self.K_p = 2.2
        self.K_i = 0.5
        # Initialize the integral to 0
        self.integral = 0
    
    def duty(self, vel_ref, vel_meas):
        '''!@brief                     Duty method to return a desired duty cycle based on the error, 
                                       Kp, and Ki measurements
            @details                   The duty method uses the error calculated when the object is created,
                                       Kp, and Ki, to calculate the duty cycle to reach the reference velocity.
                                       Sets a maximum and minimum limit of -100% to 100% to safeguard the motors
                                       against any issues with the control loop.
            @param vel_ref             The desired velocity of the left motor
            @param vel_meas            The measured velocity of the left motor from the encoder
            @return                    The duty cycle for the left motor value to be returned
        '''
        # Calculate the error from the measured and desired velocity
        self.error = vel_ref - vel_meas
        # Add the error time dt to the integral
        self.integral += self.error * 0.006
        # Calculate the duty cycle using Kp and Ki
        self.L = self.K_p*self.error + self.K_i*self.integral
        self.L = max(min(self.L, 100), -100)  # Clamp to [-100%, 100%]
        return self.L
        
        