import socket

# IP = socket.gethostbyname(socket.gethostname())
IP =  '61.28.231.242'
# IP = socket.gethostbyname(socket.gethostname())
PORT = 9896
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
PUBLISH = 'publish'
FETCH = 'fetch'
SEND = 'send'
DOWNLOAD = 'download'

local_files = {}

def main():
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
      # msg = client.recv(SIZE).decode(FORMAT)
      # print(f"[SERVER] {msg}")
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


if __name__ == "__main__":
  main()