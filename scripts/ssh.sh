#!/bin/bash

ssh -q -o BatchMode=yes -o ConnectTimeout=10 example.com exit

if [ $? -ne 0 ]
then
  # Do stuff here if example.com SSH is down
  echo 'Can not connect to example.com' | mail -s "example.com down" whoever@wherever
fi





'''
#!/bin/bash
SSH_COMMAND="ssh user@host -fTN -R 2222:127.0.0.1:22 -i $HOME/.ssh/id_rsa"

while true; do
    if [[ -z $(ps -aux | grep "$SSH_COMMAND" | sed '$ d') ]]
    then eval $SSH_COMMAND
    else sleep 60
    fi
done
'''

#To background
#nohup my_autossh >/dev/null 2>&1 &