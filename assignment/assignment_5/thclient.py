# Import socket module 
import socket 
import sys  

def Main(): 
    # local host IP '127.0.0.1' 
    host = ''
  
    # Define the port on which you want to connect 
    port = 8888
  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
  
    # connect to server on local computer 
    s.connect((host,port)) 
  
    # message you send to server 
    message = input(">>>")
    s.send(message.encode())
    data = s.recv(1024)
    print(data.decode())
    s.close() 
  
if __name__ == '__main__': 
    Main() 
