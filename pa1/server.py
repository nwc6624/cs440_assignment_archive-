#10/10/2023
#CS 440
#Author: Noah Caulfield
#Programming Assignment 1- Web Server 
#

from socket import *
import sys

# Create a server socket
serverPort = 80  
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receive the HTTP request from the client
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send HTTP headers to the socket
        response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(response_headers.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        # Send response message for file not found (404)
        not_found_message = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        error_content = "<html><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(not_found_message.encode())
        connectionSocket.send(error_content.encode())
        connectionSocket.close()

# Close the server socket
serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
