# -*- coding:utf-8 -*-
'''
服务器cpu监控程序

思路：后端后台线程一旦产生数据，即刻推送至前端。
好处：不需要前端ajax定时查询，节省服务器资源。

'''

import time
from threading import Lock

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


thread = None
thread_lock = Lock()

with open("1.txt", "r") as f:
    content = f.read().split('\r\n')
    y_dataset = [float(i) for i in content if i != '']
    x_dataset = [i for i in range(len(y_dataset))]


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        with open("1.txt", "r") as f:
            content = f.read().split('\r\n')
            y_dataset = [float(i) for i in content if i != '']
            x_dataset = [i for i in range(len(y_dataset))]
            #print(y_dataset)
            #print(x_dataset)
        f.close()
        socketio.sleep(1)
        socketio.emit('server_response',{'data': [x_dataset,y_dataset]},namespace='/test') # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！
        print("send")


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)



# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/test')
def test_connect():
    print("start the connection")
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True)