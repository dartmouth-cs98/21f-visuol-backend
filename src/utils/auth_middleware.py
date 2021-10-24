# How Authorization/Authentication works in visuol
# 
# When the user attempts to make an api request, we call this middleware before handling the api request
# If the user is not already authenticated and authorized, we send them back to the sign in portal
# In the sign-in portal the user enters their credentials, and submits a request to our login endpoint
# If successful, we return a session_token which is an encrypted JWT that stores the user's session information and id
# After autorization, the user now sends the session_token as an authorization token with each request.
# We decrypt the token and use it both to determine the person's credentials, and to authorize their session.


from werkzeug.wrappers import Request, Response, ResponseStream
from flask import jsonify
import jwt
import os

# from https://medium.com/swlh/creating-middlewares-with-python-flask-166bd03f2fd4
class middleware():
    def __call__(self, environ, start_response):
        request = Request(environ)
        
        
        # decode session token
        auth_header = request.authorization()
        
        valid_header = True
        if auth_header == None:
            valid_header = False
            message = 'Could not find header token. Please reauthenticate and reauthorize.'
        
        tokens = auth_header.split()
        if len(tokens) != 2:
            valid_header = False
            message = 'Unrecognized authorization header format. Expected 2 tokens, got {}'.format(len(tokens))
        if tokens([0] != 'Bearer'):
            valid_header = False
            message = 'Unrecognized authorization header scheme, Expected Bearer, got {}'.format(tokens[0])
        
        session_token = tokens[1]

        try:
            identity = jwt.decode(session_token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        except jwt.DecodeError:
            valid_header = False
            message = 'Could not decode jwt token.'
        
#         >>> import jwt
# >>> encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
# >>> print(encoded_jwt)
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U
# >>> jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
# {'some': 'payload'}

        

        res = Response(response=jsonify({
                    'status: error'
                    'message': message
                }),
                status=401,
                mimetype='application/json')

        print('auth header', auth_header)
        
        
        if userName == self.userName and password == self.password:
            environ['user'] = { 'name': 'Tony' }
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
        return res(environ, start_response)