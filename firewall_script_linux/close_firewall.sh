# Set the default policy of the INPUT chain to DROP
iptables -F
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# Accept incomming TCP connections from eth0 on port 22
#iptables -A INPUT -i eth0 -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp -s 217.127.234.235 -j ACCEPT
iptables -A OUTPUT -p tcp -d  217.127.234.235 -j ACCEPT

figlet "Firewall Cerrado" > /etc/motd
