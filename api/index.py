from http.server import BaseHTTPRequestHandler
import requests
import json

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        res = requests.get('https://cf.minz.workers.dev')
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header('Cache-Control', 's-maxage=3600, stale-while-revalidate')
        self.end_headers()
        self.wfile.write(json.dumps({ user['handle']:user['organization'] for user in res.json()['result'] if 'organization' in user}).encode(encoding='utf_8'))
        return