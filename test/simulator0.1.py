from __future__ import print_function

#from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import random#math
from datetime import datetime


x = 0
y = 0

xy = []
xy_noise = []

footprint = []
footprint_noise = []
footprint_filtered = []
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

def OnClick(event):

	x, y = event.xdata, event.ydata

	#TODO: assert event.xdata, event.ydata not == None,None

	xy = [x,y]
	xy_noise = [x-0.5+random.random(),y-0.5+random.random()]
	xy_filtered = []

	if len(footprint) < 10:

		footprint.append(xy)
		footprint_noise.append(xy_noise)

	else:

		footprint.pop(0)
		footprint_noise.pop(0)

		footprint.append(xy)
		footprint_noise.append(xy_noise)

	footprint_data = np.matrix(footprint)
	footprint_xdata = footprint_data[:,0]
	footprint_ydata = footprint_data[:,1]

	footprint_noise_data = np.matrix(footprint_noise)
	footprint_noise_xdata = footprint_noise_data[:,0]
	footprint_noise_ydata = footprint_noise_data[:,1]

	axes = event.inaxes

	draw_point(axes,footprint_xdata,footprint_ydata,'go','Pose')
	draw_line(axes,footprint_xdata,footprint_ydata,'c--','Ground Truth')
	draw_line(axes,footprint_noise_xdata,footprint_noise_ydata,'y-','Data Noise')

	axes.figure.canvas.draw()

def OnRelease(event):

	pass

def draw_point(axes,x,y,mtype,text):

	axes.plot(x,y,mtype,label=text)
	pass

def draw_line(axes,x,y,mtype,text):

	axes.plot(x,y,mtype,label=text)
	pass

def timer_callback(axes):

	axes.set_title('Date: %s' % datetime.now())
	axes.figure.canvas.draw()

class WorldView():

	def __init__(self):

		#fig = plt.figure('Figure Simulator')

		#self.fig2 = plt.subplot(122, projection = 'polar')
		#plt.title('Polar')

		#fig1,ax = fig.add_subplot(111)
		#fig1 = plt.subplot(111)
		fig, ax = plt.subplots(sharex=True, sharey=True)
		ax.set_title('Figure Simulator')
		ax.axis([-10,10,-10,10])
		ax.set_anchor('C')
		ax.set_title('Mouse Input')
		ax.set_xlabel('Pose X')
		ax.set_ylabel('Pose Y')
		ax.set_xlim(-10,10)
		ax.set_ylim(-10,10)
		ax.set_autoscalex_on(False)
		ax.set_autoscaley_on(False)
		ax.grid(True)

		for direction in ["left", "right", "bottom", "top"]:

			ax.spines[direction].set_visible(False)

		fig.canvas.mpl_connect('figure_enter_event', enter_figure)
		fig.canvas.mpl_connect('figure_leave_event', leave_figure)
		fig.canvas.mpl_connect('axes_enter_event', enter_axes)
		fig.canvas.mpl_connect('axes_leave_event', leave_axes)

		fig.canvas.mpl_connect('button_press_event', OnClick)
		fig.canvas.mpl_connect('button_release_event', OnRelease)

		timer = fig.canvas.new_timer(interval=100)
		timer.add_callback(timer_callback, ax)
		timer.start()

		plt.autoscale(enable=False, axis='both', tight=None)

	def run(self):

		plt.show()

#####################################

world = WorldView()
world.run()
