'''!@file                          yawrateloop.py
    @brief                         A closed loop to control the yaw rate of the robot.
    @details                       A proportional integral controller loop with a method
                                   that uses kp to return a desired reference yaw rate
    @author                        Cole Lunde and Nate Hempstead
    @date                          December 13, 2024
'''

class YawRateLoop:
    '''!@brief                          Proportional controller for the longitudinal velocity 
                                        of the Romi robot.
        @details                        A class to control the romi robot linear velocity using a proportional 
                                        controller to intake a desired reference velocity of the robot
                                        and a calculated measured velocity of the motor from the motor controllers
                                        and encoder class. The controller uses Kp and Ki to calculate and return 
                                        the linear velocity of the robot to send to the motor controller classes.
    '''
    
    def __init__(self):
        '''!@brief                      Creates an object of the YawRateLoop class.
            @details                    Initializes the object of the YawRateLoop class by setting 
                                        the value of Kp.
        '''
        self.K_p = 1.75
        
    def set_yaw(self, yaw_rate_ref, yaw_rate_meas):
        '''!@brief                      set_yaw method to return a desired uaw rate based on the error and 
                                        Kp values.
            @details                    The set_yaw method uses the error calculated from the reference and
                                        measured yaw rate. It uses Kp and the error to calculate a new 
                                        yaw rate velocity.
            @param lin_vel_ref          The desired yaw rate of the romi robot
            @param lin_vel_meas         The measured yaw rate of the romi robot from the motor controllers and encoder
            @return                     The new desired yaw rate for the romi robot to send to the motor controllers
        '''
        # Calculate the error from the reference and measured yaw rate
        self.error = yaw_rate_ref - yaw_rate_meas
        # Determine the new yaw rate from the error and return the value
        self.yaw_rate = self.K_p*self.error
        return self.yaw_rate