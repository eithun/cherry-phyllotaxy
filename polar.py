# Save ploar verion at fixed radius

import numpy as np
import multiprocessing

def get_center(img_id):
	my_row = center_table.loc[img_id]
	return int(my_row["x"]), int(my_row["y"])

def get_image(img_id):
	return np.load("../data/cherry_stump/processed/cherry"+str(img_id).zfill(4)+".npy")

def get_radius(img_id):
	return float(radius_table.loc[img_id]['r'])


# Parameters for coordinate conversion
theta_dim = 512
r_dim = 512 
theta_max = 2 * np.pi

def save_polar(img_id):
	y0,x0 = get_center(img_id)
	im = get_image(img_id)
	r_max = get_radius(img_id)#160#
	#r_max = min(x0,y0,abs(x0 - im.shape[0]),abs(y0 - im.shape[1])) - 1
	
	new_im = np.zeros((r_dim, theta_dim))
	
	for r_idx in range(r_dim):
		r = (r_idx / r_dim) * r_max
		for theta_idx in range(theta_dim):
			theta = (theta_idx / theta_dim) * theta_max
			x = x0 + r * np.cos(theta)
			y = y0 + r * np.sin(theta)

			# TODO: check that the new index is valid
			new_im[r_idx, theta_idx] = im[int(round(x)), int(round(y))]

	#matplotlib.image.imsave("polar"+str(img_id).zfill(4)+'.tif', new_im )
	np.save(file_prefix + "/rad_polar"+str(img_id).zfill(4)+'.npy', new_im)



def save_polar_all(file_front,center_table_in,radius_table_in,ids,num_cores = 8):
	global center_table 
	global radius_table 
	global file_prefix

	center_table = center_table_in
	radius_table = radius_table_in
	file_prefix = file_front

	# Parallelize!
	pool = multiprocessing.Pool(num_cores)
	pool.map(save_polar, ids)

