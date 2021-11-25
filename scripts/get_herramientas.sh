apt-get update -y
apt-get upgrade -y
apt-get dist-upgrade -y
cd ~
mkdir herramientas
#dirsearch
git clone https://github.com/maurosoria/dirsearch.git
#seclists
git clone https://github.com/danielmiessler/SecLists.git
#linenum
git clone https://github.com/rebootuser/LinEnum.git
#null linux smb
git clone https://github.com/m8r0wn/nullinux.git
cd nullinux
pip install requirements.txt
cd ..
#photon web crawler
git clone https://github.com/s0md3v/Photon.git
#devploit information gathering tool:DNS, whois, traceroute,etc
git clone https://github.com/joker25000/Devploit
cd Devploit
chmod +x install
./install
cd ..
#API OpenAPI definitions testing tool
git clone https://github.com/RhinoSecurityLabs/Swagger-EZ.git
#PayloadAllTheThings
git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git
#GDB PEDA
git clone https://github.com/longld/peda.git ~/herramientas/peda
echo "source ~/herramientas/peda/peda.py" >> ~/.gdbinit
echo "DONE! debug your program with gdb and enjoy"