import re
import json
import math
import os
from pathlib import Path

# function to convert a number value in a boolean sequence

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
	bool_result=[]	
	for t in range(n):
		if x[t] == '1':
			x_c = True
			bool_result.append(x_c)
		elif x[t] == '0':
			x_c = False
			bool_result.append(x_c)
	return bool_result

try:

# n-upla parameters:
# x0,x1,x2 => battery
# x3,x4,x5,x6 => x_position
# x7,x8,x9,x10 => y_position
# x11 => grasp

# parameters related to the resolution map:
# -(a0,a1) x-axis extremes
# -(b0,b1) y-axis extremes
# - n bit number

# initialise some variables
	n = 4
	a0 = -3.7
	a1 = 28
	b0 = -17
	b1 = 10
	fail = 0
	reached = 0
	trace = []
	init_bat_found = False
	init_pos_found = False
	init_gra_found = False
	count=0
	count_=0
	i=0

# SET HERE THE LOG_FILE FOLDER DIRECTORY
	path = '/home/gianluca/Desktop/MASTER_THESIS/RAL2022-experiments/logs-volume' 

	# keywords to find the lines we are looking for in the log file
	key1 = "Command   : level"
	key2 = "getCurrentPose"
	key3 = "Command   : hasGrasped"

# set the file to analyze
	files = os.listdir(path)
	for file in files:
		count_ = count_+1
		#print(path+"/"+file)
		file_name=Path(path+"/"+file)
# initialize the trace with the zero tuple
		while count < 3:
			with open(file_name) as file_iterator:
				for line in file_iterator:

					if key1 in line and init_bat_found != True:
						nex = next(file_iterator)
						nex_1 = next(file_iterator)
						bat_level = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
						if bat_level != []:
	 						#print('\n- start_battery_state -')
	 						bat_level= bat_level[0]
	 						min_bat = 0
	 						max_bat = 101
	 						n_bit = 3 
	 						x0_x1_x2 = bin_convert(bat_level, min_bat, max_bat, n_bit)
	 						#print(x0_x1_x2)
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

	 						#print('\n- start_position_state: -')
	 						#print(x3_x4_x5_x6_x7_x8_x9_x10)
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
	 						#print('\n- start_grasp_state: -')
	 						#print(x11)
	 						init_gra_found = True
	 						count=count+1

		zero_tupla = x0_x1_x2 + x3_x4_x5_x6_x7_x8_x9_x10 + x11
		trace.append(zero_tupla)
		n_upla = [x0_x1_x2,x3_x4_x5_x6_x7_x8_x9_x10,x11]

	# check for new messages

		with open(file_name) as file_iterator:	
	 		for line in file_iterator:
	 			if fail == 0: 

	 				# check for new battery messages

	 				if key1 in line:
	 					nex = next(file_iterator)
	 					nex_1 = next(file_iterator)
	 					bat_level = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
	 					if bat_level != []:
	 						#print('\n- New Battery Message -')
	 						#print(bat_level)
	 						bat_level=bat_level[0]
	 						if bat_level<10:
	 							fail = 1
	 						min_bat = 0
	 						max_bat = 101
	 						n_bit = 3 
	 						x0_x1_x2 = bin_convert(bat_level, min_bat, max_bat, n_bit)
	 						
	 						# update the trace adding new tupla 

	 						if x0_x1_x2 != n_upla[0]:
	 							#print('\n**update battery**')
	 							n_upla[0] = x0_x1_x2
	 							tupla=n_upla[0]+n_upla[1]+n_upla[2]
	 							#print(tupla)
	 							trace.append(tupla)
	 						else: 
	 							continue

	 				# check for new position messages

	 				if key2 in line:
	 					nex = next(file_iterator)
	 					nex_1 = next(file_iterator)
	 					rob_pose = [float(s) for s in re.findall(r'-?\d+\.?\d*', nex_1)]
	 					if rob_pose != []:
	 						x_pose = rob_pose[0]
	 						y_pose = rob_pose[1]
	 						
	 						if x_pose > 10.8 and y_pose > 2.7:
	 							reached = 1

	 						x_bin = bin_convert(x_pose, a0, a1, n)
	 						y_bin = bin_convert(y_pose, b0, b1, n)
	 						x3_x4_x5_x6_x7_x8_x9_x10 = x_bin + y_bin
	 						
	 						# update the trace adding new tupla
	 					
	 						if x3_x4_x5_x6_x7_x8_x9_x10 != n_upla[1]:
	 							#print('\n**update position**')
	 							n_upla[1] = x3_x4_x5_x6_x7_x8_x9_x10
	 							tupla=n_upla[0]+n_upla[1]+n_upla[2]
	 							#print(tupla)
	 							trace.append(tupla)
	 						else:
	 							continue

	 				# check for new grasp messages

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

	 						# update the trace adding new tupla
	 						
	 						if x11 != n_upla[2]:						
	 							#print('\n**update grasp**')
	 							n_upla[2] = x11
	 							tupla=n_upla[0]+n_upla[1]+n_upla[2]
	 							#print(tupla)
	 							trace.append(tupla)
	 						else:
	 							continue
	 			elif(fail == 1):
	 				break

		#print('\nTrace:\n')
		#print(len(trace))
		#print(trace)

	# save the trace as a json file, if the robot reached the kitchen the task is complete and the trace will be indicate ad trace_s 
	# instead if for some reason the robot don't reach the kicthen the trace is indicate ad trace_f 
		dir_path = "/home/gianluca/Desktop/MASTER_THESIS/json_trace_folder"
		os.makedirs(dir_path, exist_ok=True)
		if fail == 0 and reached == 1:
			print('Trace n.',count_)
			print("SUCCESS")
			with open(os.path.join(dir_path, 'trace'+ str(count_) +'_s.json'), "w") as outfile:
	 			json.dump(trace, outfile)

		elif fail == 1 or reached == 0:
			print('Trace n.',count_)
			print("FAILURE")
			with open(os.path.join(dir_path, 'trace'+ str(count_) +'_f.json'), "w") as outfile:
	 			json.dump(trace, outfile)
		
	# entering except block
except :
	print("\nThe file doesn't exist!")