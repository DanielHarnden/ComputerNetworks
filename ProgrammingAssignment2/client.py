import socket
import argparse
import sys
import os
import datetime

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
    if args.l[7:11] != ".txt":
        print(args.l[7:11])
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

    # Step 4: A message is read from the user
    # Easter egg: "network"
    # The user's message is appended to the logfile
    msg = input("Please enter the message you want to send to the server: ")
    appendToLog(msg, LOGFILE)

    # Step 5: The message is sent to the server
    client.send(msg.encode())

    # Step 6: A message is received from the server
    receivedMessage = client.recv(4096).decode()
    print(receivedMessage)
    
    # The message is appended to the logfile
    appendToLog(receivedMessage, LOGFILE)
        
    # The socket is closed
    client.shutdown(1)
    print("Socket closed successfully.")

def appendToLog(msg, LOGFILE):
    with open(LOGFILE, "a") as log:
        date = "[" + str(datetime.datetime.now()) + "]: "
        log.write(date + msg + "\n")

if __name__ == "__main__":
    main()