# Description: The Python script features functions to send ICMP echo requests,
# calculate packet checksums for data integrity, receive echo replies, and measure
# round-trip time to assess network reachability of a host.
# Author: Noah Caulfield
# Version: 1.0
# Intended for CS 440 at Eastern New Mexico University
# PA2-ICMPPing
# Date: 10/07/2023

# Use Python 3.10.x or above
import os
import struct
import time
import select
from socket import *

ICMP_ECHO_REQUEST = 8

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)

        if whatReady[0] == []:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        #-----Fill in start
        # Fetch the ICMP header from the IP packet
        
        # Return the time for the round trip if the packet ID matches
        
        # Fetch the ICMP header from the IP packet
        icmp_header = recPacket[20:28]
        icmp_type, code, checksum, packet_id, sequence = struct.unpack('bbHHh', icmp_header)

        # Check if the packet ID matches, then calculate and return the round-trip time
        if packet_id == ID:
            bytesInDouble = struct.calcsize('d')
            time_sent = struct.unpack('d', recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - time_sent
       
        #-----Fill in end
        timeLeft = timeLeft - howLongInSelect

        if timeLeft <= 0:
            return "Request timed out."

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0

    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, htons(myChecksum), ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")

    # SOCK_RAW is a powerful socket type.
    # For more details: http://sock-raw.org/papers/sock_raw
    # Therefore, you need to run this Python file with admin/sudo privileges
    # i.e, in MAC/Linux: sudo python3 PA2-ICMPPing.py
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process ID

    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")

    # Send ping requests to a server separated by approximately one second
    while 1:
        delay = doOnePing(dest, timeout)

        if isinstance(delay, str):
            print(delay)
        else:
            print("Ping response time:", delay * 1000, "ms")

        time.sleep(1)  # One second


## Change the destination host for every test
if __name__ == "__main__":
    #-----Fill in start
    # Ping the host
  
    host = input("Enter a host to ping: ")  # Prompt the user for a host
    ping(host)
  

   
    #-----Fill in end

