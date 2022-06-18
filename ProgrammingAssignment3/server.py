import socket
import argparse
import sys
import os
import datetime
import random

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
    if args.l[7:11] != ".txt":
        print(args.l[7:11])
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

        # Takes in the received message, appends it to the log, prints the message
        receivedMessage = client.recv(4096).decode()
        appendToLog(receivedMessage, LOGFILE)
        print ("Received Message: ", receivedMessage)

        # Step 5: If the received message is "network," a random quote is chosen and sent to the client
        if receivedMessage == "network":
            sendMessage = chooseQuote(dir)
            appendToLog(sendMessage, LOGFILE)
            print ("Sent Message: ", sendMessage)
            client.send(sendMessage.encode())

        # Server closes client
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