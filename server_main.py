import socket
import sqlite3
conn = sqlite3.connect(r'users.sqlite')
cur = conn.cursor()
HOST, PORT = 'localhost', 27906
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen(5)
sock, addr = server_sock.accept()
while True:
    data = sock.recv(1024)
    data = data.decode()
    if data[-5:] == 'enter':
        data = data.split()
        cur.execute(f'SELECT*FROM users WHERE login = "{data[0]}" AND password = "{data[1]}"')
        fetch = cur.fetchall()
        if fetch == []:
            cur.execute(f'SELECT*FROM users WHERE login = "{data[0]}"')
            fetch = cur.fetchall()
            if fetch == []:
                del data[-1]
                data.append('')
                cur.execute('INSERT INTO users VALUES(?,?,?)', data)
                conn.commit()
            else:
                sock.sendall('ququ'.encode())
        cur.execute(f'SELECT*FROM users WHERE login = "{data[0]}" AND password = "{data[1]}"')
        fetch = cur.fetchall()
        to_send = (data[0] + '\v' + fetch[-1][-1]).encode()
        sock.sendall(to_send)
    elif data[-6:] == 'create':
        key = False
        data = data.split()
        cur.execute(f'SELECT list_projects FROM users WHERE login ="{data[0]}"')
        previous = cur.fetchall()
        if previous != [('',)]:
            to_join = previous[0][0].split()
            if data[1] in to_join:
                key = True
            to_join.append(data[1])
            new = ' '.join(to_join)
        else:
            new = data[1]
        if key == False:
            table_name = data[0] + '_' + data[1]
            cur.execute(f'UPDATE users SET list_projects = "{new}" WHERE login = "{data[0]}"')
            cur.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ('
                        f'name STRING,'
                        f'problem STRING,'
                        f'description STRING);')
            conn.commit()
            sock.sendall('ok'.encode())
        else:
            sock.sendall('no'.encode())
    elif data[-3:] == 'get':
        data = data.split()
        try:
            cur.execute(f'SELECT * FROM "{data[0]}"')
        except:
            to_send = []
        to_send = cur.fetchall()
        result = ''
        for i in to_send:
            for y in i:
                result += str(y) + '\v'
            result += '\t'
        if result == '':
            result = 'ququ'
        sock.sendall(result.encode())
    elif data[-3:] == 'add':
        data = data.split('\a')
        need_data = data[1].split('\v')
        cur.execute(f'INSERT INTO "{data[0]}" VALUES(?,?,?)', need_data)
        conn.commit()
        sock.sendall('ok'.encode())
    elif data[-3:] == 'del':
        data = data[:-3].split('\a')
        cur.execute(f'DELETE FROM "{data[-1]}" WHERE name = "{data[0]}"AND '
                    f'problem = "{data[1]}"AND description = "{data[2]}"')
        conn.commit()
        sock.sendall('ok'.encode())
    elif data[-4:] == 'chek':
        data = data.split('$')
        cur.execute(f'SELECT * FROM users WHERE login ="{data[0]}"')
        if cur.fetchall() != []:
            sock.sendall('true'.encode())
        sock.sendall('false'.encode())
    elif data[-9:] == 'addperson':
        data = data.split('$')
        cur.execute(f'SELECT list_projects FROM users WHERE login = "{data[0]}"')
        result = cur.fetchall()[0][0]
        result += ' ' + data[1]
        cur.execute(f'UPDATE users SET list_projects = "{result}" WHERE login = "{data[0]}"')
        conn.commit()
