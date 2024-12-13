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
23) Optinal HC-05 Bluetooth modules


## **Getting started:**
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

## Wiring set-up:
Next step is the most critical to ensure that Romi opperates as intended. Below is the wiring diagram that we used for our project. If different ports are needed please reflect those changes in the code to ensure proper function.

![image](https://github.com/user-attachments/assets/c73e865e-4d4f-451e-8366-c2fec6e79a89)

> [!WARNING]
> Make sure to verify all ports, esspecially ground and power, before turning the system on. If not possible damage could occur to the components or sensors.

## Code set-up:
After verifying that your physcial pins match those specified in the code, load all of the attached .txt files into your python 3 program of choosing and save the file to the Romi as a .py file. Make sure that the .py file names match those verbatum of those of the .txt files, otherwise erros may occur.

