import socket
import random
import logging
import re
import json


logging.basicConfig(level=logging.DEBUG)

HOST = "127.0.0.1"
PORT = random.randint(10000, 20000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print(f"Binding server on {HOST}:{PORT}")
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:

        conn.send("Hello, I am server!".encode("utf-8"))

        while True:
            data = conn.recv(4096)
            if not data or data == b"close":
                print("Got termination signal", data, "and closed connection")
                conn.close()
            data = data.decode("utf-8")
            my_list = data.split('\n')
            dic = {}

            for i in my_list[:-2:]:
                splitter = re.split(': | / ', i)
                dic[splitter[0]] = splitter[1]

            json_file = json.dumps(dic)
            request = 'HTTP/1.1 200 OK\n Content-Length: 100\n Connection: close\n Content-Type: application/json\n\n' +\
                      json_file

            conn.send(request.encode("utf-8"))
            logging.info(f"Sent '{data}' to {addr}")