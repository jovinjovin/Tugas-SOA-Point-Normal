from nameko.web.handlers import http
from werkzeug.wrappers import Response
import uuid
import json
from nameko.rpc import RpcProxy

from session import SessionProvider

class Service:
    name = "gateway_service"

    session_provider = SessionProvider()
    file_rpc = RpcProxy('file_service')

    @http('POST', '/register')
    def register(self, request):
        user_data = []
        user_data.append(request.json['username'])
        response = Response('Register Berhasil')
        return response
    
    @http('POST', '/login')
    def login(self, request):
        user_data = {
            'id': request.json['id'],
            'username': request.json['username']
        }
        session_id = self.session_provider.set_session(user_data)
        response = Response(str(user_data))
        response.set_cookie('SESSID', session_id)
        return response

    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            session_data = self.session_provider.delete_session(cookies['SESSID'])
            response = Response('Logout Berhasil')
            return response
        else:
            response = Response('Login Dulu!')
            return response

    @http('POST', '/upload')
    def upload_file(self, request):
        cookies = request.cookies
        if cookies:
            data = request.json
            result = self.file_rpc.upload_file(data['file'])
            return result
        else:
            response = Response('Login Dulu!')
            return response
            
    @http('POST', '/download')
    def download_file(self, request):
        data = request.json
        result = self.file_rpc.download_file(data['id'])
        return json.dumps(result)