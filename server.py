from scapy.all import IP, TCP, sniff

maxPort = 65535

# takes in a packet that passes our sniff filter
def parsePacket(packet):
  sport = packet.sport
  difference = maxPort - sport
  binVal = bin(difference)[2:]
  # print binVal
  binLen = len(binVal)
  if binLen > 8:
    binChar2 = binVal[-8:]
    binChar1 = binVal[0:binLen - 8]
    print chr(int(binChar1, 2))
    print chr(int(binChar2, 2))
  else:
    char = binVal
    print chr(int(char, 2))


sniff(filter="tcp and (dst port 80)", prn=parsePacket)
