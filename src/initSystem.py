from httpsServer import init_secure_http_server

SERVER_IP = 'localhost'
SERVER_PORT = 25000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)


def init():
    init_secure_http_server(SERVER_ADDRESS)
