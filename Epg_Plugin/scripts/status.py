import requests,re
def Statusosn():
    url = requests.get('https://api.github.com/repos/ziko-ZR1/xml/branches/osn')
    date = re.search(r'date\":\"(.*?)\"',url.content)
    message = re.search(r'message\":\"(.*?)\"',url.content)
    if date==None:
        return "API rate limit exceeded"
    else:
        return message.group()+' '+date.group().replace('T','  ').replace('Z','')

def Statusdstv():
    url = requests.get('https://api.github.com/repos/ziko-ZR1/xml/branches/master')
    date = re.search(r'date\":\"(.*?)\"',url.content)
    message = re.search(r'message\":\"(.*?)\"',url.content)
    if date==None:
        return "API rate limit exceeded"
    else:
        return message.group()+' '+date.group().replace('T','  ').replace('Z','')

def StatuseJaw():
    url = requests.get('https://api.github.com/repos/ziko-ZR1/xml/branches/jawwy')
    date = re.search(r'date\":\"(.*?)\"',url.content)
    message = re.search(r'message\":\"(.*?)\"',url.content)
    if date==None:
        return "API rate limit exceeded"
    else:
        return message.group()+' '+date.group().replace('T','  ').replace('Z','')
    
def StatuseosnAR():
    url = requests.get('https://api.github.com/repos/Haxer/EPG-XMLFiles/branches/FullArabicXML')
    date = re.search(r'date\":\"(.*?)\"',url.content)
    message = re.search(r'message\":\"(.*?)\"',url.content)
    if date==None:
        return "API rate limit exceeded"
    else:
        return message.group()+' '+date.group().replace('T','  ').replace('Z','')
    
def StatuseosnEN():
    url = requests.get('https://api.github.com/repos/Haxer/EPG-XMLFiles/branches/FullEnglishXML')
    date = re.search(r'date\":\"(.*?)\"',url.content)
    message = re.search(r'message\":\"(.*?)\"',url.content)
    if date==None:
        return "API rate limit exceeded"
    else:
        return message.group()+' '+date.group().replace('T','  ').replace('Z','')