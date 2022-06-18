import socket
import argparse
import sys
import os
import datetime
import struct

def main():
    # Step 1: Client takes in three arguments, the host IP, port, and Logfile
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, required=True, metavar="<HOST IP>")
    parser.add_argument('-p', type=int, required=True, metavar="<PORT>")
    parser.add_argument('-l', type=str, required=True, metavar="<LOGFILE>")
    args = parser.parse_args()

    # The client parses the inputted arguments
    HOST = args.s
    PORT = args.p
    LOGFILE = args.l
    # If an extension is not added to the inputted logfile, it is added. The current directory is also appended to the beginning of the filename
    if args.l[9:13] != ".txt":
        print(args.l[9:13])
        LOGFILE = LOGFILE + ".txt"

    dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    LOGFILE = dir + "\\" + LOGFILE

    # Step 2: Socket object is created
    ADDR = (HOST, PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Step 3: The client connects to the server 
    # Connection failure is handled
    try:
        client.connect(ADDR)
    except socket.error:
        print("Unable to connect to IP Address. Please make sure that the input is correct.")
        sys.exit()

    helloPacket = struct.Struct('4s 4s 4s 10s')

    # Sends hello packet
    appendToLog("Sending HELLO packet...", LOGFILE)
    client.send(helloPacket.pack('17'.encode(), '0'.encode(), '5'.encode(), 'HELLO'.encode()))

    receivedMessage = client.recv(4096).decode()
    print(receivedMessage)

    # Determines if packet was sent successfully
    if receivedMessage == "Version success.":
        appendToLog("Version accepted.", LOGFILE)

        # Determines command, and what to send
        enteredMsg = input("Please enter LIGHTON or LIGHTOFF: ")

        if enteredMsg == "LIGHTON":
            client.send(helloPacket.pack('17'.encode(), '1'.encode(), str(len(enteredMsg)).encode(), enteredMsg.encode()))

        elif enteredMsg == "LIGHTOFF":
            client.send(helloPacket.pack('17'.encode(), '2'.encode(), str(len(enteredMsg)).encode(), enteredMsg.encode()))

        else:
            print("Invalid input.")
            client.shutdown(1)
            print("Socket closed successfully.")

        # Receives confirmation
        receivedMessage = client.recv(4096).decode()
        print(receivedMessage)
        appendToLog(receivedMessage, LOGFILE)

    else:
        appendToLog("Version mismatch.", LOGFILE)
        client.shutdown(1)
        print("Could no connect. Socket closed successfully.")

    # Shuts down socket
    receivedMessage = client.recv(4096).decode()
    print(receivedMessage)
    client.shutdown(1)
    print("Socket closed successfully.")

    

def appendToLog(msg, LOGFILE):
    with open(LOGFILE, "a") as log:
        date = "[" + str(datetime.datetime.now()) + "]: "
        log.write(date + msg + "\n")

if __name__ == "__main__":
    main()