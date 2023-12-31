import sys
import os
import cv2 as cv
import numpy as np

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
#read the file into a int array
img = cv.imread(filepath, cv.IMREAD_GRAYSCALE)

print("[!]Flattening the data")
#convert the image into a 1d array
gray_values = img.flatten()

print("[!]Extracting header")
#locate the header in the array and extract the file type
header_start = np.where(gray_values == 36)[0][0]
header_end = np.where(gray_values == 36)[0][1]
file_type = gray_values[header_start+1:header_end].tobytes().decode()

print("[!]Removing header and leading zeros")
#remove the header and the leading zeros from the array
gray_values = gray_values[header_end+1:]
gray_values = gray_values[np.where(gray_values != 0)[0][0]:]

print("[!]Creating filename for the output")
#create a new file with given filename with the "_enc" suffix replaced with "_dec" and the file type
outputFile = inputFile.replace("_enc", "_dec")[:-3] + file_type

print("[!]Writing to file")
#write the data to the file
file = open(outputFile, "wb")
file.write(gray_values)
file.close()

print(f'[+]File saved as {outputFile}! Time taken: {(cv.getTickCount() - start) / cv.getTickFrequency()} s')