import logging
# don't output warnings from scapy, kthx
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, TCP, sniff
import argparse

maxPort = 65535

# takes in a packet that passes our sniff filter
def parsePacket(packet):
  global fileDescriptor
  sport = packet.sport
  difference = maxPort - sport
  binVal = bin(difference)[2:]
  # print binVal
  binLen = len(binVal)
  if binLen > 8:
    binChar2 = binVal[-8:]
    binChar1 = binVal[0:binLen - 8]
    char1 = chr(int(binChar1, 2))
    char2 = chr(int(binChar2, 2))
    print "Received: " + char1 + char2
    fileDescriptor.write(char1)
    fileDescriptor.write(char2)
  else:
    char = chr(int(binVal, 2))
    print "Received: " + char
    fileDescriptor.write(char)


# start of execution
parser = argparse.ArgumentParser(description="Covert Channel Server")
parser.add_argument('-o'
                   , '--output'
                   , dest='filePath'
                   , help='Absolute path to where you would like to save packets sent to the server.'
                   , required=True)
args = parser.parse_args()
global fileDescriptor
fileDescriptor = open(args.filePath, 'a')

sniff(filter="tcp and (dst port 80)", prn=parsePacket)
