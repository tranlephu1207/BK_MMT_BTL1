import socket
import threading
import pprint
from ping3 import ping, verbose_ping

IP = socket.gethostbyname(socket.gethostname())
PORT = 9896
ADD  = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "disconnect()"
GET_CONNECTIONS = "get connections"
DISCOVER_HOSTNAME = "discover"
PING_HOSTNAME = "ping"
SERVER_TERMINAL = "!TERMINAL"
CLOSE_TERMINAL = "exit()"

# Client commands
PUBLISH = 'publish'
FETCH = 'fetch'
SEND = 'send'
DOWNLOAD = 'download'

connections = {}
files = {}

def handle_client(conn, addr):
  print(f"[NEW CONNECTION] {addr} connected")
  connected = True
  first_login = True
  while connected:
    msg = conn.recv(SIZE).decode(FORMAT)
    # print(f"Msg: {msg}")
    if first_login:
      first_login = False
      connections[addr[0]] = {
        "ip": addr[0],
        "port": addr[1],
        "name": msg,
      }
      pprint.pprint(connections, width=1)
      msg = f"Welcome {msg}"
      conn.send(msg.encode(FORMAT))
    elif msg == DISCONNECT_MSG:
      try:
        del connections[addr[0]]
      except KeyError:
        pass
      connected = False
    elif PUBLISH in msg:
      print(f'PUBLISH: {msg}')
      infos = msg.split()
      pprint.pprint(infos)
      fname = infos[2]
      if files.get(fname) != None:
        error = f"{fname} exists"
        print(error)
        print('abc')
        conn.send(error.encode(FORMAT))
      else:
        files[fname] = {
          "ip": addr[0],
          "port": addr[1],
          "fname": fname,
          "lname": infos[1],
          "name": connections.get(addr[0]).get('name')
        }
        pprint.pprint(files, width=1)
        msg = f"{fname} added"
      conn.send(msg.encode(FORMAT))
    elif FETCH in msg:
      print(f'FETCH: {msg}')
      infos = msg.split()
      pprint.pprint(infos)
    elif SEND in msg:
      print(f'SEND: {msg}')
    elif DOWNLOAD in msg:
      print(f'DOWNLOAD: {msg}')
    else:
      print(f"[{addr}] {msg}")
      msg = f"Msg received: {msg}"
      conn.send(msg.encode(FORMAT))

  conn.close()


def main():
  print("[STARTING] server is starting...")
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(ADD)
  server.listen()
  print(f"[LISTEN] Server is listening on {IP}:{PORT}")

  while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    server_command = input()
    print(f"server_command: {server_command}")
    if server_command == SERVER_TERMINAL:
      open_terminal = True
      while open_terminal:
        server_command = input('> ')
        if server_command == CLOSE_TERMINAL:
          open_terminal = False
        elif GET_CONNECTIONS in server_command:
          pprint.pprint(connections, width=1)
        elif PING_HOSTNAME in server_command:
          print('abc')
          strs = server_command.split()
          verbose_ping(strs[1])
        elif DISCOVER_HOSTNAME in server_command:
          print('discover host name')
          strs = server_command.split()
          hostname = strs[1]
          print(f"Host name: {hostname}")
          result = {}
          for file in files.values():
            if file.get('ip') == hostname:
              result[file.get('fname')] = file
          
          print(f'discover from ${hostname} success')
          pprint.pprint(result)

if __name__ == '__main__':
  main()