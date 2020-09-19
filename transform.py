import numpy as np
import cv2

def order_points(points):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left.
	ordered_points = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum.
	s = points.sum(axis = 1)
	ordered_points[0] = points[np.argmin(s)]
	ordered_points[2] = points[np.argmax(s)]

	# now, ideally from the website i referenced from, 
	# top-right point should have the smallest difference,
	# whereas the bottom-left should have the largest difference
	
	# but this is not the case here, when i tried the difference method
	# the picture had the wrong dimensions as the smallest difference is not 
	# top-right and the largest difference is not bottom-left, so i 
	# debugged the code i found out that the contour function returns 
	# the points (top left, bottom left, bottom right, top right) 
	# so i coded the order points accordingly.
	ordered_points[1] = points[3]
	ordered_points[3] = points[1]
	# return the ordered coordinates.
	return ordered_points

def four_point_transform(image, points):
	# obtain a consistent order of the points and unpack them
	# individually.
	ordered_points = order_points(points)
	(tl, tr, br, bl) = ordered_points
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates.
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view".
	destination_points = np.array([tl,
		[maxWidth+tl[0] , tl[1]],
		[maxWidth+tl[0] , maxWidth+tl[1]],
		[tl[0], maxWidth+tl[1]]], dtype = "float32")
		
	# compute the perspective transform matrix and then warp it to
	# the whole image size.
	transform_matrix = cv2.getPerspectiveTransform(ordered_points, destination_points)
	warped_image = cv2.warpPerspective(image, transform_matrix, image.shape[:2][::-1])
	# return the warped image and the box of the contour to calculate
	# the width of the road.
	return warped_image, maxWidth