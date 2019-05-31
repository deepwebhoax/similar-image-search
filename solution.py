from sys import argv
from sys import exit
from os import listdir
from PIL import Image
from PIL import ImageStat

def DifferenceHash(theImage):

	# Convert the image to 8-bit grayscale.
	theImage = theImage.convert("L") # 8-bit grayscale

	# Squeeze it down to an 8x8 image.
	theImage = theImage.resize((8,8), Image.ANTIALIAS)

	# Go through the image pixel by pixel.
	# Return 1-bits when a pixel is equal to or brighter than the previous
	# pixel, and 0-bits when it's below.

	# Use the 64th pixel as the 0th pixel.
	previousPixel = theImage.getpixel((0, 7))

	differenceHash = 0
	for row in range(0, 8, 2):

		# Go left to right on odd rows.
		for col in range(8):
			differenceHash <<= 1
			pixel = theImage.getpixel((col, row))
			differenceHash |= 1 * (pixel >= previousPixel)
			previousPixel = pixel

		row += 1

		# Go right to left on even rows.
		for col in range(7, -1, -1):
			differenceHash <<= 1
			pixel = theImage.getpixel((col, row))
			differenceHash |= 1 * (pixel >= previousPixel)
			previousPixel = pixel

	return differenceHash

if __name__ == '__main__':

    if len(argv) == 3:

        # Go through all the images in directory
        # and create difference hashes for each one
        imgNames = listdir(argv[2])
        hashes = []
        for i in range(len(imgNames)):
            img = Image.open(argv[2] + '/' + imgNames[i])
            hashes.append(DifferenceHash(img))

        # Make all the different hash comparisons
        # and print out those with 90+ percent of similarity
        for i in range(len(imgNames)):
            hash = hashes[i]

            for j in range(i+1,len(imgNames)):
                testHash = hashes[j]
                similarityPercent = (64 - bin(hash ^ testHash).count('1'))*100.0/64.0
                if similarityPercent>90:
                    print(imgNames[i], imgNames[j], similarityPercent)
                    
    else:
        print('usage: solution.py [-h] --path PATH \n')
        print('First test task on image similarity.\n')
        print('optional arguments:')
        print('\t-h, --help         show this help message and exit')
        print('\t--path PATH        folder with images')
