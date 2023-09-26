import sys
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#check if the input file name is provided
if len(sys.argv) < 2:
    print("[!]Usage: python dataEnc.py <input file name>")
    sys.exit(0)

#get the input file name from the command line
inputFile = sys.argv[1]

#locate the file in the computer
if not os.path.isfile(inputFile):
    print("[-]File not found")
    sys.exit(0)
else:
    print("[+]File found")
    filepath = os.path.abspath(inputFile)

#start timer
start = cv.getTickCount()

print("[!]Reading file")
file = open(filepath, "rb")

#read the file into a byte array
data = file.read()

#close file
file.close()

gray_values = np.frombuffer(data, dtype=np.uint8)

print("[!]Calculating size of the image")
#calculate the size of the equivalent 2d array
size = int(np.sqrt(len(gray_values)))

print("[!]Creating image header")
#create a header for the image with the original file type preceded and followed by $
header = "$" + inputFile[-3:] + "$"

#convert the header into a int array
header_values = np.frombuffer(header.encode(), dtype=np.uint8)

#add the header to the start of the array
gray_values = np.insert(gray_values, 0, header_values)

print("[!]Adjusting size of the image")
while size*size < len(gray_values):
    size += 1

print("[!]Adding zeros to fill the blank spaces")
#add zeros to the start of the array to make it a perfect square
zeros_to_add = size*size - len(gray_values)
zeros_added = 0
while len(gray_values) < size*size:
    print(f'\r[!]Zeros added: {zeros_added}/{zeros_to_add}', end='')
    gray_values = np.insert(gray_values, 0, 0)
    zeros_added += 1

print("\n[!]Reshaping the array into a 2d array")
#reshape the 1d array into a 2d array
gray_img = gray_values.reshape(size, size)

#stop timer
end = cv.getTickCount() - start

#check if the image is created
if gray_img is None:
    print(f'[-]Image not created! Time taken: {str(end/cv.getTickFrequency())}s')
    sys.exit(0)
else:
    print(f'[+]Image created successfully with size of {str(pow(size, 2))} bytes! Time taken: {str(end/cv.getTickFrequency())}s')
    #save the image as a tiff file with the file name from the command line and the adittion of "_enc.tif"
    cv.imwrite(inputFile[:-4] + "_enc.tif", gray_img)

#show the image in a window with matplotlib
plt.imshow(gray_img, cmap='gray', vmin=0, vmax=255)
plt.show()