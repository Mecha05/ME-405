'''!@file                          linesensor.py
    @brief                         The  program to read the data from a line sensor
    @details                       A  file that uses a read sensor method and a
                                   normalize sensor reading to read the value of each 
                                   line sensor and determine if that value corresponds
                                   to a white or black line. It returns the reading and
                                   normalized reading.
    @author                        Cole Lunde and Nate Hempstead
    @date                          December 13, 2024
'''

from time import ticks_us, ticks_diff
from array import array
import time
from pyb import Pin
from centroid import Centroid

class LineSensor:
    '''!@brief                    A LineSensor class to read the line sensor.
        @details                  Objects of this class can be used to read a single line 
                                  sensor
   '''  
    def __init__(self, sensor_pin):
        '''!@brief                Initializes an object associated with a line sensor.
            @details
        '''
        # Initialize sensor pin
        self.sensor_pin = Pin(sensor_pin, mode=Pin.OUT_PP) 
        self.sensor_pin_name = sensor_pin
        
    def read_sensor(self):
        '''!@brief                Reads the value of the line sensor.
            @details              This method sets the pin high and measures how long it takes to go 
                                  low, which depends on the color it reflects off of.
            @return               The time sensed between high and low output of the line sensor pin.
        '''
        # Set the pin to output mode and set it high
        self.sensor_pin = Pin(self.sensor_pin_name, mode=Pin.OUT_PP)
        self.sensor_pin.high()
        time.sleep(0.01)
        
        # Get time of start reading
        start = ticks_us()
        
        # Set the sensor pin to input mode
        self.sensor_pin = Pin(self.sensor_pin_name, mode=Pin.IN)

        # Wait for the pin to go low or timeout
        while self.sensor_pin.value() == 1:
            # Check if timeout has passed
            if ticks_diff(ticks_us(), start) > 500000:
                # If it times out, break out of the loop
                print("Timeout reached")
                return None  # or return a specific error value
        
        # Get time after the pin is low
        end = ticks_us()
        # Find the difference between start and end time
        self.time_sensed = ticks_diff(end,start)
        
        return self.time_sensed
    
    def normalize_reading(self, reading):
        '''!@brief                Normalizes the value of the line sensor.
            @details              This method takes the reading and comapres it to max 
                                  and min readings to determine if it is black(1) or 
                                  white (0)
            @return               1 or 0 if it read black(1) or white(0)
        '''
        # Time for black line reflection reading
        self.max_reading = 1800
        # Time for white line reflection reading
        self.min_reading = 720
        
        # Determine a normalized reading based on max and min time
        self.reading = (reading - self.min_reading) / self.max_reading

        if self.reading <= 0.3:
            return 0
        else:
            return 1

if __name__ == "__main__":
    
        # Define sensor pins
        sensor_7_pin = Pin(Pin.cpu.A15, mode=Pin.OUT_PP)
        sensor_6_pin = Pin(Pin.cpu.C6, mode=Pin.OUT_PP)
        sensor_5_pin = Pin(Pin.cpu.C8, mode=Pin.OUT_PP)
        sensor_4_pin = Pin(Pin.cpu.C12, mode=Pin.OUT_PP)
        sensor_3_pin = Pin(Pin.cpu.B13, mode=Pin.OUT_PP)
        sensor_2_pin = Pin(Pin.cpu.B14, mode=Pin.OUT_PP)
        sensor_1_pin = Pin(Pin.cpu.B15, mode=Pin.OUT_PP)
        sensor_0_pin = Pin(Pin.cpu.B1, mode=Pin.OUT_PP)
        
        # Define Control Odd and Even Pins
        ctrl_odd_pin = Pin(Pin.cpu.B2, mode=Pin.OUT_PP)
        ctrl_even_pin = Pin(Pin.cpu.C10, mode=Pin.OUT_PP)
        
        
        ctrl_odd_pin.high()
        ctrl_even_pin.high()

        # Define Sensor Objects
        sensor_0 = LineSensor(sensor_0_pin)
        sensor_1 = LineSensor(sensor_1_pin)
        sensor_2 = LineSensor(sensor_2_pin)
        sensor_3 = LineSensor(sensor_3_pin)
        sensor_4 = LineSensor(sensor_4_pin)
        sensor_5 = LineSensor(sensor_5_pin)
        sensor_6 = LineSensor(sensor_6_pin)
        sensor_7 = LineSensor(sensor_7_pin)
        
        readings = array('H', 8*[10])
        
        while True:
            # Read all the line sensors
            sensor_0_reading = sensor_0.read_sensor()
            sensor_1_reading = sensor_1.read_sensor()
            sensor_2_reading = sensor_2.read_sensor()
            sensor_3_reading = sensor_3.read_sensor()
            sensor_4_reading = sensor_4.read_sensor()
            sensor_5_reading = sensor_5.read_sensor()
            sensor_6_reading = sensor_6.read_sensor()
            sensor_7_reading = sensor_7.read_sensor()
            
            # Normalize line sensor values
            sensor_0_nreading = sensor_0.normalize_reading(sensor_0_reading)
            sensor_1_nreading = sensor_1.normalize_reading(sensor_1_reading)
            sensor_2_nreading = sensor_2.normalize_reading(sensor_2_reading)
            sensor_3_nreading = sensor_3.normalize_reading(sensor_3_reading)
            sensor_4_nreading = sensor_4.normalize_reading(sensor_4_reading)
            sensor_5_nreading = sensor_5.normalize_reading(sensor_5_reading)
            sensor_6_nreading = sensor_6.normalize_reading(sensor_6_reading)
            sensor_7_nreading = sensor_7.normalize_reading(sensor_7_reading)
            
            # Add all line sensor values into a readings array
            readings[0] = sensor_0_nreading
            readings[1] = sensor_1_nreading
            readings[2] = sensor_2_nreading
            readings[3] = sensor_3_nreading
            readings[4] = sensor_4_nreading
            readings[5] = sensor_5_nreading
            readings[6] = sensor_6_nreading
            readings[7] = sensor_7_nreading
            
            # Determine the weighted sum of the readings
            sensor_reading = Centroid(readings)
            #print(sensor_reading.weighted_sum())
            
            #print(f"{sensor_0_nreading}, {sensor_1_nreading}, {sensor_2_nreading}, {sensor_3_nreading}, \
                  #{sensor_4_nreading}, {sensor_5_nreading}, {sensor_6_nreading}, {sensor_7_nreading}")
            print(f"{sensor_0_reading}, {sensor_1_reading}, {sensor_2_reading}, {sensor_3_reading}, \
                  {sensor_4_reading}, {sensor_5_reading}, {sensor_6_reading}, {sensor_7_reading}")
                  
        time.sleep(0.1)
        