import socket
from urllib.request import Request, urlopen, HTTPError

def main():
    PORT = 5051
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    server.listen()
    print("[STARTING] server is starting...")
    print(f"[LISTENING] Proxy Server is listening on {SERVER} on port {PORT}")

    while True:
        conn, addr = server.accept()
        req = conn.recv(1024).decode()
        print(req)

        filename =  req.split()[1] #/test.html
        if filename == '/':
            filename = '/text.html'

        content = fetch_file(filename)
        if content:
                res = 'HTTP/1.1 200 OK \n\n' + content
        else:
                res = 'HTTP/1.1 404 NOT FOUND \n\n File Not Found'

        
        conn.send(res.encode())
        conn.close()


def fetch_file(filename):
    # Let's try to read the file locally first
    file_from_cache = fetch_from_cache(filename)

    if file_from_cache:
        print('Fetched successfully from cache.')
        return file_from_cache
    else:
        print('Not in cache. Fetching from server.')
        file_from_server = fetch_from_server(filename)

        if file_from_server:
            save_in_cache(filename, file_from_server)
            return file_from_server
        else:
            return None


def fetch_from_cache(filename):
    try:
        fin = open('cache' + filename)
        content = fin.read()
        fin.close()
        return content
    except IOError:
        return None


def fetch_from_server(filename):
    url = 'http://localhost:5050' + filename
    q = Request(url)

    try:
        res = urlopen(q)
        res_headers = res.info()
        content = res.read().decode('utf-8')
        return content
    except HTTPError:
        return None


def save_in_cache(filename, content):
    print('Saving a copy of {} in the cache'.format(filename))
    cached_file = open('cache' + filename, 'w')
    cached_file.write(content)
    cached_file.close()
    print("saving ", filename, " to cache")


if __name__ == '__main__':
    main()
