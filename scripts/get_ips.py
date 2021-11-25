import subprocess
import re
import csv

hosts = open("lista_dominio2.txt","r")
csvFile = open("hostsResults2.csv","w+")
writer = csv.writer(csvFile,delimiter=';')
writer.writerow(["Dominio","IP"])
regexIP = "\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
#\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}

def checkIP(host):
    host = host.rstrip()
    try:
        output = subprocess.check_output("host "+host,shell=True)
        resultados = re.findall(r""+regexIP,output)
    if not resultados:
        return 1
    

for line in hosts:
    line = line.rstrip()
    try:
        output = subprocess.check_output("host "+line,shell=True)
        #print "[DEBUG] output: " +output
        resultados = re.findall(r""+regexIP,output)
        if not resultados:
            try:
                output = subprocess.check_output("host www."+line,shell=True)
                #print "[DEBUG] output: " +output
                resultados = re.findall(r""+regexIP,output)
                writer.writerow(["www."+line,resultados])
            except subprocess.CalledProcessError:
                print "ERROR 2do except " + line
                writer.writerow(["www."+line,"no encontrado/error"])
        else:
            writer.writerow([line,resultados])
    except subprocess.CalledProcessError:
        try:
            output = subprocess.check_output("host www."+line,shell=True)
            #print "[DEBUG] output: " +output
            resultados = re.findall(r""+regexIP,output)
            writer.writerow([line,resultados])
        except subprocess.CalledProcessError:
            print "ERROR 2do except " + line
            writer.writerow(["www."+line,"no encontrado/error"])

hosts.close()
csvFile.close()
