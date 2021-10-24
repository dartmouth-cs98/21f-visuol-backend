
from werkzeug.wrappers import Request, Response, ResponseStream

# from https://medium.com/swlh/creating-middlewares-with-python-flask-166bd03f2fd4
class middleware():

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        session_token = request.json('session_token')
        
        if userName == self.userName and password == self.password:
            environ['user'] = { 'name': 'Tony' }
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
        return res(environ, start_response)