import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,2*np.pi,100)
y = np.sin(x) + np.random.random(100) * 0.8

def smooth(y, box_pts):

	box = np.ones(box_pts)/box_pts
	#print y
	#print box
	#print box_pts


	y_smooth = np.convolve(y, box, mode='same')

	#print y_smooth

	return y_smooth

#fig = plt.figure('Smoothing')

plt.plot(x, y,'-')
plt.plot(x, smooth(y,3), 'r-', lw=2)
plt.plot(x, smooth(y,15), 'g-', lw=2)

plt.show()
