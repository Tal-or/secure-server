import cgi
import json
import sys

from collections import namedtuple
from http.server import BaseHTTPRequestHandler
from io import StringIO

from logger import SecureServerLogger as log

MAX_REQ_LEN = 512


class HttpsHandler(BaseHTTPRequestHandler):
    blacklist = ['sudo ', '\\']

    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm="Demo Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.check_auth:
            self._set_headers()
            self.wfile.write(bytes(json.dumps({'received': 'ok'}), 'utf-8'))

        # POST echoes the message adding a JSON field

    def do_POST(self):
        try:
            header = self.headers.get('content-type')
            if header is None:
                self.handle_error()
                return

            ctype, pdict = cgi.parse_header(header)
            # refuse to receive non-json content
            if ctype != 'application/json':
                self.handle_error()
                return

            if not self.check_auth():
                return

            # read the message and convert it into a python dictionary
            length = int(self.headers.get('content-length'))
            if length == 0:
                self.handle_error()
                return

            if length > MAX_REQ_LEN:
                self.handle_error("Request length is too long")
                return

            # Parse JSON into an object with attributes corresponding to dict keys.
            message = json.loads(self.rfile.read(length),
                                 object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

            if not self.validate(message.cmd):
                self.handle_error("Command contains illegal word and/or characters")
                return

            res = self.execute_cmd(message.cmd)

            if res:
                self._set_headers()
                self.wfile.write(bytes(json.dumps({'result': res}), 'utf-8'))
            else:
                self.handle_error("failed to compute result")

        except BrokenPipeError as e:
            print("{}:{}".format(self.do_POST.__name__, log.lineno()), str(e))

        except (AttributeError, ValueError) as e:
            print("{}:{}".format(self.do_POST.__name__, log.lineno()), str(e))
            self.handle_error(str(e))

        except (SyntaxError, NameError, TypeError) as e:
            print("{}:{}".format(self.do_POST.__name__, log.lineno()), str(e))
            self.handle_error(str(e))

        except Exception as e:
            print("{}:{}".format(self.do_POST.__name__, log.lineno()), str(e))
            self.handle_error(str(e))

    def handle_error(self, msg=''):
        self.send_response(400)
        self.end_headers()
        if not msg:
            msg = "Unknown error"
        self.wfile.write(bytes(json.dumps({'error': msg}), 'utf-8'))

    def check_auth(self):
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()
            self.wfile.write(bytes(json.dumps({'error': "No auth header received"}), 'utf-8'))
            return False

        if self.headers.get('Authorization') != 'Basic ' + str(self.server.get_auth_key()):
            self.do_AUTHHEAD()
            self.wfile.write(bytes(json.dumps({'error': "Invalid credentials"}), 'utf-8'))
            return False

        return True

    def validate(self, cmd):
        for word in self.blacklist:
            if word in cmd:
                return False
        return True

    @staticmethod
    def execute_cmd(cmd):
        old_stdout = sys.stdout
        sys.stdout = local_stdout = StringIO()
        res = eval(cmd)
        sys.stdout = old_stdout
        if res:
            return res
        return local_stdout.getvalue().strip()
