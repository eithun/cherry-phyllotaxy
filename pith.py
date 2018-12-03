# Find center using initial guess
import numpy as np

# Load image from npy
def get_image(f):
	A = np.load(f)
	return np.array(A)

# A cross pixel-relation
def cross_stencil(idx):
	return [[idx[0]+1, idx[1]], [idx[0], idx[1]+1],
		[idx[0]-1, idx[1]],[idx[0], idx[1]-1]]

# Center finding algorithm
def find_center_of_slice(img, seed, lower_bound,boundary_function,verbose=False):
	idx_queue = [seed]
	img_shape = img.shape
	img_marks = np.zeros(img_shape)
	img_marks[tuple(seed)] = 1

	if verbose:
		print("Finding region...")
	while(idx_queue):
		idx = idx_queue[0]
		tidx = tuple(idx)
		img_val = img[tidx]

		# We found a dark cell!
		if (img_val >= lower_bound):
			break

		# Add neighbors to queue
		new_idxs = cross_stencil(idx)

		for new_idx in new_idxs:
			if boundary_function(new_idx):
				new_tidx = tuple(new_idx)
				if not img_marks[new_tidx]:
					idx_queue.append(new_idx)
					img_marks[new_tidx] = 1

		del idx_queue[0]

	if verbose:
		print("Exploring region...")

	# Start at this point
	new_seed = idx_queue[0]
	region_pts = [new_seed]
	idx_queue = [new_seed]
	img_marks[tuple(idx_queue[0])] = 2

	# Search for closed region 
	while (idx_queue):
		idx = idx_queue[0]
		img_val = img[tuple(idx)]

		# We found a dark cell!
		if (img_val >= lower_bound):
			img_marks[tuple(idx)] = 3
			region_pts.append(idx)

			# Add neighbors to queue
			new_idxs = cross_stencil(idx)

			for new_idx in new_idxs:
				if boundary_function(new_idx):
					new_tidx = tuple(new_idx)
					if img_marks[new_tidx] == 0:
						idx_queue.append(new_idx)
						img_marks[new_tidx] = 2

		del idx_queue[0]

	#plt.imshow(img_marks, cmap=plt.cm.Greys)
	#plt.imshow(org_img, cmap=plt.cm.Greys,alpha=0.3)
	#plt.colorbar()
	#plt.show()

	center_point = [0,0]
	for idx in region_pts:
		center_point[0] += idx[0]
		center_point[1] += idx[1]
	center_point[0] = round(center_point[0]/len(region_pts))
	center_point[1] = round(center_point[1]/len(region_pts))


	return (len(region_pts), center_point)


# Loop over many slices
def find_center(filenames, seed, lower_bound, boundary_function=None,init_id=100,verbose=False):
	result_rows = []

	if boundary_function == None:
		boundary_function = lambda x: True

	#for i in range(100,1811,1): #range(100,0,-1): #1851 (1871)??
	i = init_id-1
	for f in filenames:
		i+=1
		if verbose:
			print("Trying file",f)
			print("Using seed",seed)
		img = -1 * get_image(f)
		org_img = np.copy(img)
		num_pts, center_point = find_center_of_slice(img, seed, lower_bound,boundary_function,verbose)

		if verbose:
			print("Number of center points:",num_pts)
			print("Center:",center_point)
		seed = center_point

		#import matplotlib.pyplot as plt
		#import matplotlib.colors
		#plt.cla()
		#plt.plot(center_point[1], center_point[0], marker='o', markersize=10, color="red")
		#plt.imshow(org_img, cmap=plt.cm.Greys)
		#plt.savefig("../cherry_log/slice"+str(i).zfill(4)+".png")

		###matplotlib.image.imsave("polar"+str(img_id).zfill(4)+'.tif', new_im )

		result_rows.append([i, center_point[1], center_point[0], num_pts])


	return result_rows
