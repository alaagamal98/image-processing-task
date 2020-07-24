from transform import four_point_transform
import argparse
import cv2
import imutils

def BuildArgparser():
    """
    This function is specified for determining the image that th top
    view will be constructed from.
    """
    parser = argparse.ArgumentParser()    
    parser.add_argument("-i", "--image", required = True, help = "Path to the image to construct top view from.")
    args = parser.parse_args()
    return args

def FindContour(image):
	"""
    This function is specified for determining the contour of the box
	in order to know the coordinates of the box in the image.
    """	
	# convert the image to grayscale, blur it, and find edges
	# in the image.
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
	edged_image = cv2.Canny(blurred_image, 75, 200)
	# find the contours in the edged image, keeping only the
	# largest ones.
	contours = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
	# loop over the contours
	for c in contours:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if our approximated contour has four points, then we
		# can assume that we have found our required contour
		if len(approx) == 4:
			box_contour = approx
			break
	return box_contour.reshape(4, 2)

def CalculateRoadWidth(image, box_width_px):
	"""
    This is for calculating the real width of the road from
	knowing the value of the real width of the box, the width of 
	the box in pixels in the image, and the width of the road in 
	pixels in the image.
    """
	box_width = 75
	road_width_px = image.shape[0]
	road_width = box_width * road_width_px / box_width_px
	return road_width

def PrintandDisplay(image, warped_image, road_width):
	"""
    This is for viewing the original and the top view image
	and for printing the value of the road width.
    """
	print("The Width of The Road is Nearly: {} Meters".format(road_width/100))
	cv2.imshow("Original", image)
	cv2.imshow("Scanned", warped_image)
	cv2.waitKey(0)


if __name__ == '__main__':

	args = BuildArgparser()
	image = cv2.imread(args.image)
	box_contour = FindContour(image)
	warped_image, box_width_px = four_point_transform(image,box_contour)
	road_width = CalculateRoadWidth(image, box_width_px)
	PrintandDisplay(image, warped_image, road_width)
