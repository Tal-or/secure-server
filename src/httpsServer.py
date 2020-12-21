import ssl
import base64
from http.server import HTTPServer
from socketserver import ThreadingMixIn

from httpsHandler import HttpsHandler
from logger import SecureServerLogger as log

# nothing fancy, just keep the credentials from being display as plain text
USER = 'c2VtaW5hcg=='
PASSWD = 'MjA5Mjg='


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class HttpsServer(ThreadedHTTPServer):
    def __init__(self, user, passwd, server_address, handler_class=HttpsHandler):
        super().__init__(server_address, handler_class)
        self.key = base64.b64encode(bytes('%s:%s' % (user, passwd), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


def init_secure_http_server(ip_and_port):
    l_user = base64.urlsafe_b64decode(USER).decode('utf-8')
    l_passwd = base64.urlsafe_b64decode(PASSWD).decode('utf-8')
    httpd = HttpsServer(l_user, l_passwd, ip_and_port)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile='../private.pem',
                                   certfile='../cacert.pem',
                                   server_side=True)

    print("{}:{}".format(init_secure_http_server.__name__, log.lineno()),
          "Secure server initialized successfully! listening on: " +
          str(tuple(ip_and_port)))

    httpd.serve_forever()
