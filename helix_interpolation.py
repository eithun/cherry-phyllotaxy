import numpy as np

def get_helix(theta0, z0, theta1, z1,hand):
	x0, y0 = np.cos(theta0), np.sin(theta0)
	x1, y1 = np.cos(theta1), np.sin(theta1)

	alpha0 = np.arctan2(y0,x0)
	alpha1 = np.arctan2(y1,x1)

	
	cond = theta0 > np.pi and theta1 < np.pi
	if hand == 1:
		cond = theta0 < np.pi and theta1 > np.pi
	

	if cond:
		alpha0 = -np.arctan2(y0, -x0) + np.pi
		alpha1 = -np.arctan2(y1, -x1) + np.pi

	omega = (alpha1 - alpha0) / (z1 - z0)
	phi = (alpha0*z1 - alpha1*z0) / (z1 - z0)

	return (omega, phi)

