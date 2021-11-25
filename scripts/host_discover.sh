#!/bin/bash
if [ -z $1 ]
then
 echo -e "\n\tUsage: $0 <hostsfile.txt>\n"
 exit
fi

count=0
foundCount=0
nhosts=`wc -l $1 | awk '{print $1}'`
fecha=`date +'%Y-%m-%d_%k-%M'`
ficherosalida="bash_results.csv"
echo "Escribiendo en el fichero: $ficherosalida"
echo "Nombre de dominio ; IP" >> $ficherosalida
while read linea; do
    result=`host $linea | egrep "[[:digit:]]{2,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}"`
    ecode=`echo $?`
    if [ $ecode -eq 0 ]
    then
        ip=`echo $result | awk '{print $4}'`
        echo "$linea ; $ip" >> $ficherosalida
        let "foundCount++"
    else
        linea2="www.$linea"
        result2=`host $linea2 | egrep "[[:digit:]]{2,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}\.[[:digit:]]{1,3}"`
        ecode2=`echo $?`
        if [ $ecode2 -eq 0 ]
        then
            ip2=`echo $result2 | awk '{print $4}'`
            echo "$linea2 ; $ip2" >> $ficherosalida
            let "foundCount++"
        else
            echo "$linea ; No encontrado" >> $ficherosalida
        fi
    fi
    let "count++"
    echo -ne "Analizados $count de $nhosts hosts\r"
done < $1
echo "Terminado. Se han encontrado $foundCount de $nhosts hosts"
# alternativa a awk: cut -d " " -f 4
