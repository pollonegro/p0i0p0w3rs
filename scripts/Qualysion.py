#!/usr/bin/env python
import json
import requests
import urllib
from termcolor import colored
import xlsxwriter
import argparse
import os
import time
import socket
import socks
import re
import time

c = 0
cuenta = 0
'''
cipherlist=["TLS_DHE_RSA_WITH_AES_128_GCM_SHA256","TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
"TLS_DHE_PSK_WITH_AES_128_GCM_SHA256","TLS_DHE_PSK_WITH_AES_256_GCM_SHA384",
"TLS_AES_128_GCM_SHA256","TLS_AES_256_GCM_SHA384","TLS_CHACHA20_POLY1305_SHA256",
"TLS_AES_128_CCM_SHA256","TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
"TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384","TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
"TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384","TLS_DHE_RSA_WITH_AES_128_CCM",
"TLS_DHE_RSA_WITH_AES_256_CCM","TLS_DHE_PSK_WITH_AES_128_CCM","TLS_DHE_PSK_WITH_AES_256_CCM",
"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256","TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
"TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256","TLS_ECDHE_PSK_WITH_CHACHA20_POLY1305_SHA256",
"TLS_DHE_PSK_WITH_CHACHA20_POLY1305_SHA256","TLS_ECDHE_PSK_WITH_AES_128_GCM_SHA256",
"TLS_ECDHE_PSK_WITH_AES_256_GCM_SHA384","TLS_ECDHE_PSK_WITH_AES_128_CCM_SHA256"]
'''
def DatosCorrectos(responsejson):

	prueba = len(responsejson.get('endpoints'))	
	IPV4SEG  = r'(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
	IPV4ADDR = r'(?:(?:' + IPV4SEG + r'\.){3,3}' + IPV4SEG + r')'
	patron = re.compile(r'(?:(?:' + IPV4SEG + r'\.){3,3}' + IPV4SEG + r')')

	for x in range(prueba):
		if patron.match(responsejson.get('endpoints')[x].get('ipAddress')):
			cuenta = x
	
	for x in range(len(responsejson.get('endpoints')[cuenta].get('details').get('suites'))):
		#print (responsejson.get('endpoints')[1].get('details').get('suites')[x].get('protocol'))
		if responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('protocol') == 512:
			print (colored("\nProtocolo SSLV2 - INSECURE \n", 'red'))
		if responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('protocol') == 768:
			print (colored("\nProtocolo SSLV3 - INSECURE \n", 'red'))
		if responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('protocol') == 769:
			print (colored("\nProtocolo TLSV1.0 \n", 'yellow'))
		if responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('protocol') == 770:
			print (colored("\nProtocolo TLSV1.1 \n", 'yellow'))
		if responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('protocol') == 771:
			print (colored("\nProtocolo TLSV1.2 \n", 'green'))
		if responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('protocol') == 772:
			print (colored("\nProtocolo TLSV1.3 \n", 'green'))

		for y in range(len(responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('list'))):
			var = responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('list')[y].get('kxType')
			var2 = responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('list')[y].get('kxStrength')
			if var2 is not None and "3DES" not in responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('list')[y].get('name'):
				if var2 >= 2048:
					#print (colored(responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('list')[y].get('name') + "\t" + var + " " + str(var2) + " bits",'green'))
					print(colored('{} - {} - {} bits'.format(responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('list')[y].get('name'),var,str(var2)), 'green'))
			else:
				if var2 is not None:
					print(colored('{} - WEAK'.format(responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('list')[y].get('name')), 'red'))
				else:	
					print(colored('{} - WEAK'.format(responsejson.get('endpoints')[cuenta].get('details').get('suites')[x].get('list')[y].get('name')), 'red'))



	fecha = str(responsejson.get('certs')[0].get('notAfter'))
	fecha = (fecha[0:10:1])
	dia = time.strftime('%Y-%m-%d', time.localtime(int(fecha)))
	print (colored("\nEl certificado expira el dia: " + str(dia) + "\n", 'yellow'))

###################COMIENZO DEL MAIN##################################################

#Argumentos del programa en este caso -f y -ex
parser = argparse.ArgumentParser(description='Version: 1 - This script ...')
parser.add_argument('-hs','--Host', help='Insert Host to analyce ssl certs\n\n', required=True)
parser.add_argument('-ex','--exportFile', help='Export results to text file\n\n', required=False)
args = parser.parse_args()

response = requests.get("https://api.ssllabs.com/api/v3/analyze?host=%s&all=on&fromCache=on&ignoreMismatch=on"%args.Host)
time.sleep(2)
response = requests.get("https://api.ssllabs.com/api/v3/analyze?host=%s&all=on&fromCache=on&ignoreMismatch=on"%args.Host)
responsejson = json.loads(response.text)
try:

	if responsejson.get('status') == "IN_PROGRESS":

		while True:
			print ('Esta realizandose el escaneo de los certificados en ' + args.Host)
			time.sleep(45)
			responseNew = requests.get("https://api.ssllabs.com/api/v3/analyze?host=%s&all=on&fromCache=on&ignoreMismatch=on"%args.Host)
			responsejsonNew = json.loads(responseNew.text)
			if responsejsonNew.get('status') == "READY":
				DatosCorrectos(responsejsonNew)
				break
	#print (responsejson.get('endpoints')[1].get('details').get('suites'))
	
	else:
		DatosCorrectos(responsejson)

except Exception as e:
	print("No se a podido obtener información acerca de ese dominio. Asegurese que es ese dominio"
		" si es asi pruebe a analizar ese dominio de nuevo")
