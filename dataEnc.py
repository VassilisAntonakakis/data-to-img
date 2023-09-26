import sys
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#check if the input file name is provided
if len(sys.argv) < 2:
    print("Usage: python dataEnc.py <input file name>")
    sys.exit(0)

#get the input file name from the command line
inputFile = sys.argv[1]

#locate the file in the computer
if not os.path.isfile(inputFile):
    print("File not found")
    sys.exit(0)
else:
    print("File found")
    filepath = os.path.abspath(inputFile)

file = open(filepath, "rb")

#read the file into a byte array
data = file.read()

#close file
file.close()

gray_values = np.frombuffer(data, dtype=np.uint8)


#calculate the size of the equivalent 2d array
size = int(np.sqrt(len(gray_values)))

#create a header for the image with the original file type preceded and followed by $
header = "$" + inputFile[-3:] + "$"

#convert the header into a int array
header_values = np.frombuffer(header.encode(), dtype=np.uint8)

#add the header to the start of the array
gray_values = np.insert(gray_values, 0, header_values)

while size*size < len(gray_values):
    size += 1

print("data from file: " + str(gray_values))

#add zeros to the start of the array to make it a perfect square
while len(gray_values) < size*size:
    gray_values = np.insert(gray_values, 0, 0)

print("data after adding zeros: " + str(gray_values))
#reshape the 1d array into a 2d array
gray_img = gray_values.reshape(size, size)

print("Image: " + str(gray_img))

print("Image size: " + str(gray_img.shape))
#check if the image is created
if gray_img is None:
    print("Image not created")
    sys.exit(0)
else:
    print("Image created")
    print("image: " + str(gray_img))
    #save the image as a tiff file with the file name from the command line and the adittion of "_enc.tif"
    cv.imwrite(inputFile[:-4] + "_enc.tif", gray_img)

#show the image in a window with matplotlib
plt.imshow(gray_img, cmap='gray', vmin=0, vmax=255)
plt.show()

