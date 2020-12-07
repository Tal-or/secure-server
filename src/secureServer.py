import cgi
import json
from collections import namedtuple
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import ssl
from logger import SecureServerLogger as log, ResCode


# TODO replace all CtlLogger with standard logger

class Server(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # GET sends back a Hello world message

    def do_GET(self):
        self._set_headers()
        self.wfile.write(bytes(json.dumps({'received': 'ok'}), 'utf-8'))

        # POST echoes the message adding a JSON field

    def do_POST(self):
        try:
            header = self.headers.get('content-type')
            if header is None:
                self.handle_error()
                return

            # ctype, pdict = cgi.parse_header(header)
            # # refuse to receive non-json content
            # if ctype != 'application/json':
            #     self.handle_error()
            #     return

            # read the message and convert it into a python dictionary
            length = int(self.headers.get('content-length'))
            if length == 0:
                self.handle_error()
                return

            message = self.rfile.read(length)
            # Parse JSON into an object with attributes corresponding to dict keys.
            # message = json.loads(self.rfile.read(length),
            #                      object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

            # rc, rc_str = handle_message(message)
            print(message)
            rc = ResCode.OK
            if rc == ResCode.OK:
                self._set_headers()
                # if not rc_str:  # rc_str is empty
                #     rc_str = "return code:{} command returned successfully".format(str(rc.value))
                # self.wfile.write(bytes(_(rc=rc.value, result=rc_str).__str__(), 'utf-8'))
            # else:
            #     self.handle_error(rc_str)
        except BrokenPipeError as e:
            print("{}:{}".format(self.do_POST.__name__, log.lineno()), str(e))

        except (AttributeError, ValueError) as e:
            print("{}:{}".format(self.do_POST.__name__, log.lineno()), str(e))
            self.handle_error(e)

    def handle_error(self, msg=''):
        self.send_response(400)
        self.end_headers()
        # self.wfile.write(bytes(_(rc=1, result=msg).__str__(), 'utf-8'))


def init_secure_http_server(ip_and_port):
    server_class = ThreadedHTTPServer
    handler_class = Server
    httpd = server_class(ip_and_port, handler_class)
    # httpd.socket = ssl.wrap_socket(httpd.socket,
    #                                keyfile='../private.pem',
    #                                certfile='../cacert.pem',
    #                                server_side=True)

    print("{}:{}".format(init_secure_http_server.__name__, log.lineno()),
          "Secure server initialized successfully! listenning on: " +
          str(tuple(ip_and_port)))

    httpd.serve_forever()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
