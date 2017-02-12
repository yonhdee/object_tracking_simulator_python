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

#axe = np.linspace(0.0, 5.0)

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
	event.canvas.figure.patch.set_facecolor('green')
	event.canvas.draw()

def leave_figure(event):
	#print('leave_figure', event.canvas.figure)
	event.canvas.figure.patch.set_facecolor('white')
	event.canvas.draw()


def OnClick(event):

	#print (event)
	#print (event.x, event.y)
	x, y = event.xdata, event.ydata

	#assert ((x == None) or (y == None))

	xy = [x,y]
	xy_noise = [x-0.5+random.random(),y-0.5+random.random()]
	xy_filtered = []

	if len(footprint) < 4:

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

	#print (xy)
	#print ('x',footprint_data[:,0])
	#print ('y',footprint_data[:,1])
	#print (len(footprint))

	draw_point(x,y,'go','Pose')#plt.plot(x,y,'go',label='pose')
	draw_line(footprint_xdata,footprint_ydata,'c--','Ground Truth')#plt.plot(footprint_xdata,footprint_ydata,'c-',label='ground truth')
	draw_line(footprint_noise_xdata,footprint_noise_ydata,'y-','Data Noise')#plt.plot(footprint_noise_xdata,footprint_noise_ydata,'r-',label='footprint noise')


def OnRelease(event):

	pass

def draw_point(x,y,mtype,text):

	plt.plot(x,y,mtype,label=text)
	pass

def draw_line(x,y,mtype,text):

	plt.plot(x,y,mtype,label=text)
	pass

def timer_callback(axes):

	axes.set_title(datetime.now())
	axes.figure.canvas.draw()


class Reciever():

	buffsize = 90

	def __init__(self):

		self.data = []
		pass

	def queue(self, incoming):

		if len(self.data) < buffsize:

			self.data.append(incoming)

		else:

			self.data.pop(0)
			self.data.append(incoming)

	def callback(self,msg):

		frame = msg#.

		self.queue(frame)


class WorldView():

	def __init__(self):

		#fig = plt.figure('Figure Simulator')

		#self.fig2 = plt.subplot(122, projection = 'polar')
		#plt.title('Polar')

		#fig1,ax = fig.add_subplot(111)
		#fig1 = plt.subplot(111)
		fig, ax = plt.subplots(sharex=True, sharey=True)
		ax.set_title('Figure Simulator')
		plt.title('Linar')
		plt.axis([-8,8,-8,8])

		#fig.canvas.mpl_connect('figure_enter_event', enter_figure)
		#fig.canvas.mpl_connect('figure_leave_event', leave_figure)
		fig.canvas.mpl_connect('axes_enter_event', enter_axes)
		fig.canvas.mpl_connect('axes_leave_event', leave_axes)

		fig.canvas.mpl_connect('button_press_event', OnClick)
		fig.canvas.mpl_connect('button_release_event', OnRelease)

		timer = fig.canvas.new_timer(interval=100)
		timer.add_callback(timer_callback, ax)
		timer.start()
		#drawid = fig.canvas.mpl_connect('draw_event', start_timer)


	#def start_timer(evt):

	#	self.timer.start()
	#	fig.canvas.mpl_disconnect(drawid)

	def run(self):

		plt.show()

		#while True:

			#self.fig1.plot(xy)
			#plt.plot(xy)
			#plt.show()
			#plt.pause(0.1)

#####################################

world = WorldView()
world.run()
