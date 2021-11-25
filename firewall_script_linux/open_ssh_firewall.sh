iptables -F

iptables -A INPUT -i eth0 -p tcp --dport 22 -j ACCEPT
