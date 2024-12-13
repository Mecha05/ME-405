'''!@file                          BNO055.py
    @brief                         A class to read from and write to the BNO055 IMU
    @details                       A class to initialize a BNO055 I2C IMU object with methods
                                   set_mode to set the mode of the imu, get calib_status to return
                                   the status of the IMU calibration, get_calib_coeffs to get the
                                   calibration coefficients of the object, set_calib_coefficients
                                   to set the calibration coefficients, read_euler to read the 
                                   heading roll and pitch data, read_heading to return only the 
                                   heading data, read_angular_velocity to return the gyroscope 
                                   data of heading rate, pitch rate, and yaw rate, and get_yaw_rate
                                   to get just the yaw rate data from the object.
    @author                        Cole Lunde and Nate Heampstead
    @date                          December 13, 2024
'''

from pyb import Pin, I2C
import time
import struct

class BNO055:
    def __init__(self, i2c, sda, scl, reset):
        '''!@brief                      Initializes objects of the BNO055 class.
            @details                    Takes in an i2c object, sda, scl, and reset pin and specifies the address,
                                        mode, and reset pin to high of the BNO055 object.
            @param i2c                  An i2c object previously created
            @param sda                  The pin object used for the sda
            @param scl                  The pin objectused for the scl
            @param reset                The pin object used for reset
        '''
        self.i2c=i2c
        self.addr = 0x28  # Default I2C address for BNO055
        self.mode = 0x00  # Default mode
        
        # Initialize the reset pin
        self.reset_pin = Pin(reset, Pin.OUT_PP)
        self.reset_pin.high()  # Ensure reset pin is high (active low)
        time.sleep(0.75)

    def set_mode(self, mode):
        '''!@brief                      Sets the mode of the BNO055 object.
            @details                    Takes in a mode value to write to the BNO055 object at the mode address
                                        of 0x3D.
            @param mode                 The desired mode to set the BNO055 to
        '''
        # Set the mode of the BNO055
        self.mode = mode
        self.i2c.mem_write(self.mode, self.addr, 0x3D)  # Register address for mode setting
        time.sleep(0.05)

    def get_calib_status(self):
        '''!@brief                      Gets the calibration status of the BNO055 IMU
            @details                    Gets the calibration status by reading the calibration status byte on
                                        the BNO055 IMU. Unpacks the byte and assigns the two bits to the system,
                                        gyroscope, accelermoeter, and the magnetometer.
            @return                     The four calibration status as a number 0-3
        '''
        # Get the calibration status from the IMU
        calib_stat = bytearray([0 for n in range(1)])
        calib_stat = self.i2c.mem_read(calib_stat, self.addr, 0x35)
        # Unpack the calibration status and assign bytes to the sys, gyr, acc, and mag
        calib_byte, = struct.unpack('<B', calib_stat)
        sys_calib = (calib_byte >> 6) & 0x03  
        gyr_calib = (calib_byte >> 4) & 0x03  
        acc_calib = (calib_byte >> 2) & 0x03  
        mag_calib = calib_byte & 0x03         
        return sys_calib, gyr_calib, acc_calib, mag_calib
        

    def get_calib_coeffs(self):
        '''!@brief                      Gets the calibration coefficients of the BNO055 IMU
            @details                    Gets the calibration coefficients by reading the calibration coefficients
                                        bytes on the BNO055 IMU. Unpacks the bytes and assigns the coefficients to the
                                        gyroscope, accelermoeter, and the magnetometer.
            @return                     The  calibration coefficients as a signed int
        '''
        calib_coeffs = bytearray([0 for n in range(22)])
        self.i2c.mem_read(calib_coeffs, self.addr, 0x55)
        acc_offset_x, acc_offset_y, acc_offset_z = struct.unpack('<hhh', calib_coeffs[0:6])
        mag_offset_x, mag_offset_y, mag_offset_z = struct.unpack('<hhh', calib_coeffs[6:12])
        gyr_offset_x, gyr_offset_y, gyr_offset_z = struct.unpack('<hhh', calib_coeffs[12:18])
        acc_radius, mag_radius = struct. unpack('<hh', calib_coeffs[18:22])
        return (acc_offset_x, acc_offset_y, acc_offset_z,
            mag_offset_x, mag_offset_y, mag_offset_z,
            gyr_offset_x, gyr_offset_y, gyr_offset_z,
            acc_radius, mag_radius)

    def set_calib_coeffs(self, calib_data):
        '''!@brief                      Sets the calibration coefficients of the BNO055 IMU
            @details                    Sets the calibration coefficients by writing to the calibration coefficients
                                        bytes on the BNO055 IMU. 
            @param calib_data           The calibration coefficients data to write to the BNO055 IMU
        '''
        self.i2c.mem_write(calib_data, self.addr, 0x55)
        time.sleep(0.05)

    def read_euler(self):
        '''!@brief                      Gets the euler angles data of the BNO055 IMU
            @details                    Gets the euler angles data by reading the 6 bytes with the euler data 
                                        on the BNO055 IMU. Unpacks the bytes and assigns the coefficients to 
                                        heading, roll, and pitch.
            @return                     The heading, roll, and pitch in degrees.
        '''
        euler_data = bytearray([0 for n in range(6)])
        self.i2c.mem_read(euler_data, self.addr, 0x1A)  # Start of Euler angles data
        heading, roll, pitch = struct.unpack('<hhh', euler_data)
        return heading/16.0, roll/16.0, pitch/16.0
    
    def read_heading(self):
        '''!@brief                      Gets the heading data of the BNO055 IMU
            @details                    Gets the heading data by reading the 2 bytes with the heading data 
                                        on the BNO055 IMU. Unpacks the bytes and assigns the coefficients to 
                                        heading.
            @return                     The heading in degrees.
        '''
        heading_data = bytearray([0 for n in range(2)])
        self.i2c.mem_read(heading_data, self.addr, 0x1A)
        heading, = struct.unpack('<h', heading_data)
        return heading/16.0

    def read_angular_velocity(self):
        '''!@brief                      Gets the angular velocity data of the BNO055 IMU
            @details                    Gets the angular velocity data by reading the 6 bytes with the angular velocity
                                        on the BNO055 IMU from the gyroscope. Unpacks the bytes and assigns the coefficients 
                                        to gyro_x, gyro_y, and gyro_z.
            @return                     The gyro_x, gyro_y, and gyro_z in degrees per second.
        '''
        angular_data = bytearray([0 for n in range(6)])
        self.i2c.mem_read(angular_data, self.addr, 0x14)  # Start of angular velocity data
        gyro_x, gyro_y, gyro_z = struct.unpack('<hhh', angular_data)
        return gyro_x/16.0, gyro_y/16.0, gyro_z/16.0
    
    def read_yaw_rate(self):
        '''!@brief                      Gets the yaw rate data of the BNO055 IMU
            @details                    Gets the yaw rate data by reading the 2 bytes with the gyro_x data 
                                        on the BNO055 IMU. Unpacks the bytes and assigns the coefficients to 
                                        yaw_rate.
            @return                     The yaw_rate in degrees per second.
        '''
        yaw_data = bytearray([0 for n in range(2)])
        self.i2c.mem_read(yaw_data, self.addr, 0x18)
        yaw_rate, = struct.unpack('<h', yaw_data)
        return yaw_rate /16.0

if __name__ == "__main__":
    # Initialize I2C on bus 1 with correct pin assignments
    i2c = I2C(1, I2C.MASTER, baudrate=100000)
        
    imu = BNO055(i2c, Pin.cpu.B9, Pin.cpu.B8, Pin.cpu.C9)
    imu.set_mode(0x0C)  # NDOF mode
    heading, roll, pitch = imu.read_euler()
    '''print("Heading:", heading, "Roll:", roll, "Pitch:", pitch)
    print(f"{imu.get_calib_status()}")
    #print(f"{bin(255)}")
    print(f"{imu.get_calib_coeffs()}")
    gyro_x, gyro_y, gyro_z = imu.read_angular_velocity()
    print("gyro_x: ", gyro_x, "gyro_y: ", gyro_y, "gyro z: ", gyro_z)
    print(f"Heading: {imu.read_heading()}")
    print(f"Yaw Rate: {imu.read_yaw_rate()}")'''
    
    
