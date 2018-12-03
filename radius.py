import numpy as np
from skimage.filters import sobel

def reject_outliers(data, m = 2.):
	data = np.array(data)
	d = np.abs(data - np.median(data))
	mdev = np.median(d)
	s = d/mdev if mdev else 0.

	return data[s < m]

def get_center(img_id,center_table):
	my_row = center_table.loc[img_id]
	return int(my_row["x"]), int(my_row["y"])

def dist(p,q):
	return np.sqrt(pow(p[0]-q[0],2) + pow(p[1]-q[1],2))

def find_radii(boundary_function,img_f,init_id,center_table,p=99,verbose=False):
	circle_mask = np.fromfunction(lambda i, j: boundary_function((i,j)), (512,512), dtype='int')
	
	rads = []
	result_rows = []
	img_id = init_id-1
	
	for f in img_f:
		img_id += 1
		img = np.load(f)
		edges = sobel(img,  mask=circle_mask)
		center = get_center(img_id,center_table)
		mod_edges = edges > np.percentile(edges,p)
		boundary_locations = np.array(np.nonzero(mod_edges)).T

		distances = []
		for i,j in boundary_locations:
			distances.append(dist((i,j),(center[1], center[0])))

		#m = 3
		#distances = reject_outliers(distances, m)
		radius = np.median(distances)
		rads.append(radius)
		if verbose:
			print([img_id, radius])
		result_rows.append([img_id, radius])

	return result_rows



