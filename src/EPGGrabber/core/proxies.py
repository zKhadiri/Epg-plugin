import requests,string,random,re,base64

def proxy():
    res = {"result": 'a'+''.join(random.choice(string.digits+string.ascii_lowercase) for i in range(31))}
    _ = requests.post("http://free-proxy.cz/s.php",params=res)
    headers={
        "Connection": "keep-alive",
        "Cookie": "fp="+res['result'],
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }
    ur = requests.get('http://free-proxy.cz/fr/proxylist/country/DE/https/ping/level3',headers=headers)
    
    for ip,port in zip(re.findall(r'decode\(\"(.*?)\"',ur.text),re.findall(r'<span class=\"fport\" style=\'\'>(\d+)<\/span>',ur.text)):
        yield base64.b64decode(ip)+":"+port