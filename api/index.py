from http.server import BaseHTTPRequestHandler
import requests
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        res = requests.get('https://cf.samarpitminz.com/').json()['result']
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.send_header('Cache-Control', 's-maxage=3600, stale-while-revalidate')
        self.end_headers()
        params = parse_qs(self.path[5:])
        if 'contest' in params:
            cres = requests.get('https://codeforces.com/api/contest.standings?contestId=' + params['contest'][0]).json()['result']['rows']
            user_country = { user['handle']:user['country'] for user in res if 'country' in user }
            user_country_contest = { record['party']['members'][0]['handle']:user_country[record['party']['members'][0]['handle']] for record in cres if record['party']['members'][0]['handle'] in user_country }
            user_rank = { user['handle']:user['rank'] for user in res }
            user_rank_contest = { record['party']['members'][0]['handle']:user_rank[record['party']['members'][0]['handle']] for record in cres }
            user_org = { user['handle']:user['organization'] for user in res if 'organization' in user}
            user_org_contest = { record['party']['members'][0]['handle']:user_org[record['party']['members'][0]['handle']] for record in cres if record['party']['members'][0]['handle'] in user_org }
            self.wfile.write(json.dumps({'country': user_country_contest, 'rank': user_rank_contest, 'organization': user_org_contest}).encode(encoding='utf_8'))
        else:
            user_country = { user['handle']:user['country'] for user in res if 'country' in user }
            user_rank = { user['handle']:user['rank'] for user in res }
            user_org = { user['handle']:user['organization'] for user in res if 'organization' in user }
            self.wfile.write(json.dumps({'country': user_country, 'rank': user_rank, 'organization': user_org}).encode(encoding='utf_8'))
        return