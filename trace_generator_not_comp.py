import re
import json
import math

# function to convert a number in binary value

def bin_convert(x,a0,a1,n):
	Xn = (x-a0)/(a1-a0)
	Xm = pow(2,n)*Xn
	ix = math.floor(Xm)
	x = bin(ix)
	x = '{:0b}'.format(ix)
	m=len(x)
	while m != n:
		x = "0" + x
		m=m+1
	c=[]	
	for t in range(n):
		if x[t] == '1':
			x_c = True
			c.append(x_c)
		elif x[t] == '0':
			x_c = False
			c.append(x_c)
	return c

try:

# PARAMETRI RELATIVI ALLE COMPONENTI DELLA N-UPLA:
# x0,x1,x2 => battery
# x3,x4,x5,x6 => x_position
# x7,x8,x9,x10 => y_position
# x11 => grasp

# PARAMETRI RELATIVI ALLA MAPPA E ALLA RISOLUZIONE:
# -(a0,a1) estremi sull'asse x 
# -(b0,b1) estremi sull'asse y 
# - n numero di bit
#---------------------
	a0 = -3.5
	a1 = 64
	b0 = -19
	b1 = 17
	n = 4               
#----------------------- 

	key1 = "Command   : level"
	key2 = "getCurrentPose"
	key3 = "Command   : hasGrasped"

	trace = []

	file_name = 'log.txt'
	file_read = open(file_name, "r")
	lines = file_read.readlines()

	init_bat_found = False
	init_pos_found = False
	init_gra_found = False
	count=0

# initialize the trace with the firt tuple

	while count < 3:
		with open(file_name) as file_iterator:
			for line in file_iterator:

				if key1 in line and init_bat_found != True:
					nex = next(file_iterator)
					nex_1 = next(file_iterator)
					bat_level = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
					if bat_level != []:
 						print('\n- start_battery_state -')
 						bat_level= bat_level[0]
 						min_bat = 0
 						max_bat = 101
 						n_bit = 3 
 						x0_x1_x2 = bin_convert(bat_level, min_bat, max_bat, n_bit)
 						print(x0_x1_x2)
 						init_bat_found = True
 						count=count+1

				if key2 in line and init_pos_found != True:
 					nex = next(file_iterator)
 					nex_1 = next(file_iterator)
 					rob_pose = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
 					
 					if rob_pose != []:
 						x_pose = rob_pose[0]
 						y_pose = rob_pose[1]
 					
 						x_bin = bin_convert(x_pose, a0, a1, n)
 						y_bin = bin_convert(y_pose, b0, b1, n)
 						x3_x4_x5_x6_x7_x8_x9_x10 = x_bin + y_bin

 						print('\n- start_position_state: -')
 						print(x3_x4_x5_x6_x7_x8_x9_x10)
 						init_pos_found = True
 						count=count+1

				if key3 in line and init_gra_found != True:
 					nex = next(file_iterator)
 					nex_1 = next(file_iterator)
 					grasp = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
 					if grasp != []: 
 						if grasp == [27503]:
 							grasp_var = True
 						else:
 							grasp_var = False
 						x11 = [grasp_var]
 						print('\n- start_grasp_state: -')
 						print(x11)
 						init_gra_found = True
 						count=count+1

	tupla = x0_x1_x2 + x3_x4_x5_x6_x7_x8_x9_x10 + x11
	print('\nInitial state [battery_state, position_state, grasp_state]:\n')
	print(tupla)
	trace.append(tupla)
	n_upla = [x0_x1_x2,x3_x4_x5_x6_x7_x8_x9_x10,x11]

# check for new messages

	with open(file_name) as file_iterator:
 		for line in file_iterator:

 			if key1 in line:
 				nex = next(file_iterator)
 				nex_1 = next(file_iterator)
 				bat_level = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
 				if bat_level != []:
 					#print('\n- New Battery Message -')
 					bat_level=bat_level[0]
 					min_bat = 0
 					max_bat = 101
 					n_bit = 3 
 					x0_x1_x2 = bin_convert(bat_level, min_bat, max_bat, n_bit)
 					#print(x0_x1_x2)
 					print('\n**update battery**')
 					n_upla[0] = x0_x1_x2
 					tupla=n_upla[0]+n_upla[1]+n_upla[2]
 					print(tupla)
 					trace.append(tupla)

 			if key2 in line:
 				nex = next(file_iterator)
 				nex_1 = next(file_iterator)
 				rob_pose = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
 				if rob_pose != []:
 					x_pose = rob_pose[0]
 					y_pose = rob_pose[1]
 					
 					x_bin = bin_convert(x_pose, a0, a1, n)
 					y_bin = bin_convert(y_pose, b0, b1, n)
 					x3_x4_x5_x6_x7_x8_x9_x10 = x_bin + y_bin
 					#print('\n- New Position Message: -')
 					print('\n**update position**')
 					n_upla[1] = x3_x4_x5_x6_x7_x8_x9_x10
 					tupla=n_upla[0]+n_upla[1]+n_upla[2]
 					print(tupla)
 					trace.append(tupla)
 			
 			if key3 in line:
 				nex = next(file_iterator)
 				nex_1 = next(file_iterator)
 				grasp = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
 				if grasp != []: 
 					#print('\n- New Grasp Message -')
 					if grasp == [27503]:
 						grasp_var = True
 					else:
 						grasp_var = False
 					x11 = [grasp_var]			
 					print('\n**update grasp**')
 					n_upla[2] = x11
 					tupla=n_upla[0]+n_upla[1]+n_upla[2]
 					print(tupla)
 					trace.append(tupla)
	print('\nTrace:\n')
	print(trace)

# produce the total trace
	
	with open("not_comp_trace.json", "w") as outfile:
 		json.dump(trace, outfile)

	# entering except block
except :
	print("\nThe file doesn't exist!")
