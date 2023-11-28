import socket
import select
import threading

import urllib.request


# IP = socket.gethostbyname(socket.gethostname())
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
def sendf(soc):
    soc.send('file name: ')
    fname = soc.recv(SIZE)    
    file=open(fname,'rb')
    data=file.read()
    soc.send(data)
    print('File sent')

#function for client to connect to listening client                
def cconnect(peer_ip, peer_port, fname, lname):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        soc.connect((peer_ip,peer_port))
    except:
        print('Unable to connect to client')
    print('now connected')
    while 1:
        msg = soc.recv(SIZE)
        if DOWNLOAD in msg:
            sendf(soc)
        if EXIT in msg:
            print('session ended')
            soc.close()
            break
        # user_input = raw_input('<Me> ')
        # soc.send(user_input)
        # if user_input == '\SEND_FILE':
        #     recvf(soc)  
        # if user_input == '\CLOSE_SESSION':
        #     print 'session ended'
        #     soc.close()
        #     break
    return

def handle_client(conn, addr):
    print(f"[PEER NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
      msg = conn.recv(SIZE).decode(FORMAT)
      print(f"Msg: {msg}")
      if DOWNLOAD in msg:
        print(f"DOWNLOAD: ")

def plisten():
  external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
  print(external_ip)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  #binding the socket to external ip and port
  s.bind(("0.0.0.0", LISTEN_PORT))
  s.listen()
  print(f"listening to {external_ip}:{LISTEN_PORT}")

  while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[PEER ACTIVE CONNECTIONS] {threading.active_count() - 1}")


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
      msg = client.recv(SIZE).decode(FORMAT)
      print(f"[SERVER PUBLISH] {msg}")
    elif FETCH in msg:
      print('FETCH')
      msg = client.recv(SIZE).decode(FORMAT)
      print(f"[SERVER] {msg}")
      infos = msg.split()
      fname = infos[1]
      lname = infos[2]
      peer_ip = infos[3]
      peer_port = infos[4]
      cconnect(peer_ip=peer_ip, peer_port=peer_port, fname=fname, lname=lname)
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
  # listen_thread = threading.Thread(target=plisten)

  connect_thread.start()
  # listen_thread.start()


if __name__ == "__main__":
  main()