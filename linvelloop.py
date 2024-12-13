'''!@file                          linvelloop.py
    @brief                         A closed loop to control the longitudinal velocity of the robot.
    @details                       A proportional controller loop with a method that uses Kp to 
                                   return a desired reference linear velocity
    @author                        Cole Lunde and Nate Hempstead
    @date                          December 13, 2024
'''

class LinVelLoop:
    '''!@brief                          Proportional controller for the longitudinal velocity 
                                        of the Romi robot.
        @details                        A class to control the romi robot linear velocity using a proportional 
                                        controller to intake a desired reference velocity of the robot and a
                                        calculated measured velocity of the motor from the motor controllers
                                        and encoder class. The controller uses Kp to calculate and return 
                                        the linear velocity of the robot to send to the motor controller classes.
    '''
    
    def __init__(self):
        '''!@brief                      Creates an object of the LinVelLoop class.
            @details                    Initializes the object of the LinVelLoop class by setting 
                                        the value of Kp.
        '''
        self.K_p = 1.75
        
    def set_vel(self, lin_vel_ref, lin_vel_meas):
        '''!@brief                      set_vel method to return a desired linear velocity based on the error 
                                        and Kp values.
            @details                    The set_vel method uses the error calculated from the reference and
                                        measured linear velocity. It uses Kp and the error to calculate a new 
                                        linear reference velocity.
            @param lin_vel_ref          The desired linear velocity of the romi robot
            @param lin_vel_meas         The measured linear velocity of the romi robot from the motor controllers and encoder
            @return                     The new desired linear velocity for the romi robot to send to the motor controllers
        '''
        # Calculate the error from the reference and measured velocity
        self.error = lin_vel_ref - lin_vel_meas
        # Calculate the new velocity and return the velocity
        self.vel = self.K_p*self.error 
        return self.vel