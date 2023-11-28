import socket
import select
import threading
import pprint

import urllib.request

CLIENT_IP = socket.gethostbyname(socket.gethostname())
CLIENT_PORT = 57244
CLIENT_ADDR = (CLIENT_IP, CLIENT_PORT)

# IP = socket.gethostbyname(socket.gethostname())
# IP = "0.0.0.0"
# IP = "192.168.1.12"
IP =  '61.28.231.242'
# IP = socket.gethostbyname(socket.gethostname())
PORT = 9896
ADDR = (IP, PORT)
SIZE = 1024
BACKLOG = 10
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
PUBLISH = 'publish'
FETCH = 'fetch'
SEND = 'send'
DOWNLOAD = 'download'
EXIT = 'exit'

LISTEN_PORT = 57244

local_files = {}

#function to send file
def sendf(soc, lname):
    file=open(lname,'rb')
    data=file.read()
    print(f"send file {data}")
    soc.send(data)
    print('File sent')

#function to receive file
def recvf(soc, fname):
    data = soc.recv(40960)
    print(f"receiving file")
    file=open(fname,'w')
    file.write(str(data))
    file.close()
    print('File received')

#function for client to connect to listening client                
def cconnect(peer_ip, peer_port, fname, lname):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        # soc.connect((peer_ip,peer_port))
        soc.connect((peer_ip,CLIENT_PORT))
    except:
        print('Unable to connect to client')
        return
    print('now connected')
    msg = f"download {fname} {lname}".encode(FORMAT)
    soc.send(msg)
    recvf(soc, fname=fname)
    while 1:
       data = soc.recv(SIZE).decode(FORMAT)
       if EXIT in data:
          soc.close()
          break

def handle_client(conn, addr):
    print(f"[PEER NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
      msg = conn.recv(SIZE).decode(FORMAT)
      print(f"Msg: {msg}")
      if DOWNLOAD in msg:
        print(f"DOWNLOAD: ")

def plisten():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(CLIENT_ADDR)
  s.listen()
  print(f"listening to {CLIENT_IP}:{CLIENT_PORT}")


  while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[PEER ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    connected = True
    while connected:
       data = conn.recv(SIZE).decode(FORMAT)
       if DOWNLOAD in data:
        print(f"[LISTEN] Received Download request: {data}")
        infos = data.split()
        lname = infos[2]
        fname = infos[1]
        msg = f"send {fname}".encode(FORMAT)
        sendf(conn, lname=lname)
        conn.send(msg)
       


def pconnect():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(ADDR)
  print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
  first_login = True

  connected = True
  while connected:
    msg = input("Input your name: " if first_login else "> ")
    if first_login:
      first_login = False

    client.send(msg.encode(FORMAT))
    if msg == DISCONNECT_MSG:
      connected = False
    elif PUBLISH in msg:
      print('PUBLISH')
      data = client.recv(SIZE).decode(FORMAT)
      print(f"[SERVER PUBLISH] {data}")
    elif FETCH in msg:
      print('FETCH')
      data = client.recv(SIZE).decode(FORMAT)
      print(f"[SERVER] {msg}")
      infos = data.split()
      fname = infos[1]
      lname = infos[2]
      peer_ip = infos[3]
      peer_port = infos[4]
      if peer_ip != CLIENT_IP:
        cconnect_thread = threading.Thread(target=cconnect, args=(peer_ip, peer_port, fname, lname))
        cconnect_thread.start()
    elif SEND in msg:
      print('SEND')
      # msg = client.recv(SIZE).decode(FORMAT)
      # print(f"[SERVER] {msg}")
    elif DOWNLOAD in msg:
      print('DOWNLOAD')
      # msg = client.recv(SIZE).decode(FORMAT)
      # print(f"[SERVER] {msg}")
    else:
      msg = client.recv(SIZE).decode(FORMAT)
      print(f"[SERVER] {msg}")

def main():
  connect_thread = threading.Thread(target=pconnect)
  listen_thread = threading.Thread(target=plisten)

  connect_thread.start()
  listen_thread.start()


if __name__ == "__main__":
  main()