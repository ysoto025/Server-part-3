import sys
import socket
from sys import argv
import threading
import signal
import os.path

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.settimeout(10.0)

if (len(argv) < 3) | (len(argv) > 3):
    sys.stderr.write("missing arguments or too many Arguments")
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

file_list = []


def connector(d, e):
    global con
    word = 'accio\r\n'
    var = 1
    global file_list
    file_not_open = True
    try:
        while True:
            if file_not_open:
                filename = str(argv[2]) + str(var) + ".file"
                stored_file = open(filename, "wb")
                var = var + 1
                file_not_open = False

            d.send(bytes(word.encode()))
            data = d.recv(1).decode("utf-8")
            stored_file.write(data)

            if not data:
                file_not_open = True

                stored_file.close()
                file_list.append(stored_file)
                con.remove(d)
                d.close()
                break
    except socket.timeout:
        stored_file.seek(0)
        stored_file.truncate()
        stored_file.write(bytes("ERROR: timeout"))
        stored_file.close()
        file_not_open = True
        file_list.append(stored_file)
        con.remove(d)
        d.close()



def signal_handler(sig, frame):
    sys.stderr.write("ERROR: SignalInterrupted")
    sys.exit(0)


while True:
        x, v = sock.accept()
        signal.signal(signal.SIGINT, signal_handler)
        cThread = threading.Thread(target=connector, args=(x, v))
        cThread.daemon = True
        cThread.start()
        con.append(x)
        print(var)



