import socket
import simplefix

def _synch(text):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 24444))    
    msg_data = str.encode(text)
    msg_len = len(msg_data).to_bytes(4,'little')

    sock.send(msg_len)   
    sock.send(msg_data)
    sock.recv(4)
    data = sock.recv(1024*1024)    
    sock.close()
    return data.decode("utf-8") 

def login():
    
    msg_text = '<FIXML v="5.0" r="20080317" s="20080314"><UserReq UserReqID="0" UserReqTyp="1" Username="BOS" Password="BOS" /></FIXML>' 
    msg_respons = _synch(msg_text)
    print(msg_respons)
    


if __name__ == '__main__':
   
    login()

    
    