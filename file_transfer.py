import socket, os, threading


# called by Weather_model.py to transfer data
class SendFile():
    def __init__(self,serverAdd="127.0.0.1",serverPort=9000,fileName=""):
        self.address=(serverAdd,serverPort)
        self.filename=fileName


    # function to connect to the socket and send file
    def send(self):

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(self.address)
        send_file=os.path.normcase(self.filename)


        # attempt to send the file
        try:
            f=open(send_file,"rb")
            print(f)
            send_file_thread = SendFileThread(s,f)
            send_file_thread.start()
        except IOError:
            print("Error")


   # Called by SendFile() to tranfer data
class SendFileThread(threading.Thread):
    def __init__(self,sock,file):
        threading.Thread.__init__(self)
        self.sock = sock
        self.file=file

        def run(self):
            print("file name is == "+self.filename)
            BUFFERSIZE=1024
            count = 0

            while True:
                file_data = self.file.read(BUFFERSIZE)
                if not file_data:
                    print("no data found")
                    break
                self.sock.send(file_data)

        print("sent file")
        self.file.close()
        self.sock.close()