import socket

HOST, PORT = 'localhost', 27906
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def server_enter(login, password):
    to_send = (login + ' ' + password + ' ' + 'enter').encode()
    sock.sendall(to_send)
    return sock.recv(1024).decode()


def server_create(login, name):
    to_send = (login + ' ' + name + ' ' + 'create').encode()
    sock.sendall(to_send)
    return sock.recv(1024).decode()


def get_data(project):
    to_send = (project + ' ' + 'get').encode()
    sock.sendall(to_send)
    return sock.recv(1024).decode()


def add_problem(project, data):
    to_send = (project + '\a' + data + '\a' + 'add').encode()
    sock.sendall(to_send)
    return sock.recv(1024).decode()


def delet_data(author, problem, description, table):
    to_send = (author + '\a' + problem + '\a' + description + '\a' + table + 'del').encode()
    sock.sendall(to_send)
    return sock.recv(1024).decode()


def chek_person(person):
    to_send = (person + '$' + 'chek').encode()
    sock.sendall(to_send)
    return sock.recv(1024).decode()


def add_person(person, project):
    to_send = (person + '$' + project + '$' + 'addperson').encode()
    sock.sendall(to_send)
    return sock.recv(1024).decode()
def close():
    sock.close()