from scapy.all import *
import argparse
import re

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80

parser = argparse.ArgumentParser(description='Generates a monitor_flujos-alike csv output')
parser.add_argument('-i', '--input', type=str, help='Input pcap file', required=True)
parser.add_argument('-o', '--output', type=str, help='Output file', required=True)
args = parser.parse_args()
print(args)
exit


trace = rdpcap(args.input)
SYNs = {}
SYNACKs = {} 
res = {}

for packet in trace:
    if IP in packet and TCP in packet:
        srcIP = packet['IP'].src 
        sport = packet['TCP'].sport
        dstIP = packet['IP'].dst 
        dport = packet['TCP'].dport
        
        if sport > dport:
            srcIP, dstIP = dstIP, srcIP
            sport, dport = dport, sport
        qtuple = (srcIP, dstIP, sport, dport)
        sqtuple = str(qtuple)
        F = packet.sprintf('%TCP.flags%')
        if F == 'S':
            #print('SYN')
            SYNs[sqtuple] = packet.time
            #print(qtuple)
        elif F == 'SA':
            #print('SYNACK')
            SYNACKs[sqtuple] = packet.time
            #print(qtuple)

for k, pSYN in SYNs.iteritems():
    if k in SYNACKs:
        res[k] = (SYNACKs[k] - pSYN)
    else:
        print('SYNACK not found for %s' % (k))

print(res)
print(min(res.values()), max(res.values()))
f = open(args.output, 'w')

for k, v in res.iteritems():
    k = re.sub('[!\'()]', '', k)
    k = '%s, %.12f' % (k, v)
    f.write(k+"\n")

