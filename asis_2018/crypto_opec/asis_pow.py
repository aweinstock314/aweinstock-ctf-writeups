import json
import re
import requests
import time

def solve_pow(p):
    #r = r'Submit a printable string X, such that sha256(X)\[-6:\] = ([0-9a-f]{6})'
    r = r'Submit[^\n]* = ([0-9a-f]{6})'
    s = p.recvregex(r)
    chal = re.findall(r, s)[0]
    print(repr(chal))

    # Requires an instance of https://github.com/aweinstock314/power
    resp = json.loads(requests.get('http://localhost:8080/sha256', params={'mask': '00'*29+'ff'*3, 'goal': '00'*29+chal, 'printable': 1}).text)

    print(repr(resp))
    print(resp['preimage_hex'].decode('hex'))
    p.send(resp['preimage_hex'].decode('hex'))
    time.sleep(1)
    p.sendline()


