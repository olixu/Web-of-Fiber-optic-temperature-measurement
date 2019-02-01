# -*- coding:utf-8 -*-
import  socketserver


class Myserver(socketserver.BaseRequestHandler):

    def handle(self):

        conn = self.request
        with open("1.txt", "w+") as f:
            while True:
                ret_bytes = conn.recv(1024)
                ret_data = str(ret_bytes,encoding="utf-8")
                if not ret_data:
                    break
                f.write(ret_data)
                print("jie shou dao wen jian")
        f.close() 
        conn.close()

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("0.0.0.0",5000),Myserver)
    server.serve_forever()


'''
class Myserver(socketserver.BaseRequestHandler):

    def handle(self):
        content = ''
        conn = self.request
        while True:
            ret_bytes = conn.recv(1024)
            ret_data = str(ret_bytes,encoding="utf-8")
            if not ret_data:
                print(content)
                break
            content = content + ret_data
        conn.close()

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("0.0.0.0",80),Myserver)
    server.serve_forever()
'''