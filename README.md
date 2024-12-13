# ME-405
ME-405 Romi Portfolio

## Required materials:
1) Romi chasis of your desired color
2) Romi Drive and caster wheels
3) BNO055 IMU Breakout Board
4) Modified shoe of Brian
5) Nucleo L476RG
6) M2.5 x 8mm Standoff
7) M2.5 x 10mm Standoff
8) M2.5 x 30mm Standoff
9) M2.5 x 6mm Socket Head Cap Screw
10) M2.5 x 8mm Socket Head Cap Screw
11) M2.5 x 10mm Socket Head Cap Screw
12) M2.5 Nylon Lock Nuts
13) M2.5 Nylon Washers
14) Custom Romi to shoe adapter
15) Gearmotor and Encoder assembly
17) Motor driver and PDP for Romi
18) 8-channel QTRX sensor array
19) Bumper Switch Assembley (Right, Left, or both)
20) Assorted tools
21) Attached .txt files
22) Female to Felmale wires
23) Optional HC-05 Bluetooth modules


## **Getting Started:**
To get started follow the set-up instructions provided with the Romi chassis and on the Romi webpage to secure and attach the Motor driver and PDP for Romi, Gearmotor and Encoder assembly, and Romi Drive and caster wheels. The Gearmotor and Encoder assembly should plug directly into the PDP.

Romi should now look like this:
![image](https://github.com/user-attachments/assets/e760a3ce-15c4-42c0-9b98-1cedb14b8d93)

These highlighted section show necessary cable connections for power to the Nucleo, Motor control cables, and Encoder cables for communication between the PDP and our Nucleo. Example cables are shown below.

![image](https://github.com/user-attachments/assets/113104cb-3fd7-4eab-9f95-e6f8b0f85cdb)


Following this step please attach the BNO055 IMU Breakout Board, in the specified location shown below. A different location may be needed depending on the quantity and location of bump sensors. Consider a custom mount on the aft part of Romi as the best solution.

![image](https://github.com/user-attachments/assets/d99e1f5d-8476-43cb-95f0-c8b8beb8c088)

Next step in to wire up the IMU, the necessary pins are power, ground, SDA, SCL, and RST. An example Cable set up is provided below:
![image](https://github.com/user-attachments/assets/5ffcd769-5be7-4e52-a887-3fded771dff7)

Wiring the 8-channel QTRX sensor array comes next, I reccomend creating your cables using a 7x1 joined female end to 7 free ends to enable a solid connection on the array board while giving freedom to use any desired pins on the Nucleo. A pin our of the array board are given below.
![image](https://github.com/user-attachments/assets/ce4e4915-e4b3-4a8e-83b0-4e5d26c08e82)

To install the 8-channel QTRX sensor array, first fish the wire through the highlighted holes on the bottome of the Romi, shown belown, then place the board in the left over gap. You will need to secure the board, however be aware of blocking sensors or potential shorts. I reccomend taping the 7x1 joined adaptor to the standoffs for the nucleo, but do what every feels most secure.

![image](https://github.com/user-attachments/assets/e846cf6a-10cd-4ff1-a0d6-48ee966c80ce)


This is what the bottom of Romi should look like after the instalation.
![image](https://github.com/user-attachments/assets/058e1dd3-efec-4e74-b188-443a04f25f05)

The final step in Romi assebly before wiring is the bump sensors. You are welcome to choose as many or as few as you would like. For our project we chose the Right assembly only. This was doen to avoid having to relocate the IMU. You will need a 4x1 cable and I reccomend having one end of this cable be 1x1s for port avalibility. The attached system should look like this (note this is with both installed)

![image](https://github.com/user-attachments/assets/d4550775-a4a1-40d7-85b7-ee4eda08abd7)

## Wiring Set-Up:
Next step is the most critical to ensure that Romi opperates as intended. Below is the wiring diagram that we used for our project. If different ports are needed please reflect those changes in the code to ensure proper function.

![image](https://github.com/user-attachments/assets/506046b4-3178-4a1f-891e-dd3a5c93631e)


> [!WARNING]
> Make sure to verify all ports, esspecially ground and power, before turning the system on. If not possible damage could occur to the components or sensors.

## Code Set-Up:
After verifying that your physcial pins match those specified in the code, load all of the attached .txt files into your python 3 program of choosing and save the file to the Romi as a .py file. Make sure that the .py file names match those verbatum of those of the .txt files, otherwise erros may occur.

The overall structure of the code to run the Romi around the track involves three states: Left Wheel, Right Wheel, and Velocity Control. The Left Wheel tasks runs the left motor and encoder of the Romi and controls the duty cycle based on a reference velocity specified from the velocity control task and a measured velocity from the left encoder. The Right Wheel tasks similarly runs the right motor and encoder of the Romi, controlling the duty cycle based on the reference velocity and the measured velocity from the left encoder. The Velocity control taks is the larger task, which controlls the overall behavior of the Romi. The velocity control task reads reads the line sensor data, calculates a weighted sum, and specifies a yaw rate based on the value of the weighted sum. Our control structure is a cascaded control structure with the left and right wheel motor controllers on the inner loop in the Left Wheel and Right Wheel tasks. The outer loop of our control system is contained within Task 3 and it involves a longitudinal velocity controller and a yaw rate controller, which feed reference wheel velocities to the other two controllers. All the shares variables, motor objects, and controller must be defined correctly within all of the states to ensure good communication. Thec scheduler included in the cotask and task_share runs the tasks on time at a period of 6 miliseconds for the Left and Right Wheel Encoders and 8 ms for the velocity control task.

## Task Diagram

![Term Project Task Diagram](https://github.com/user-attachments/assets/7e2cb9d2-7e19-4277-a54d-ff991995a10e)

The task diagram shows the interaction between the three different tasks. The left and right wheel reference velocities are shared from the velocity control task, while the measured left and right wheel measured velocities are shared from the left and right wheel tasks respectively to the velocity control task. These velocities allow the controllers for each motor to control the motor speed to match the reference velocity calculated from the yaw rate and linear velocity controllers in the velocity task. Additionally, these share variables allow the yaw rate and linear velocity tasks to update based on the measured velocity from the left and right wheel tasks. The calibration flag, bump flag, and end flag variables are shared from the velocity control task to signal when the IMU has calibrated on startup, when the bump sensors are triggered, and when the Romi has reached the end of the track.

## Left Wheel Task

![Left Wheel FSM](https://github.com/user-attachments/assets/b50e64d3-8943-4cbc-8401-986b2dfd28cc)

The Left Wheel Task Finite State Machine displays the three states within the Left Wheel task. State 0 is simply a setup state that runs only until the calibration flag reads true once the IMU has been calibrated in the Velocity Control task. State 1 is the state where the control of the motor occurs. State one updates the left encoder and calculates the measured velocity of the left wheel. State 1 takes in the shares variable, including the reference velocity of the left wheel from the Velocity Control task, which is fed into the left wheel PI controller. The left wheel controller will return a duty cycle for the motor to keep the measured velocity of the wheel at the reference velocity. Finally, state 1 also puts the velocity of the left wheel into the shares variable to be used in the Velocity Control task. State 2 is used to avoid the wall and return to the start once the bump flag or end flag is true, which has been harcoded within the Velocity Control task, meaning the left wheel task is in an idle state until the bump flag and end flag are false.

## Right Wheel Task

![Right Wheel FSM](https://github.com/user-attachments/assets/a602c13f-b853-402f-b12a-679cf94af513)

Similar to the Left Wheel Task, the Right Wheel Task Finite State Macine shows the three states within the Right Wheel task. State 0 runs and sets up the motor until the calibration flag reads true after the IMU has been calibrated in the Velocity Control Task. State 1 controls the right motor by updating the right aencoder and calculates the measured velocity. It also takes in the reference velocity of the right wheel from the Velocity control task, which is used in the right wheel PI controller. The PI controller returns a duty cycle to update the motor and keep the measured velocity of the right wheel at the reference velocity. State 2 is used to avoid the wall and return to the start once the bump flag or end flag is true, which has been haroded within the Velocity Control task, measning the left wheel task is in an idle state until the bump flag and end flag are flase.

## Velocity Control Task

![Velocity Control FSM](https://github.com/user-attachments/assets/c5533523-61bb-47b6-b4a3-104a45336083)

The Velocity Control Task Finite State Machine shows the 4 states that are within the Velocity Control task. State 0 is a velocity setup task that initlizes the important objects, such as the line sensors, and calirates the IMU. Once the IMU is calibrated, the task will transition to state 1 and it will signal to the Left and Right Wheel Tasks that they must transition to state 1 as well. State 1 is where the majority of the control stucture is taking place. The state reads each of the line sensors, normalizes the reading, and calculates the weighted sum of the line sensor readings. Based on the value of the weighted sum, we update the yaw rate to control the behavior of the motor. If the absolute value of the weighted sum is small drive the motor straight when it is reading equal amounts of black and white on each side of the line sensor array. If the absolute value of the weighted sum is very large, the linear velocity of the Romi robot is decreased for the sharp curves to increase accuracy of reading the tight radii. If it has been less than 2 seconds since the last sharp turn reading from the line sensor array, the Romi will continue to go slow. To ensure that the initial line of the starting box does not affect the robot, a condition has been included that will cause the Romi to continue straight if it reads 3 or more of the sensors over a black line in about 5 seconds after the Romi starts moving. The same logic is implemented to ignore when 5 or more of the sensors read as all black so that the Romi continues along the course track even with large vertical black lines in the path. However, if the bump flag has been triggered and the Romi reads 4 or more line sensors that read black, the Romi has reached the final box, which will cause it to reach state 3. Triggering the bump sensors will trigger the transition to state 2. With the yaw rate determined from the readings of the line sensors, state 1 of the Velocity Control task also inputs the reference linear velocity and yaw rate into the Proporitonal controllers to keep the lienar velocity and yaw rate similar to the reference values. These values of the linear velocity and yaw rate are then decoupled using our decoupling matrix, and are used to calculate the reference left and right wheel velocities for the Left and Right WHeel Task. Finally, state 1 puts the reference left and right wheel velocities into the shares variable to be shared with the other tasks.

State 2 occurs after one of the bump sensors has been triggered, and it causes the Romi to move backwards, then turn left, then move forwards, then turns right and moves forward for a certain amount of time. The duty cycle of the motors are set and tuned so that the Romi will avoid the wall and re-establish its position reading the line sensors. Once this sequence is complete, the variables are reset and the state transitions back to 1. State 3 occurs after the Romi has reached the final box and has read more than 4 black sensors at once, signifying an all black line. Once this occurs, state 3 causes the robot to continue forward for a small amount of time before turning around. The Romi knows when to start turning ased on time, and it will stop turning once the current heading is within 3 degrees of the initial heading we ran. Once the Romi has returned to the start box, the motors are disabled and the program is complete.

## Optional Attachments
In the attached files there is a .STL file that contains an object for a optional mount. This mount has mounting holes for both a single bump sensor and the 8-channel QTRX sensor array. However due to printing challengs we did not implement this feature into our design. However given more time this mout would be a very benifical thing to have. Locating the  8-channel QTRX sensor array out infront of the robot plus closer to the ground woul dhelp with smoother robot movements and clearer line tracking. Additionly by putting the bump sensor our from you eliminate the risk of not contacking the box, reduces the price of ordering both bump sensor assemblies, and the IMU does not need to be relocated.
