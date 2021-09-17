from http.server import BaseHTTPRequestHandler
import requests
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        res = requests.get('https://cf.samarpitminz.com/')
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header('Cache-Control', 's-maxage=3600, stale-while-revalidate')
        self.end_headers()
        params = parse_qs(self.path[5:])
        if 'contest' in params:
            cres = requests.get('https://codeforces.com/api/contest.standings?contestId=' + params['contest'][0])
            if 'country' in params:
                user_country = { user['handle']:user['country'] for user in res.json()['result'] if 'country' in user}
                user_country_contest = { record['party']['members'][0]['handle']:user_country[record['party']['members'][0]['handle']] for record in cres.json()['result']['rows'] if record['party']['members'][0]['handle'] in user_country}
                self.wfile.write(json.dumps(user_country_contest).encode(encoding='utf_8'))
                return
            if 'rank' in params:
                user_rank = { user['handle']:user['rank'] for user in res.json()['result']}
                user_rank_contest = { record['party']['members'][0]['handle']:user_rank[record['party']['members'][0]['handle']] for record in cres.json()['result']['rows']}
                self.wfile.write(json.dumps(user_rank_contest).encode(encoding='utf_8'))
                return
            user_org = { user['handle']:user['organization'] for user in res.json()['result'] if 'organization' in user}
            user_org_contest = { record['party']['members'][0]['handle']:user_org[record['party']['members'][0]['handle']] for record in cres.json()['result']['rows'] if record['party']['members'][0]['handle'] in user_org}
            self.wfile.write(json.dumps(user_org_contest).encode(encoding='utf_8'))
        else:
            if 'country' in params:
                user_country = { user['handle']:user['country'] for user in res.json()['result'] if 'country' in user}
                self.wfile.write(json.dumps(user_country).encode(encoding='utf_8'))
                return
            if 'rank' in params:
                user_rank = { user['handle']:user['rank'] for user in res.json()['result']}
                self.wfile.write(json.dumps(user_rank).encode(encoding='utf_8'))
                return
            user_org = { user['handle']:user['organization'] for user in res.json()['result'] if 'organization' in user}
            self.wfile.write(json.dumps(user_org).encode(encoding='utf_8'))
        return