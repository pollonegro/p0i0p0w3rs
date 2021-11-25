# -*- coding: utf-8 -*-
#!/usr/bin/env python
#	SCRAPING DE RESULTADOS DE DATOS HISTORICOS DNS:
# 	https://securitytrails.com/domain/altasadsl.vodafone.es/history/a
import sys, urllib, requests, json, argparse, time, re
from termcolor import colored
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Version: 1.0 - This script intend to obtain real ip bypassing WAFs by Historical DNS data')
parser.add_argument('-t','--target', help="Indicate domain to process \n\n",required=True)
args = parser.parse_args()

try:
	if args.target is not None: 
		cleanParam = args.target
		if 'http://' in cleanParam:
			cleanParam =  cleanParam.replace("http://", "")
			cleanParam =  socket.gethostbyname(cleanParam)

		if 'https://' in cleanParam:
			args.target =  args.target.replace("https://", "")
			args.target =  socket.gethostbyname(cleanParam)

		if 'www.' in cleanParam:
			cleanParam =  cleanParam.replace("www.", "")
			cleanParam =  socket.gethostbyname(cleanParam)
			args.target = cleanParam

		'''
		# https://securitytrails.com/domain/altasadsl.vodafone.es/history/a
		with urllib.request.urlopen('https://securitytrails.com/domain/' + args.target + '/history/a') as url:
			data = json.loads(url.read().decode())

			print("Entra")
			results = data.get('ip')

			print(results)
		'''

		url = ('https://securitytrails.com/domain/' + args.target + '/history/a')

		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		#print(re.findall(r'\b25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\.25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?\b',soup))








		#print(soup) # IMPRIME LA WEB AL COMPLETO ---- PARA CONTROL ----

	else:
		print(colored(' Warning: Need indicate domain to process, use -h for help', 'yellow'))
		sys.exit(1)

	print(colored(' --- The execution has been completed --- ', 'yellow'))

except Exception as e:
	print(colored(' Fatal Error: {}'.format(e), 'yellow'))
	sys.exit(1)