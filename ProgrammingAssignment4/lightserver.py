import socket
import argparse
import sys
import os
import datetime
import random
import struct

def main():
    # Step 1: Server takes in two arguments, the port and Logfile
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, required=True, metavar="<PORT>")
    parser.add_argument('-l', type=str, required=True, metavar="<LOGFILE>")
    args = parser.parse_args()

    # The client parses the inputted arguments
    PORT = args.p
    LOGFILE = args.l
    # If an extension is not added to the inputted logfile, it is added. The current directory is also appended to the beginning of the filename
    if args.l[9:14] != ".txt":
        print(args.l[9:14])
        LOGFILE = LOGFILE + ".txt"

    dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    LOGFILE = dir + "\\" + LOGFILE

    while True:

        # Step 2: Create socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = ('127.0.0.1', PORT)
    
        # Step 3: Bind and listen
        try:
            server.bind(ADDR)
        except socket.error:
            print("Unable to bind. Please make sure that the input is correct.")
            sys.exit()

        # Server listens for a message from the client
        server.listen(1)

        # Step 4: Receive message from client, stores client information
        client, clientAddress = server.accept()
        print ("Connected to: ", clientAddress)

        packetStructure = struct.Struct('4s 4s 4s 10s')

        # Receive header information
        version, command, msgLength, receivedMessage = packetStructure.unpack(client.recv(4096))

        version = version.decode()
        version = version[0:2]
        command = command.decode()
        msgLength = msgLength.decode()
        receivedMessage = receivedMessage.decode()
        
        # Checks version
        if version == '17':
            client.send("Version success.".encode())
            print("Version success.")
            appendToLog("Returning: Version success.", LOGFILE)

            # Received command
            version, command, msgLength, receivedMessage = packetStructure.unpack(client.recv(4096))

            version = version.decode()
            command = command.decode()
            command = command[0:1]
            msgLength = msgLength.decode()
            receivedMessage = receivedMessage.decode()

            # Determines command
            if command == '1':
                print("Executing: LIGHTON.")
                appendToLog("Returning: Executing: LIGHTON.", LOGFILE)
                client.send("Success: LIGHTON.".encode())
            elif command == '2':
                print("Executing: LIGHTOFF.")
                appendToLog("Returning: Executing: LIGHTOFF.", LOGFILE)
                client.send("Success: LIGHTOFF".encode())
            else:
                print("Command not supported.")
                appendToLog("Returning: Command not supported.", LOGFILE)
                client.send("Failure".encode())
        else:
            client.send("Version mismatch.".encode())
            print("Version mismatch.")
            appendToLog("Returning: Version mismatch.", LOGFILE)

        client.close()



def chooseQuote(dir):
    quoteFile = dir + "\\quotes.txt"
    with open(quoteFile, "r") as quote:
        return random.choice(quote.readlines())

def appendToLog(msg, LOGFILE):
    with open(LOGFILE, "a") as log:
        date = "[" + str(datetime.datetime.now()) + "]: "
        log.write(date + msg + "\n")

if __name__ == "__main__":
    main()