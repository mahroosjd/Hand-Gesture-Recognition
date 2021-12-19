
# SKIN PIXEL DETECTION- Method 1
import numpy as np
import cv2 as cv

img = cv.imread('hand_5.jpg')

print("Image Properties")
print("- Number of Pixels: " + str(img.size))
print("- Shape Dimensions: " + str(img.shape))

b,g,r = cv.split(img)

#CONVERSION FROM RGB TO YCBCR
convrtd = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
cv.imshow('YCbCr', convrtd)

Y, Cr, Cb = cv.split(convrtd)

# SKIN PIXEL DETECTION
for b in range(img.shape[0]):
		for a in range(img.shape[1]):
			if Cb[b][a]>=77 and Cb[b][a]<=127 and Cr[b][a]>=133 and Cr[b][a]<=173:
			#if Cb[b][a]>=100 and Cb[b][a]<=150 and Cr[b][a]>=150 and Cr[b][a]<=200:
				convrtd[b][a][0]=255
				convrtd[b][a][1]=255
				convrtd[b][a][2]=255
			else: 
				convrtd[b][a][0]=0
				convrtd[b][a][1]=0
				convrtd[b][a][2]=0
# DISPLAY SEGMENTED IMAGE	
cv.imshow('imsegmen',convrtd)		

#MORPHOLOGICAL FILTERING TO REMOVE NOISE	

structel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(2,2)) #Defining Structural Element for Opening
opened = cv.morphologyEx(convrtd, cv.MORPH_OPEN, structel) #opening operation
cv.imshow('After opening',opened)

structel2 = cv.getStructuringElement(cv.MORPH_ELLIPSE,(6,6)) #Defining a bigger structural element for Closing
closeaftropen = cv.morphologyEx(opened, cv.MORPH_CLOSE, structel2) #closing operation
cv.imshow('Closing After Opening',closeaftropen)

#FINDING THE CONTOURS OF THE BLOB
img2 = img
closeaftropen = cv.cvtColor(closeaftropen, cv.COLOR_BGR2GRAY)

contours, hierarchy = cv.findContours(closeaftropen, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)  #cv.RETR_TREE / cv.RETR_EXTERNAL
lngth = len(contours)
print("Number of contours found:"+ str(lngth))

#FINDING THE PERIMETER OF LARGEST CONTOUR 

arcs = []
for i in range(lngth):
	arc = cv.arcLength(contours[i],True)
	arcs.append(arc)

c = max(arcs)
indx = arcs.index(c)
print("Contour Number "+str(indx)+ " is the longest") 

cv.drawContours(img2, contours, -1, (0,0,255), 3)
cv.imshow('Contour',img2)


#FINDING THE IMAGE CENTROID

M = cv.moments(contours[indx])
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
print(str(cX) + " is the x coordinate of contour/hand centre") 
print(str(cY) + " is the Y coordinate of contour/hand centre") 


dist=[]
cont = contours[indx]
num_points=len(cont)
print(num_points)
print(cont)

for p in range(num_points):
	
	dist.append((cX-cont[p][0][0])**2+(cY-cont[p][0][1])**2)

dist2 = np.sqrt(dist)
maxd = max(dist2)
print(maxd)
print(dist2)
indx2 = np.where(dist2==maxd)
print(type(indx2))



h = int(indx2[0])

print(h)

cv.circle(img, (cX, cY), 10, (255, 0, 0), -1)
cv.circle(img, (cont[h][0][0],cont[h][0][1]),10,(0,255,0), -1)
cv.imshow('Centroid',img)

x = img.shape[0]
y = img.shape[1]

#SHIFTING FILLED HAND CONTOUR TO A BLACK IMAGE BACKGROUND

black_backgrnd = np.zeros((x,y,3), dtype="uint8")
cv.drawContours(black_backgrnd, [contours[indx]], -1, (255,255,255), thickness=-1)

cv.imshow('Hand against Black Background',black_backgrnd)

#CREATING A CIRCULAR MASK

mask = np.zeros((x,y,3), dtype="uint8")
cv.circle(mask,(cX, cY),int(0.7*maxd),(255,255,255),4)
cv.imshow('Mask',mask)

finger_count = cv.bitwise_and(black_backgrnd,mask)

cv.imshow('Count Fingers',finger_count)

#COUNTING THE LINE SEGMENTS TO GET THE NUMBER OF FINGERS
finger_count = cv.cvtColor(finger_count, cv.COLOR_BGR2GRAY)
contours2, hierarchy2 = cv.findContours(finger_count, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
finger_num = len(contours2)
finger_num = finger_num-1 #Subtracting the segment detected for Wrist Section
print("Number of open fingers found in the image:"+ str(finger_num))

cv.waitKey(0)


