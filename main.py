'''!@file                          main.py
    @brief                         The main program to drive Romi in a circle
    @details                       A main file that uses 3 tasks to drive Romi around a
                                   track using line sensors, bump sensors, IMU sensors, 
                                   Romi motors and encoders, and closed loop feedback. A 
                                   user specifies the linear velocity and the yaw rate based
                                   on the weighted sum from the line sensor data, and the Romi 
                                   will used datafrom the IMU to determine the yaw rate and the 
                                   encoders to determine the linear velocity to drive 
                                   around the specified track.
    @author                        Cole Lunde and Nate Hempstead
    @date                          December 13, 2024
'''

import cotask
import task_share
from pyb import Pin, Timer, I2C, UART, repl_uart
from encoder_romi import Encoder_romi
from time import ticks_ms, ticks_diff, sleep
from mot_romi import MotorDriver
import gc
from array import array
from closedloopright import ClosedLoopRight
from closedloopleft import ClosedLoopLeft
from linvelloop import LinVelLoop
from yawrateloop import YawRateLoop
from BNO055 import BNO055
from linesensor import LineSensor
from centroid import Centroid

def wheel_L(shares):
    '''!@brief                     A task to run and control the left wheel of Romi
        @details                   A task with two states that initializes the left motor and 
                                   encoder, and runs the left motor at a specified duty cycle. 
                                   The duty cycle is determined using a PI controller to control
                                   the left motor.
        @param shares              A tuple of multiple shares to share data from and with the task
    '''
    # set state to 0
    state = 0
    
    # Run FSM
    while True:
        # State 0 - Motor Setup
        if state == 0:

            # Enable the motor
            mot_L.enable()
            mot_L.set_duty(0)

            # Zero encoder for left wheel
            enc_L.zero()
            # Set start time as current time
            old_time = ticks_ms()
            # Create controller object for left wheel motor
            cont_L = ClosedLoopLeft()
            # Define variables from shares
            my_velocityL_ref, my_velocityL_meas, my_calib_flag, my_bump_flag, my_end_flag = shares
            L = 0
            
            # Set state to 1 only if IMU is calibrated
            if my_calib_flag.get() == 1:
                state = 1    
            yield state
    
        # State 1 - Update Encoder and Motor Control
        elif state == 1:
            # Update current time
            now = ticks_ms() 
            # Update the encoder and velocity measured
            enc_L.update()
            velL = enc_L.get_delta()/(ticks_diff(now,old_time))
            # Correct the measurement to rad/s  units
            velL = velL*2*3.1415*1000/1440
            # Set old time to current time
            old_time = now
            
            # Get desired velocity from shares
            omega_L = my_velocityL_ref.get()
            
            # Set Duty Cycle based on desired velocity and measured velocity
            L = cont_L.duty(omega_L, velL)
            mot_L.set_duty(L)
            
            # Put measured velocity into the shares variable
            my_velocityL_meas.put(velL)
            
            if (my_bump_flag.get() ==1):
                state=2
            if (my_end_flag.get()==1):
                state = 2
                    
            yield state
        elif state==2:
            #print('Left state 2')
            if (my_bump_flag.get() ==0 and my_end_flag.get() == 0):
                state=1
            yield state
        
        else: 
            raise ValueError('Invalid state')
            
def wheel_R(shares):
    '''!@brief                     A task to run and control the right wheel of Romi
        @details                   A task with two states that initializes the right motor and 
                                   encoder, and runs the right motor at a specified duty cycle. 
                                   The duty cycle is determined using a PI controller to control
                                   the right motor.
        @param shares              A tuple of multiple shares to share data from and with the task
    '''
    # Set state to 0
    state = 0
    
    # Run FSM
    while True:
        # State 0 - Motor Setup
        if state == 0:
            
            #Enable the motor and set duty cycle to 0
            mot_R.enable()
            mot_R.set_duty(0)

            # Zero Encoder R
            enc_R.zero()
            
            # Set old time to now
            old_time = ticks_ms()
            # Create controller object for right wheel motor
            cont_R = ClosedLoopRight()
            # Define variables from shares
            my_velocityR_ref, my_velocityR_meas, my_calib_flag, my_bump_flag, my_end_flag = shares
            
            # Set state to 1 if IMU is calibrated
            if my_calib_flag.get() == 1:
                state = 1
   
            yield state
    
        # State 1 - Update Encoder and Motor Control
        elif state == 1:
            # Update Current time
            now = ticks_ms()
            # Update the encoder and velocity measured
            enc_R.update()
            velR = enc_R.get_delta()/(ticks_diff(now,old_time))
            # Correct the measurement to rad/s units
            velR = velR*2*3.1415*1000/1440
            # Set old time to current time
            old_time = now
            
            # Get reference velocity from shares
            omega_R = my_velocityR_ref.get()

            # Set Duty Cycle based on desired velocity and measured velocity
            L = cont_R.duty(omega_R, velR)
            mot_R.set_duty(L)
            
            # Put measured velocity into shares variable
            my_velocityR_meas.put(velR)

            if (my_bump_flag.get()==1):
                state = 2
            if (my_end_flag.get()==1):
                state = 2
                
            yield state
        elif state == 2:
            #print('Right state 2')
            if (my_bump_flag.get() ==0 and my_end_flag.get() == 0):
                state=1
            yield state
        else: 
            raise ValueError('Invalid state')
            
def VelControl(shares):
    '''!@brief                     A task to run and control the linear velocity and yaw rate of Romi
        @details                   A task with four states that initializes the IMU and calibrates it.
                                   The task takes in data from the LineSensor and Centroid class that
                                   creates a weighted sum, which determines the specified yaw rate.
                                   The task specifies the linear velocity and uses the yaw rate
                                   from the centroid class before creating objects for linear 
                                   velocity and yaw rate controllers. The task uses these controllers
                                   and the data from the encoders to control the yaw rate and linear 
                                   velocity of Romi. The task calculates new reference velocities
                                   for the left and right motor and sends these values to the wheel_L
                                   and wheel_R tasks.The task monitors the bump sensors and runs the 
                                   Romi around the box if the bump sensors are triggered. The task also
                                   returns the Romi to the start of the track.
        @param shares              A tuple of multiple shares to share data from and with the task
    '''
    # Define state 0
    state = 0
    
    # Run FSM
    while True:
        # State 0 - Setup
        if state == 0:
            # Define reference variables from shares
            our_velL_ref, our_velL_meas, our_velR_ref, our_velR_meas, our_calib_flag, our_bump_flag, our_end_flag = shares
            
            # Define trackwidth
            w = 0.141
            # Define wheel radius
            r_w = 0.035
            # Define Linear Velocity
            lin_vel = 0.2
            
            # Define calibration flag variable
            calib_flag = 0
            # Define bump flag variable
            bump_flag = 0
            
            all_ones = True
            # Initialize Sharp time
            sharp_time = 0
            
            turn_done_flag = 0

            # Define sensor pins
            sensor_0_pin = Pin(Pin.cpu.A15, mode=Pin.OUT_PP)
            sensor_1_pin = Pin(Pin.cpu.C6, mode=Pin.OUT_PP)
            sensor_2_pin = Pin(Pin.cpu.C8, mode=Pin.OUT_PP)
            sensor_3_pin = Pin(Pin.cpu.C12, mode=Pin.OUT_PP)
            sensor_4_pin = Pin(Pin.cpu.B13, mode=Pin.OUT_PP)
            sensor_5_pin = Pin(Pin.cpu.B14, mode=Pin.OUT_PP)
            sensor_6_pin = Pin(Pin.cpu.B15, mode=Pin.OUT_PP)
            sensor_7_pin = Pin(Pin.cpu.B1, mode=Pin.OUT_PP)
            
            # Define Control Odd and Even Pins
            ctrl_odd_pin = Pin(Pin.cpu.B2, mode=Pin.OUT_PP)
            ctrl_even_pin = Pin(Pin.cpu.C10, mode=Pin.OUT_PP)
            
            # Set the Pins high
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
            
            # Create a sensor readings array
            readings = array('H', 8*[10])
            
            # Initialize Bump Sensor Pins as inputs
            bump_sensor_0 = Pin(Pin.cpu.D2, mode = Pin.IN, pull = Pin.PULL_UP)
            bump_sensor_1 = Pin(Pin.cpu.C11, mode = Pin.IN, pull = Pin.PULL_UP)
            bump_sensor_2 = Pin(Pin.cpu.B7, mode = Pin.IN, pull = Pin.PULL_UP)
            
            
            tleft_time = None
            current_time = None
            
            # Initialize controller objects for linear velocity and yaw rate
            lin_cont = LinVelLoop()
            yaw_cont = YawRateLoop()
            
            # Initialize IMU i2c object
            i2c = I2C(1, I2C.CONTROLLER, baudrate=100000)
            imu = BNO055(i2c, Pin.cpu.B9, Pin.cpu.B8, Pin.cpu.C9)
            imu.set_mode(0x0C)  # NDOF mode
            
            # Read Calibration Status of the IMU and display it
            sys_calib_status, gyr_calib_status, acc_calib_status, mag_calib_status = imu.get_calib_status()
            print(f"{sys_calib_status}, {gyr_calib_status}, {acc_calib_status}, {mag_calib_status}")
            
            # If IMU is fully calibrated, set calib_flag to 1 to signal that it is calibrated 
            if sys_calib_status == 3 and gyr_calib_status == 3 and acc_calib_status == 3 and mag_calib_status == 3:
                calib_flag = 1
                print("Calibration Complete")
                our_calib_flag.put(calib_flag)
                
            our_calib_flag.put(calib_flag)   
            
            # Set state to 1
            if calib_flag == 1:
                sleep(10)
                init_heading = imu.read_heading()
                print(f"{init_heading}")
                done_time = ticks_ms()
                state = 1
            
            yield state
            
            # State 1 - Velocity Control
        elif state == 1:
            
            # Get actual left and right wheel velocities
            omega_L_act = our_velL_meas.get()
            omega_R_act = our_velR_meas.get()
                    
            if (bump_sensor_0.value() == 0 or bump_sensor_1.value() == 0 or bump_sensor_2.value() == 0):
                print('bumped')
                back_time = ticks_ms()
                tright_time = None
                tleft_time = None
                our_bump_flag.put(1)
                bump_flag = 1
                state = 2
            
            # Read all the line sensors
            sensor_7_reading = sensor_0.read_sensor()
            sensor_6_reading = sensor_1.read_sensor()
            sensor_5_reading = sensor_2.read_sensor()
            sensor_4_reading = sensor_3.read_sensor()
            sensor_3_reading = sensor_4.read_sensor()
            sensor_2_reading = sensor_5.read_sensor()
            sensor_1_reading = sensor_6.read_sensor()
            sensor_0_reading = sensor_7.read_sensor()
            
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
            
            #print(f"{readings}")
            
            # Determine the weighted sum of the readings
            sensor_reading = Centroid(readings)
            reading = sensor_reading.weighted_sum()
            #print(reading)
            
            if -1 <= reading <= 1:
                yaw_rate = 0
            elif -11 <= reading < -1:
                yaw_rate = -3
            elif reading < -11:
                yaw_rate = -5
                sharp_time = ticks_ms()
            elif 1 < reading <= 11:
                yaw_rate = 3
            else:  
                yaw_rate = 5
                sharp_time = ticks_ms()
                
            # Get current time
            current_time = ticks_ms()
            
            # If it has been less than 1.5 seconds since a +/- 12 reading
            if ticks_diff(current_time, sharp_time) < 2000:
                # Set linear velocity to slower rate
                lin_vel = 0.065
            else:
                # Set linear velocity to normal rate
                lin_vel = 0.2
        
        
            # Reading sum variable initialized
            reading_sum = 0
            all_ones = False
            
            print(ticks_diff(current_time, done_time))
            if bump_flag == 1 and ticks_diff(current_time,done_time) >= 12000:
                for value in readings: 
                    reading_sum += value
                    if reading_sum >= 4:
                        all_ones = True
                if all_ones == True:
                    all_ones_time= ticks_ms()
                    our_end_flag.put(1)
                    state = 3
            elif ticks_diff(current_time,done_time) <= 12000:
                  for value in readings:
                      reading_sum += value
                      if reading_sum >= 3:
                          all_ones = True
                  if all_ones == True:
                      yaw_rate = 0  
                      lin_vel = 0.2
            else:
                for value in readings:
                    reading_sum += value
                    if reading_sum >= 5:
                        all_ones = True
                if all_ones == True:
                    yaw_rate = 0  
                    lin_vel = 0.25
                    
            # Calculate measured linear velocity
            lin_vel_meas = (omega_L_act + omega_R_act)*(r_w/2)
            
            # Get desired linear velocity from controller
            lin_vel_ref = lin_cont.set_vel(lin_vel, lin_vel_meas)
           # print(f"{lin_vel}, {lin_vel_ref}, {lin_vel_meas}")
            
            # Read IMU to get angular velocity
            IMU_yaw_rate = imu.read_yaw_rate()
            # Convert from degrees to rad
            yaw_rate_meas = IMU_yaw_rate * 3.1415/180
           
            # Calculate measured yaw rate
            yaw_rate_meas = (omega_R_act-omega_L_act)*(r_w/w)
            # Get desired yaw rate from controller
            yaw_rate_ref = yaw_cont.set_yaw(yaw_rate, yaw_rate_meas)
            #print (yaw_rate_ref)
            
            # Calculate desired left and right motor velocities
            omega_L_ref = ((lin_vel_ref)/r_w) - (w/(2*r_w))*yaw_rate_ref
            omega_R_ref = ((lin_vel_ref)/r_w) + (w/(2*r_w))*yaw_rate_ref
            
            # Put desired left and right motor velocities in shares
            our_velL_ref.put(omega_L_ref)
            our_velR_ref.put(omega_R_ref)
            
            curr_heading = imu.read_heading()
            print(f"{curr_heading}, {init_heading}")
            
            yield state
            
        # State 2 - Bumped
        elif state == 2:
            now_time = ticks_ms()
            # First: Handle "back" movement
            if ticks_diff(now_time, back_time) <= 800:
                print('back')
                #print(f"{lin_vel}, {lin_vel_ref}, {lin_vel_meas}")
                mot_L.set_duty(-30)
                mot_R.set_duty(-30)                
                tright_time = None
                tleft_time = None
            else:
                if tright_time is None: # Set tright_time only once
                    tright_time = ticks_ms()  # Record the start time of "right" state
                elif ticks_diff(now_time, tright_time) <= 550:
                    # Continue "right" movement
                    print('Turn R')
                    mot_L.enable()
                    mot_R.disable()
                    mot_L.set_duty(30)
                elif ticks_diff(now_time, tright_time) <= 1200:
                    # Forward movement
                    print('frwd')
                    mot_R.enable()
                    mot_L.set_duty(30)
                    mot_R.set_duty(30)
                else:
                    if tleft_time is None: # Set tright_time only once
                        tleft_time = ticks_ms()  # Record the start time of "right" state
                    elif ticks_diff(now_time, tleft_time) <= 460:
                        # Continue "right" movement
                        print('Turn L')
                        mot_R.enable()
                        mot_L.disable()
                        mot_R.set_duty(30)
                    elif ticks_diff(now_time, tleft_time) <= 2500:
                        # Forward movement
                        print('frwd')
                        mot_L.enable()
                        mot_L.set_duty(27)
                        mot_R.set_duty(30)
                    else:
                        # Return to state 1
                        print('transition to state 1')
                        # Ensure tright_time and tleft_time are reset here
                        done_time = ticks_ms()
                        tright_time = None
                        tleft_time = None
                        state = 1
                        # Reset bump flag share variable
                        our_bump_flag.put(0)
            
            yield state
            
        # State 3 - Return to Start    
        elif state == 3:
            # Get the current heading from the imu
            curr_heading = imu.read_heading()
            #print(f"{curr_heading}, {init_heading}")
            # Record the time when all black is read
            all_ones_now = ticks_ms()
            # Go forward for 600 ms
            if ticks_diff(all_ones_now, all_ones_time) <= 600:
                print('forward')
                mot_L.set_duty(20)
                mot_R.set_duty(20)
            # Turn around until the heading is accurate
            elif abs(curr_heading - init_heading) >= .5 and turn_done_flag == 0:
                print('turn')
                mot_L.set_duty(-10)
                mot_R.set_duty(10)
                turn_time = ticks_ms()
            # Pause for  500 ms
                print(f"{curr_heading}, {init_heading}")
            elif ticks_diff(all_ones_now, turn_time) <= 500:
                print('stopped')
                turn_done_flag = 1
                mot_L.set_duty(0)
                mot_R.set_duty(0)
            # Go Forward for the next 3600 ms
            elif ticks_diff(all_ones_now, turn_time) <= 2050:
                #IF NOT WORK PUT BACK TO <= 4100, L=34.5, R=30
                #print('forward to start')
                mot_L.set_duty(64.5)
                mot_R.set_duty(60)
            # Disable the motors as the Track has been completed
            else:
                #print('done')
                mot_L.disable()
                mot_R.disable()
            yield state
            
        else:
            raise ValueError('Invalid State')

    
if __name__ == "__main__": 
    
    uart = UART(3, baudrate=115200)
    repl_uart(uart)
    
    # Create a timer and motor object for the right wheel
    tim_R = Timer(4, freq = 20_000)
    mot_R = MotorDriver(tim_R, Pin.cpu.B6, Pin.cpu.A10, Pin.cpu.B3)
    
    # Create a timer and motor object for the left wheel
    tim_L = Timer(1, freq = 20_000)
    mot_L = MotorDriver(tim_L, Pin.cpu.A8, Pin.cpu.C0, Pin.cpu.C1)
    
    # Create an encoder object for the right wheel
    tim_ENR = Timer(3, period = 65535, prescaler = 0)
    enc_R = Encoder_romi(tim_ENR, Pin.cpu.A6, Pin.cpu.A7)
    # Zero encoder R
    enc_R.zero()
    
    # Create an encoder object for the left wheel
    tim_ENL = Timer(2, period = 65535, prescaler = 0)
    enc_L = Encoder_romi(tim_ENL, Pin.cpu.A0, Pin.cpu.A1)
    # Zero encoder L
    enc_L.zero()
    
    
    # Create reference and measured velocity share variables for the left motor
    velocityL_ref = task_share.Share('f', thread_protect = False, name = "velocityL_ref")
    velocityL_meas = task_share.Share('f', thread_protect = False, name = "velocityL_meas")

    # Create reference and measured velocity share variables for the right motor
    velocityR_ref = task_share.Share('f', thread_protect = False, name = "velocityR_ref")
    velocityR_meas = task_share.Share('f', thread_protect = False, name = "velocityR_meas")
    
    # Create share variables for the calibration, bump, and end flags
    calibration_flag = task_share.Share('H', thread_protect = False, name = "calibration_flag")
    Bump_flag = task_share.Share('H', thread_protect = False, name = "Bump flag")
    end_flag = task_share.Share('H', thread_protect = False, name = "end_flag")
    
    # Create each task and append the task to the list
    task1 = cotask.Task (wheel_L, name="Task_1", priority=3, period=6, profile=True, trace=False, \
                         shares=(velocityL_ref, velocityL_meas, calibration_flag, Bump_flag, end_flag))
    cotask.task_list.append(task1)
    
    task2 = cotask.Task (wheel_R, name="Task_2", priority=3, period=6, profile=True, trace=False, \
                         shares=(velocityR_ref, velocityR_meas, calibration_flag, Bump_flag, end_flag))
    cotask.task_list.append(task2)
    
    task3 = cotask.Task (VelControl, name="Task_3", priority=2, period=8, profile=True, trace=False, \
                         shares=(velocityL_ref, velocityL_meas, velocityR_ref, velocityR_meas, calibration_flag, Bump_flag, end_flag))
    cotask.task_list.append(task3)
    
    
    gc.collect()
    
    # Run the Scheduler
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break
        
    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print('')
        
        
