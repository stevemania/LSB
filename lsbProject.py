## Author: Steve Duran
## Class: CPSC 353
## CWID: 805923158
## File: lsbProject.py

#!/usr/bin/python3
from PIL import Image
import binascii
import argparse
import sys


######################################################
## <Description> Converts string into bit form & appends length to string
## Parameter:
##       message: string variable
## Return: returning string of bits
######################################################
def convertMessage(message):
    message = ''.join(format(ord(x), '08b') for x in message)
    message = format(len(message), '011b') + message
    return message


######################################################
## <Description> Converts string into bit form & appends length to string
## Parameter:
##       message: string variable
## Return: Outputs a image with the message hidden in the Least Significant Bit
######################################################
def encode(file, message):
    message = convertMessage(message)
    
    k = 0
    image = Image.open(file)
    pixels = image.load()
    
    #Retrieving every pixel from image
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r,g,b = pixels[i, j]
            bit = int(message[k])if k < len(message) else 0; k += 1
            pixels[i, j] = ((r & ~1) | bit, g, b) # bit wise operator(checks lsb if even/odd)/converting lsb
    image.save(file[:5] + '_encoded.png')

######################################################
## <Description> The function retrieves the hidden message from the image.
## Parameter:/Users/steve/Desktop/imag_encoded/images/testImage.jpg
##       file: string variable with the file path
## Return: Outputs the hidden message to the console.
######################################################
def decode(file):
    message = ''
    image = Image.open(file[:5] + '_encoded.png')
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r,g,b = pixels[i, j]
            bit = r & 1 # bit wise operator
            message += str(bit)
    size = int(message[:11],2)
    message = message[11:] #retreiving length of message
    m = []

    # taking 8 bit at a time and convering the bit to byte to character
    for i in range(int(size / 8)):
        byte = message[i*8:(i+1)*8]
        m.append(chr(int(byte, 2)))
    return ''.join(m)

# functions being called
file = 'images/testImage.jpg'
encode(file, 'THIS IS THE SECRET MESSAGE THAT WILL BE HIDDEN WITHIN THE IMAGE!!!')
print (decode(file))
