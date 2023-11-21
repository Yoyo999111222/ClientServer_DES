# ClientServer_DES
<table>
    <tr>
        <th colspan=2>Keamanan Informasi D</th>
    </tr>
    <tr>
        <th>NRP</th>
        <th>Nama</th>
    </tr>
    <tr>
        <td>5025211121</td>
        <td>Frederick Yonatan Susanto</td>
    </tr>
</table>   

#### Dalam melakukan komunikasi di sini, saya memanfaatkan GNS-3 dan mengimplementasikan Python3.

## Topologi

![image](https://github.com/Yoyo999111222/ClientServer_DES/assets/106955551/2bf7b697-7744-4797-b01d-55fb22030313)

## Config

- **Router**
```
auto eth0
 iface eth0 inet dhcp

auto eth1
 iface eth1 inet static
 	address 10.44.1.1
 	netmask 255.255.255.0

auto eth2
 iface eth2 inet static
 	address 10.44.2.1
 	netmask 255.255.255.0
```

- **Server**
```
auto eth0
 iface eth0 inet static
 	address 10.44.1.2
 	netmask 255.255.255.0
 	gateway 10.44.1.1
```

- **Client1**
```
auto eth0
 iface eth0 inet static
 	address 10.44.2.2
 	netmask 255.255.255.0
 	gateway 10.44.2.1
```

- **Client2**
```
auto eth0
 iface eth0 inet static
 	address 10.44.2.3
 	netmask 255.255.255.0
 	gateway 10.44.2.1
```

## Setup
Pada ./bashrc menggunakan nano :

- **Server**
```
echo "nameserver 192.168.122.1" > /etc/resolv.conf
apt-get update
apt-get install python3
```

- **Client 1 dan Client2**
```
echo "nameserver 10.44.1.2
nameserver 192.168.122.1
" > /etc/resolv.conf

apt-get update
apt-get install python3
```

## Result
- **Buka Node server, client1, dan client2:**

![(1)](https://github.com/Yoyo999111222/ClientServer_DES/assets/106955551/4a8562d7-57f3-4359-8251-0218ec8e7049)

- **Run file server.py pada node server serta client.py pada node client1 dan client2:**

![(2)](https://github.com/Yoyo999111222/ClientServer_DES/assets/106955551/e2763181-1585-4bf9-a9f3-af527dd7f521)
