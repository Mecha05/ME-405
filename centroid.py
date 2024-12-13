'''!@file                          centroid.py
    @brief                         The  program to create a weighted sum of the 
                                   line sensor data.
    @details                       A  file that uses a weighted sum of the line sensor
                                   data that will be used to determine the control
                                   of the Romi Robot.
    @author                        Cole Lunde and Nate Hempstead
    @date                          December 13, 2024
'''

from array import array 

class Centroid:
    '''!@brief                    A Centroid class to determine a weighted sum
        @details                  Objects of this class can be used to create a weighted  
                                  sum of the line sensor readings array.
   ''' 
   
    def __init__(self,measurements):
        '''!@brief                Initialize a centroid object.
            @details              This intiializes the measurements and weights of the array to
                                  determine the weighted sum.
        @param measurements       An array of line sensor readings from the LineSensor class.
        '''
        
        self.measurements = measurements
        # Create sum variable for weighted sum
        self.weight_sum = 0
        # Create an array of weights of the sensors
        self.weights = array('h', [-7, -5, -2, -1, 1, 2, 5, 7])
    
    def weighted_sum(self):
        '''!@brief                Creates a weighted sum based on which line sensors read 0 or 1.
            @details              This method creates a weighted sum with the measurements array of 0 
                                  or 1 from the LineSensor class.
            @return               The weighted sum calculated from the array of the line sensor readings.
        '''
        self.weight_sum = 0
        # Loop through the measurements to determine a centroid of the sensor array
        for i, val in enumerate(self.measurements):
             # Add the value times the weight of the senor to the centroid
             self.weight_sum += val * self.weights[i]
        # Return the centroid value
        return self.weight_sum