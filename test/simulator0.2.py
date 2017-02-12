from __future__ import print_function
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from pykalman import KalmanFilter


import numpy as np
import random#math


mouse_x_now,mouse_y_now = 0,0
update_rate = 4 #Hz

trace_x,trace_y = [],[]
trace_x_noise,trace_y_noise = [],[]
trace_x_filtered,trace_y_filtered = [],[]
trace_noise = []

xy = []
xy_noise = []

status = 0
is_mouse_entered = False
is_mouse_left_clicked,is_mouse_middle_clicked,is_mouse_right_clicked = False,False,False

def enter_axes(event):

	global is_mouse_entered, ax

	if event.inaxes is ax:

		is_mouse_entered = True

	else:

		pass

def leave_axes(event):

	global is_mouse_entered, ax

	if event.inaxes is ax:

		is_mouse_entered = False

	else:

		pass

def enter_figure(event):
	#print('enter_figure', event.canvas.figure)
	event.canvas.figure.patch.set_facecolor('white')
	event.canvas.draw()

def leave_figure(event):
	#print('leave_figure', event.canvas.figure)
	event.canvas.figure.patch.set_facecolor('white')
	event.canvas.draw()

def onClick(event):

	global is_mouse_left_clicked,is_mouse_middle_clicked,is_mouse_right_clicked

	if event.button == 1:

		is_mouse_left_clicked = True

	elif event.button == 2:

		is_mouse_middle_clicked = True

	elif event.button == 3:

		is_mouse_right_clicked = True

	else:

		pass

	#print (is_mouse_left_clicked,is_mouse_middle_clicked,is_mouse_right_clicked)

def onRelease(event):

	global is_mouse_left_clicked,is_mouse_middle_clicked,is_mouse_right_clicked

	is_mouse_left_clicked,is_mouse_middle_clicked,is_mouse_right_clicked = False,False,False

	pass

def draw_point(axes,x,y,mtype,text):

	axes.plot(x,y,mtype,label=text)
	pass

def draw_line(axes,x,y,mtype,text):

	axes.plot(x,y,mtype,label=text)
	pass

def timer_callback(axes):

	global is_mouse_left_clicked,is_mouse_middle_clicked,is_mouse_right_clicked
	global mouse_x_now,mouse_y_now,trace_noise
	global trace_x,trace_y,trace_x_noise,trace_y_noise,trace_x_filtered,trace_y_filtered

	if is_mouse_entered is True:

		trace_x = data_queue(trace_x,mouse_x_now)
		trace_y = data_queue(trace_y,mouse_y_now)

		mouse_x_now_noise = mouse_x_now-1+2*random.random()
		mouse_y_now_noise = mouse_y_now-1+2*random.random()
		trace_x_noise = data_queue(trace_x_noise,mouse_x_now_noise)
		trace_y_noise = data_queue(trace_y_noise,mouse_y_now_noise)


		trace_noise = data_queue(trace_noise,[mouse_x_now_noise,mouse_y_now_noise])
		trace_noise = data_queue(trace_noise,[mouse_x_now_noise,mouse_y_now_noise])
		trace_noise = data_queue(trace_noise,[mouse_x_now_noise,mouse_y_now_noise])
		print (trace_noise)

		kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)
		measurements = [[1,0], [0,0], [0,1]]
		x_filtered = kf.em(measurements).smooth(trace_noise)
		#x_filtered = kf.em(measurements).smooth(trace_x_noise)
		#y_filtered = kf.em(measurements).smooth(trace_y_noise)

		#trace_x_filtered = data_smooth(trace_x_noise,3)#data_queue(trace_x_filtered,mouse_x_now)
		#trace_y_filtered = data_smooth(trace_y_noise,3)#data_queue(trace_y_filtered,mouse_y_now)

		axlines[0].set_xdata(trace_x)
		axlines[0].set_ydata(trace_y)
		axlines[1].set_xdata(trace_x)
		axlines[1].set_ydata(trace_y)
		axlines[2].set_xdata(trace_x_noise)
		axlines[2].set_ydata(trace_y_noise)
		axlines[3].set_xdata(xy_filtered[0])
		axlines[3].set_ydata(xy_filtered[1])

	else:

		pass

	axes.set_title('Date: %s' % datetime.now())
	axes.figure.canvas.draw()


def motion_notify_callback(event):

	global is_mouse_entered,mouse_x_now,mouse_y_now

	if is_mouse_entered is True:

		if event.xdata == None or event.ydata == None:

			pass

		else:

			mouse_x_now,mouse_y_now = event.xdata,event.ydata

	else:

		pass

def data_queue(queue,new):

	if len(queue) < 20:

		queue.append(new)

	else:

		queue.pop(0)
		queue.append(new)

	return queue

def data_smooth(y, box_pts):

	box = np.ones(box_pts)/box_pts

	y_smooth = np.convolve(y, box, mode='same')

	return y_smooth


def animation_init():

	return lines

def animation_update(i):

	return lines


##########################################
fig = plt.figure('Kalman Filter')

ax = fig.add_subplot(121)
ax.set_title('Mouse Input Simulation')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_xlim(0,20)
ax.set_ylim(0,20)
ax.set_autoscalex_on(False)
ax.set_autoscaley_on(False)
ax.grid(True)

axline1, = ax.plot(trace_x,trace_y,'go')
axline2, = ax.plot(trace_x,trace_y,'g-')
axline3, = ax.plot(trace_x_noise,trace_y_noise,'b-')
axline4, = ax.plot(trace_x_filtered,trace_y_filtered,'r-')
axlines = [axline1,axline2,axline3,axline4,]

bx = fig.add_subplot(122)
bx.set_title('Difference Serial')
bx.set_xlabel('Time')
bx.set_ylabel('Error')
bx.set_xlim(0,1)
bx.set_ylim(-10, 10)
bx.set_autoscalex_on(False)
bx.set_autoscaley_on(False)
bx.grid(True)

#bxline1, = bx.plot(data_diff_range, data_diff, 'ro')
#bxline2, = bx.plot(data_smoothed_range, data_smoothed, 'g-')
#bxline3, = bx.plot(data_peak_range, data_peak, 'b*')
#bxlines = [bxline1, bxline2, bxline3, ]

lines = axlines #axlines.append(bxlines)

fig.canvas.mpl_connect('figure_enter_event', enter_figure)
fig.canvas.mpl_connect('figure_leave_event', leave_figure)
fig.canvas.mpl_connect('axes_enter_event', enter_axes)
fig.canvas.mpl_connect('axes_leave_event', leave_axes)

fig.canvas.mpl_connect('button_press_event', onClick)
fig.canvas.mpl_connect('button_release_event', onRelease)

fig.canvas.mpl_connect('motion_notify_event', motion_notify_callback)

timer = fig.canvas.new_timer(interval=1000/update_rate)
timer.add_callback(timer_callback, ax)
timer.start()

ani = animation.FuncAnimation(fig, animation_update, init_func=animation_init, frames=1, interval=100)#, blit=True)

plt.autoscale(enable=False, axis='both', tight=None)
plt.show()
