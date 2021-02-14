import sys
import socket
from sys import argv
import threading
import signal

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.settimeout(10.0)

if (len(argv) < 3) | (len(argv) > 3):
    sys.stderr.write("ERROR: missing arguments or too many Arguments")
    sys.exit()

if argv[1] == "":
    sys.stderr.write("ERROR: empty string")
    sys.exit(1)

if argv[2] == "":
    sys.stderr.write("ERROR: empty string")
    sys.exit(1)

if (int(argv[1]) < 0) | (int(argv[1]) > 65535):
    sys.stderr.write("ERROR: Overflow error")
    sys.exit(1)

con = []
sock.bind(('0.0.0.0', int(argv[1])))
sock.listen(1)


def connector(d, e):
    global con
    while True:
        a = d.recv(1024)
        for con in con:
            word = 'accio\r\n'
            con.send(bytes(word.encode()))

        if not a:
            con.remove(d)
            d.close()
            break


def signal_handler(sig, frame):
    sys.stderr.write("ERROR: SignalInterrupted")
    sys.exit(0)


try:

    while True:
        x, v = sock.accept()
        signal.signal(signal.SIGINT, signal_handler)
        cThread = threading.Thread(target=connector, args=(x, v))
        cThread.daemon = True
        cThread.start()
        con.append(x)
        print(con)

except socket.timeout:
    sys.stderr.write("ERROR: timeout")
    sys.exit(1)
