from __future__ import print_function
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
from scipy import signal

import random
import math

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

x = 0
y = 0

scan_range = 360#120
scan_distance = 5.0
frame_rate = 1

user_found = False
user_size_max = 7
user_size_min = 5
user_arm_size= 1
user_arm_size_max = 2
user_arm_size_min = 1
user_distance_diff = 0.2

data = np.zeros(scan_range)
data_range = np.linspace(1,scan_range,scan_range)

data_user_mask = np.ones(scan_range)

data_diff = np.zeros(scan_range-1)
data_diff_range = np.linspace(1,scan_range-1,scan_range-1)

data_smoothed = np.zeros(scan_range)
data_smoothed_range = np.linspace(1,scan_range,scan_range)

data_peak = np.zeros(scan_range)
data_peak_range = np.linspace(1,scan_range,scan_range)

status = 0

def enter_axes(event):
	#print('enter_axes', event.inaxes)
	event.inaxes.patch.set_facecolor('white')
	event.canvas.draw()

def leave_axes(event):
	#print('leave_axes', event.inaxes)
	event.inaxes.patch.set_facecolor('white')
	event.canvas.draw()

def enter_figure(event):
	#print('enter_figure', event.canvas.figure)
	event.canvas.figure.patch.set_facecolor('white')
	event.canvas.draw()

def leave_figure(event):
	#print('leave_figure', event.canvas.figure)
	event.canvas.figure.patch.set_facecolor('white')
	event.canvas.draw()

def onClick(event):

	global data

	if event.xdata == None or event.ydata == None:

		data = data_reset(data)

	else:

		x, y = int(round(event.xdata)), event.ydata

		if event.button == 1:

			data = data_reset(data)

			data = data_add_people(data, x, y)

		elif event.button == 3:

			data = data_add_people(data, x, y)

		elif event.button == 2:

			data = data_smooth(data,5)

		else:

			pass

	data_diff = np.diff(data)
	data_smoothed = data_smooth(data,5)
	data_smoothed = data_smooth(data,5)
	#data_peak = data_findpeak(data_smoothed)
	data_peak = data_detect(data)

	#print (data - data_peak)
	axlines[0].set_ydata(data)
	bxlines[0].set_ydata(data_diff)
	bxlines[1].set_ydata(data_smoothed)
	bxlines[2].set_ydata(data_peak)

def onRelease(event):

	pass

def data_add_people(data, x, y):

	x_offset = int(round(user_size_max/2))

	if y <= scan_distance:

		data[x-x_offset:x+x_offset+1] = [y]*user_size_max

	else:

		data[x-x_offset:x+x_offset+1] = [0]*user_size_max

	return data

def data_reset(data):

	data = np.zeros(scan_range)

	return data

def data_smooth(y, box_pts):

	box = np.ones(box_pts)/box_pts

	y_smooth = np.convolve(y, box, mode='same')

	return y_smooth

def data_findpeak(data):

	peakind = signal.find_peaks_cwt(data, np.arange(1,5))

	data_out = np.zeros(scan_range)

	#TODO: data_mask_generate(data,mask)
	for index in peakind:

		data_out[index-1] = 1
		index += 1

	return data_out

def data_mask_generate(data,mask):

	data_out = np.zeros(scan_range)

	for index in mask:

		data_out[int(index-1)] = 1
		index += 1

	return data_out

def data_detect(data):

	global user_found, data_user_mask

	if user_found == False:

		#Finding objects
		data_diff_left = np.diff(data)
		data_diff_left = np.append(data_diff_left,0)

		data_ = data[::-1]
		data_diff_right = np.diff(data_)
		data_diff_right = np.append(data_diff_right,0)

		data_mask_left = data_object_filter(data_diff_left)
		data_mask_right = data_object_filter(data_diff_right)
		data_object_mask = data_mask_left * data_mask_right[::-1]

		#Checking for object_info
		object_info = data_object_detect(data,data_object_mask)
		object_info_matrix = np.matrix(object_info)

		#Picking up The One by Finding nearest object
		theone_dis_array = object_info_matrix[:,1]
		theone_index = theone_dis_array.argmax()
		theone = object_info[theone_index]

		#The one mask
		data_theone = data_crop(data_object_mask,theone)
		#The user_mask for nearest search in next frame
		data_user_mask = data_crop(data_object_mask,[theone[0],theone[1],theone[2],theone[3]-10,theone[4]+10,theone[5]])

		user_found = True

		print ('Tracking')

	elif user_found == True:

		data = data * data_user_mask

		data_diff_left = np.diff(data)
		data_diff_left = np.append(data_diff_left,0)

		data_ = data[::-1]
		data_diff_right = np.diff(data_)
		data_diff_right = np.append(data_diff_right,0)

		data_mask_left = data_object_filter(data_diff_left)
		data_mask_right = data_object_filter(data_diff_right)
		data_object_mask = data_mask_left * data_mask_right[::-1]

		object_info = data_object_detect(data,data_object_mask)

		if object_info == []:

			user_found = False
			#The user_mask reset
			data_user_mask = np.ones(scan_range)

			print ('Lost')

		else:

			object_info_matrix = np.matrix(object_info)

			#Picking up The One by Finding nearest object
			theone_dis_array = object_info_matrix[:,1]
			theone_index = theone_dis_array.argmax()
			theone = object_info[theone_index]

			#The one mask
			data_theone = data_crop(data_object_mask,theone)

			user_found = True
			#The user_mask for nearest search in next frame
			data_user_mask = data_crop(data_object_mask,[theone[0],theone[1],theone[2],theone[3]-10,theone[4]+10,theone[5]])

		#object_info_matrix = np.matrix(object_info)

		#print (object_info)

		#Picking up The One by Finding nearest object
		#theone_dis_array = object_info_matrix[:,1]
		#theone_index = theone_dis_array.argmax()
		#theone = object_info[theone_index]

		#The one mask
		#data_theone = data_crop(data_object_mask,theone)
		#The user_mask for nearest search in next frame
		#data_user_mask = data_crop(data_object_mask,[theone[0],theone[1],theone[2],theone[3]-10,theone[4]+10,theone[5]])

		#user_found == True

	else:

		pass

	return data_user_mask

def data_object_filter(data):

	data_out = np.zeros(scan_range)
	data_out_range = np.linspace(1,scan_range,scan_range)

	is_object = False

	for index in data_out_range:

		if is_object == True:

			if data[int(index-1)] <= -user_distance_diff:

				is_object = False

			else:

				pass

			data_out[int(index-1)] = 1

		else:

			if data[int(index-1)] >= user_distance_diff:

				is_object = True

		index += index

	return data_out

def data_object_detect(data_raw,data):

	data_diff = np.diff(data)
	data_diff = np.append(data_diff,0)

	data_out = np.zeros(scan_range)
	data_out_range = np.linspace(1,scan_range,scan_range)

	is_object = False
	list_object_info = []
	object_center, object_distance, object_type, object_leftedge, object_rightedge, object_width = 0,0,0,0,0,0

	for index in data_out_range:

		if is_object == True:

			if data_diff[int(index-1)] <= -user_distance_diff:

				is_object = False
				object_rightedge = int(index-1)
				object_width = object_rightedge - object_leftedge
				object_center = int(round((object_rightedge+object_leftedge)/2))
				object_distance = data_raw[int(object_center-1)]

				if object_width>0 and object_width<=user_arm_size:

					object_type = 2

				elif object_width>user_arm_size and object_width <= user_size_min:

					object_type = 3

				elif object_width>user_size_min and object_width <= user_size_max:

					object_type = 1

				else:

					object_type = 0

				list_object_info.append([object_center,object_distance,object_type,object_leftedge,object_rightedge,object_width])

			else:

				pass

			data_out[int(index-1)] = 1

		else:

			if data_diff[int(index-1)] >= user_distance_diff:

				is_object = True
				object_leftedge = int(index-1)

		index += index

	return list_object_info

def data_crop(data,config):

	#object_center, object_distance, object_type, object_leftedge, object_rightedge, object_width
	mask_ = range(config[3],config[4]+1,1)

	data_out = data_mask_generate(data,mask_)

	return data_out

def timer_callback(axes):

	axes.set_title('Click Input Simulation. Time: %s' % datetime.now())
	axes.figure.canvas.draw()

def animation_init():

	return lines

def animation_update(i):

	return lines


#####################################
fig = plt.figure('Figure Simulator')

ax = fig.add_subplot(211)
ax.set_title('Click Input Simulation')
ax.set_xlabel('Range')
ax.set_ylabel('Distance')
ax.set_xlim(0, scan_range)
ax.set_ylim(-0.2, scan_distance+0.2)
ax.set_autoscalex_on(False)
ax.set_autoscaley_on(False)
ax.grid(True)

axline1, = ax.plot(data_range, data,'go')
axlines = [axline1, ]

bx = fig.add_subplot(212)
bx.set_title('Difference Serial')
bx.set_xlabel('Range')
bx.set_ylabel('Difference')
bx.set_xlim(0, scan_range)
bx.set_ylim(-1.2*scan_distance, 1.2*scan_distance)
bx.set_autoscalex_on(False)
bx.set_autoscaley_on(False)
bx.grid(True)

bxline1, = bx.plot(data_diff_range, data_diff, 'ro')
bxline2, = bx.plot(data_smoothed_range, data_smoothed, 'g-')
bxline3, = bx.plot(data_peak_range, data_peak, 'b*')
bxlines = [bxline1, bxline2, bxline3, ]

lines = axlines.append(bxlines)

#fig.canvas.mpl_connect('figure_enter_event', enter_figure)
#fig.canvas.mpl_connect('figure_leave_event', leave_figure)
#fig.canvas.mpl_connect('axes_enter_event', enter_axes)
#fig.canvas.mpl_connect('axes_leave_event', leave_axes)

fig.canvas.mpl_connect('button_press_event', onClick)
fig.canvas.mpl_connect('button_release_event', onRelease)

timer = fig.canvas.new_timer(interval=100)
timer.add_callback(timer_callback, ax)
timer.start()

ani = animation.FuncAnimation(fig, animation_update, init_func=animation_init, frames=1, interval=100)
#ani.save('object_tracking.mp4', writer=writer)

plt.autoscale(enable=False, axis='both', tight=None)
plt.show()
