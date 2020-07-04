import requests
def Statusosn():
    url = requests.get('https://api.github.com/repos/ziko-ZR1/xml/branches/osn').json()
    try:
        return url['commit']['commit']['message']+' '+url['commit']['commit']['committer']['date'].replace('T',' ').replace('Z','')
    except KeyError:
        return url['message'].split('. (')[0]

def Statusdstv():
    url = requests.get('https://api.github.com/repos/ziko-ZR1/xml/branches/master').json()
    try:
        return url['commit']['commit']['message']+' '+url['commit']['commit']['committer']['date'].replace('T',' ').replace('Z','')
    except KeyError:
        return url['message'].split('. (')[0]
    
def StatuseosnAR():
    url = requests.get('https://api.github.com/repos/Haxer/EPG-XMLFiles/branches/FullArabicXML').json()
    try:
        return url['commit']['commit']['message']+' '+url['commit']['commit']['committer']['date'].replace('T',' ').replace('Z','')
    except KeyError:
        return url['message'].split('. (')[0]
  
def StatusJawwy():
    url = requests.get('https://api.github.com/repos/ziko-ZR1/xml/branches/jawwy').json()
    try:
        return url['commit']['commit']['message']+' '+url['commit']['commit']['committer']['date'].replace('T',' ').replace('Z','')
    except KeyError:
        return url['message'].split('. (')[0]
  
def StatuseosnEN():
    url = requests.get('https://api.github.com/repos/Haxer/EPG-XMLFiles/branches/FullEnglishXML').json()
    try:
        return url['commit']['commit']['message']+' '+url['commit']['commit']['committer']['date'].replace('T',' ').replace('Z','')
    except KeyError:
        return url['message'].split('. (')[0]