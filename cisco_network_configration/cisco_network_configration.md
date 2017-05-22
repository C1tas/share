# 三层交换机 dhcp

``` shell
vlan 10
name v10
int vlan 10
ip add 192.168.1.254 255.255.255.0
no shut
exit
ip dhcp pool v10
network 192.168.1.0 255.255.255.0
default-router 192.168.1.254
exit
```
# 三层交换机连通vlan

``` shell
ip routing
```

# NAT 转发

## NAT 静态一对一

>将192.168.1.1映射到200.1.1.10，使得PC能够访问8.8.8.8,同时Internet 200.1.1.10来访问PC

![](/home/r7/screenshots/cisco_network_configration.md/2017-05-22_094252.png)

``` shell
int fa 0/1
ip nat inside
exit
int se 0/0/0
ip net outside
exit
ip nat inside source static 192.168.1.1 200.1.1.10
ip route 0.0.0.0 0.0.0.0 200.1.1.2
show ip dhcp binding
```

## 删除NAT配置，静态端口映射PC web映射到200.1.1.10:8080

删除nat设置
``` shell
int se 0/0/0
no ip outside
int fa 0/1
no ip inside
no ip nat inside source static 192.168.1.1 200.1.1.10
no ip nat inside source list 10

```

``` shell
ip nat inside source static tcp 192.168.1.1 80 200.1.1.10 8080
```
## 删除NAT配置，动态NAT地址池一对一IP方式，PC能访问外网

``` shell
access-list 10 permit 192.168.1.0 0.0.0.255
ip nat pool i5 200.1.1.10 200.1.1.10 netmask 255.255.255.0
ip nat inside source list 10 pool i5
int fa0/1
ip nat inside
int se 0/0/0
ip nat outside
```

## 删除NAT配置，改用动态NAT地址池Overload方式，pc能访问外网

``` shell
access-list 11 permit 192.168.1.0 0.0.0.255
ip nat pool i6 200.1.1.3 200.1.1.254 netmask 255.255.255.0
ip nat inside source list 11 pool i6 overload
int fa 0/1
ip nat inside
int se 0/0/0
ip nat outside
```

# ospf 配置

``` shell
router ospf 10
network 192.168.1.1 0.0.0.255 area 0
network 172.16.1.1 0.0.0.255 area 0
end
```

# PAP 认证

``` shell
username r7 password lulu
encapsulaton PPP
ppp authentication PAP
encapsulaton PPP
ppp pap sent-username lulu password r7
```

# CHAP 认证

``` shell
encapsulaton PPP
ppp authentication chap

```

http://www.cisco.com/c/zh_cn/support/docs/wan/point-to-point-protocol-ppp/25647-understanding-ppp-chap.html#chapconfig

要配置 CHAP 身份验证，请完成以下步骤：

在接口上发出 encapsulation ppp 命令。

使用 ppp authentication chap 命令在两个路由器上启用 CHAP 身份验证。

配置用户名和口令。要执行此操作，请发出 username username password password 命令，其中 username 是对等体的主机名。请确保：

两端上的口令相同。

由于路由器名称和口令区分大小写，因此请确保它们完全相同。

注意： 默认情况下，路由器使用其主机名向对等体标识其身份。然而，可以通过 ppp chap hostname 命令更改此 CHAP 用户名。有关详细信息，请参阅使用 ppp chap hostname 和 ppp authentication chap callin 命令执行 PPP 身份验证。

# 访问控制表

``` shell
ip access-list standard acl
permit 192.168.1.0 0.0.0.255
int se 0/0/0
ip access-group acl in
```
``` shell
access-list 114 permit tcp host 192.168.1.1 host 3.3.3.3 eq telnet
access-list 114 permit icmp host 1.1.1.1 host 3.3.3.3
int se 0/0/0
ip access-group 114 in
```

# RIP
``` shell
router rip
network 192.168.4.0
network 10.0.3.0
end
```

# 网络地址/广播地址
A类网：网络号为1个字节，定义最高比特为0，余下7比特为网络号，主机号则有24比特编址。用于超大型的网络，每个网络有16777216（2^24）台主机（边缘号码如全“0”或全“1”的主机有特殊含义，这里没有考虑）。全世界总共有128（2^7）个A类网络，早已被瓜分完了。

B类网：网络号为2字节，定义最高比特为10，余下14比特为网络号，主机号则可有16比特编址。B类网是中型规模的网络，总共有16384（2^14）个网络，每个网络有65536（2^16）台主机（同样忽略边缘号码），也已经被瓜分完了。

C类网：网络号为3字节，定义最高三比特为110，余下21比特为网络号，主机号仅有8比特编址。C类地址适用的就是较小规模的网络了，总共有2097152（2^21）个网络号码，每个网络有256（2^8）台主机（同样忽略边缘号码）。

D类网：不分网络号和主机号，定义最高四比特为1110，表示一个多播地址，即多目的地传输，可用来识别一组主机。

如何识别一个IP地址的属性？只需从点分法的最左一个十进制数就可以判断其归属。例如，1～126属A类地址，128～191属B类地址，192～223属C类地址，224～239属D类地址。除了以上四类地址外，还有E类地址，但暂未使用。[2]

对于因特网IP地址中有特定的专用地址不作分配：
- （1）主机地址全为“0”。不论哪一类网络，主机地址全为“0”表示指向本网，常用在路由表中。
- （2）主机地址全为“1”。主机地址全为“1”表示广播地址，向特定的所在网上的所有主机发送数据包。
- （3）四字节32比特全为“1”。若IP地址4字节32比特全为“1”，表示仅在本网内进行广播发送。
- （4）网络号127。TCP/IP协议规定网络号127不可用于任何网络。其中有一个特别地址：127．0．0．1称之为回送地址（Loopback），它将信息通过自身的接口发送后返回，可用来测试端口状态。

广播地址(Broadcast Address)是专门用于同时向网络中所有工作站进行发送的一个地址。在使用TCP/IP 协议的网络中，主机标识段host ID 为全1 的IP 地址为广播地址，广播的分组传送给host ID段所涉及的所有计算机。例如，对于10.1.1.0 （255.255.255.0 ）网段，其广播地址为10.1.1.255 （255 即为2 进制的11111111 ），当发出一个目的地址为10.1.1.255 的分组（封包）时，它将被分发给该网段上的所有计算机。

# 静态路由
``` shell
ip route 192.168.2.0 255.255.255.0 10.0.1.2

ip route 192.168.3.0 255.255.255.0 10.0.1.2

ip route 192.168.4.0 255.255.255.0 10.0.1.2
```

# 聚合端口
show etherchannel summary
show etherchannel load-balance
show vlan
show spanning-tree
show port-security
``` shell
int port-channel 1
int range fa 0/1-2
switchport trunk encapsulaton dot1q
sw mode trunk
channel-group 1 mode on
```

## 流量平横
``` shell
port-channel load-balance src-mac
```

## 开启RSTP
``` shell
spanning-tree mode rapid-pvst
```

## 安全端口
``` shell
switchport port-security mac-address 00f0.0800.0730
```

# vlan路由 STP协议

## 子接口设置dot1q封装协议

``` shell
int fa0/0.10
encapsulation dot1q 10 //10 vlan id
```
## STP协议 根网桥
``` shell
spanning-tree mode pvst
spanning-tree vlan 1 root primary
spanning-tree vlan 1 priority 24768
```

# 交换机基本设置

## 特权密码
enable password c1tas

## telnet
``` shell
line vty 0 5
password c1tas
login

```
