#!/usr/bin/python

#script for enumerating directories and obtain information in web applications
#Developed by Jose Maria Bedoya
#v1.6.5b

import argparse, binascii, time, subprocess, random, sys, httplib, ssl, xlsxwriter, time, requests
from argparse import RawTextHelpFormatter
from multiprocessing import Pool
from Queue import Queue
from threading import Thread
from time import time, sleep

#Definition and treatment of the parameters
parser = argparse.ArgumentParser(description='Version: 1.6.5b\nThis script intend to make a list of the application directories and obtain certain information about the web server.', formatter_class=RawTextHelpFormatter)
parser.add_argument('-u','--url', help="Indicate the url direction to enumerate, without 'http://' prefix\n\n",required=True)
parser.add_argument('-p','--port', help="Indicate the port of the url (Default: 80)\n\n",required=False, default=80)
parser.add_argument('-P','--protocol', help='Perform requests with a specific protocol (HTTP or HTTPS)\n\n', required=False)
parser.add_argument('-i','--info', help="Shows certain information about the target like HTTP headers, cookies and HTTP methods. (this action require more requests over the target)\n\n",required=False, action='store_true')
parser.add_argument('-d','--dictionary', help="Indicate the path of the dictionary to use for the enumeration\n\n",required=True)
parser.add_argument('-D','--delay', help="Indicate a delay between requests\n\n",required=False)
parser.add_argument('-t','--thread', help='Indicate the number of threads to use for the enumeration\n\n',required=False)
parser.add_argument('-r','--respond', nargs='*', help="Filter response codes to display (separated by spaces):\n\
	200\n\
	302\n\
	404\n\
	401\n\
	403\n\
	500\n\n",required=False)
parser.add_argument('-ej','--export', help='Export the results to a json file\n\n', required=False)
parser.add_argument('-ex','--exportXLS', help='Export the results to a XLSX file\n\n', required=False)
parser.add_argument('-E','--extension', help='Perform requests with a specific file extension\n\n', required=False)
parser.add_argument('-R','--recursive', help='Perform recursive requests to directories that respond with ok\n\n', required=False, action='store_true')
parser.add_argument('-pr','--proxy', help='Set a proxy for the connections (<IP address>:<port>)\n\n', required=False)
args = parser.parse_args()

#Execution
print "__          __  _     _    _                       _ "
print "\ \        / / | |   | |  | |                     | |"
print " \ \  /\  / /__| |__ | |__| | ___  _   _ _ __   __| |"
print "  \ \/  \/ / _ \ '_ \|  __  |/ _ \| | | | '_ \ / _` | "
print "   \  /\  /  __/ |_) | |  | | (_) | |_| | | | | (_| | "
print "    \/  \/ \___|_.__/|_|  |_|\___/ \__,_|_| |_|\__,_| "
print "***************************************************************************************************"
print "*** Author: Jose Maria Bedoya  									***"
print "***************************************************************************************************"
print "***************************************************************************************************"
print "				Server info											  "
print "***************************************************************************************************\n"

try:

	cont = 0
	responds = {}
	file = open(args.dictionary, 'r')
	q = Queue(maxsize=0)
	map(q.put, file)
	file.close()

	if args.export is not None:
		fileout = open(args.export + '.json', 'w', 0)
		fileout.writelines("{")
	elif args.exportXLS is not None:
		fileoutXLS = xlsxwriter.Workbook(args.exportXLS + '.xlsx')
		fileout_sheet = fileoutXLS.add_worksheet()
		bold = fileoutXLS.add_format({'bold': True})
		fileout_sheet.write(0, 0, 'URL Address', bold)
		fileout_sheet.write(0, 1, 'Response', bold)
		if args.info is True:
			fileout_sheet.write(0, 2, 'Headers', bold)
			fileout_sheet.write(0, 3, 'Set-Cookies', bold)
			fileout_sheet.write(0, 4, 'Methods', bold)
		cont_lines = 1

	def Socket(url, port, method, folder, ext, id):
		headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}
		try:
			#With Proxy
			if args.proxy is not None:
				Purl = str(args.proxy).split(':')[0]
				Pport = str(args.proxy).split(':')[1]			
				if id == 1:
					if method == "GET":
						conn = requests.get(url + ":" + port + "/" + folder + "." + ext, verify=False, proxies=args.proxy, headers=headers)
					elif method == "OPTIONS":
						conn = requests.options(url + ":" + port + "/" + folder + "." + ext, verify=False, proxies=args.proxy, headers=headers)
				else:
					if method == "GET":
						conn = requests.get(url + ":" + port + "/" + folder, verify=False, proxies=args.proxy, headers=headers)
					elif method == "OPTIONS":
						conn = requests.options(url + ":" + port + "/" + folder, verify=False, proxies=args.proxy, headers=headers)
			#Without Proxy
			else:				
				if id == 1:
					if method == "GET":
						print "hola1"
						conn = requests.get(url + ":" + port + "/" + folder + "." + ext, verify=False, headers=headers)
						print conn
					elif method == "OPTIONS":
						conn = requests.options(url + ":" + port + "/" + folder + "." + ext, verify=False, headers=headers)
				else:
					if method == "GET":
						print str(url) + ":" + str(port) + "/" + str(folder)
						conn = requests.get("https://" + str(url) + ":" + str(port) + "/" + str(folder), verify=False, headers=headers)
					elif method == "OPTIONS":
						conn = requests.options("https://" + str(url) + ":" + str(port) + "/" + str(folder), verify=False, headers=headers)
		except:
			print "ERROR: URL address/port is not valid or not exist.\n"
			##En principio no deberia de ser necesario salir del programa. Ver como controlar si pones una URL mal.
			#sys.exit(1)
		return conn
		
	def Info(resp, id):
		print "\n"
		head_info = ""
		if "x-powered-by" in resp.text:
			print "--> X-powered-by:", resp.headers['x-powered-by']
			head_info = head_info + "X-powered-by:" + resp.headers['x-powered-by'] + ", "
		if "Powered-By" in resp.text:
			print "--> Powered-by:", resp.headers['Powered-By']
			head_info = head_info + "Powered-by:" + resp.headers['Powered-By'] + ", "
		if "server" in resp.text:
			print "--> Server:", resp.headers['Server']
			head_info = head_info + "Server:" + resp.headers['Server'] + ", "
		if "X-OWA-Version" in resp.text:
			print "--> X-OWA-Version:", resp.headers['X-OWA-Version']
			head_info = head_info + "X-OWA-Version:" + resp.headers['X-OWA-Version'] + ", "
		if "X-Frame-Options" in resp.text:
			print "--> X-Frame-Options:", resp.headers['X-Frame-Options']
			head_info = head_info + "X-Frame-Options:" + resp.headers['X-Frame-Options'] + "."
		else:
			print "--> X-Frame-Options: The server didn't provide this header."
			head_info = head_info + "X-Frame-Options didn't provide."		
		cookie = resp.headers['Set-Cookie']
		if "Set-Cookie" in resp.text:
			print "\nCookies info"
			print "*************************************************************\n"
			for i in cookie.split(','):
				print "-->Set-Cookie:", i
				if "Secure" in cookie:
					print "\n'Secure' attribute defined in cookie."
				else:
					print "\n'Secure' attribute is not defined."
				if "HttpOnly" in cookie:
					print "'HttpOnly' attribute defined in cookie.\n"
				else:
					print "'HttpOnly' attribute is not defined.\n"
		#Export XLS info
		if args.exportXLS is not None and id != 0:
			fileout_sheet.write(cont_lines, 2, head_info)
			fileout_sheet.write(cont_lines, 3, cookie)
		
		print "\n"

	def results(line, resp, methods, id):
		global cont_lines
		if id == 1:
			out = args.url + "/" + line + "." + args.extension + "			+++	" + str(resp.status_code)
		else:
			out = args.url + "/" + line + "			+++	" + str(resp.status_code)
		
		if resp.status_code in responds:
			responds[resp.status_code] = responds[resp.status_code] + 1
		else:
			responds[resp.status_code] = 1
		
		if args.respond is not None:
			for i in args.respond:
				if i in str(resp.status_code):
					if args.export is not None and id == 1:
						out_export = "\"" + args.url + "/" + line + "." + args.extension + "\":\"" + str(resp.status_code) + "\","
						fileout.writelines(out_export)
					elif args.export is not None:	
						out_export = "\"" + args.url + "/" + line + "\":\"" + str(resp.status_code) + "\","
						fileout.writelines(out_export)
					#Export XLS
					if args.exportXLS is not None and id == 1:
						fileout_sheet.write(cont_lines, 0, args.url + "/" + line + "." + args.extension)
						fileout_sheet.write(cont_lines, 1, str(resp.status_code))
					elif args.exportXLS is not None:	
						fileout_sheet.write(cont_lines, 0, args.url + "/" + line)
						fileout_sheet.write(cont_lines, 1, str(resp.status_code))
					print out
					if args.info is True and args.exportXLS is not None:
						Info(resp, 1)
						print "Methods (" + args.url + "/" + line + "):", methods.headers['allow']
						fileout_sheet.write(cont_lines, 4, methods.headers['allow'])
						cont_lines +=1
					elif args.info is True:
						Info(resp, 1)
						print "Methods (" + args.url + "/" + line + "):", methods.headers['allow']
					elif args.exportXLS is not None:
						cont_lines +=1
					print "\n---------------------------------------------------------------------------------------------------\n",
					print "---------------------------------------------------------------------------------------------------\n\n",
		else:
			if args.export is not None and id == 1:
				out_export = "\"" + args.url + "/" + line + "." + args.extension + "\":\"" + str(resp.status_code) + "\","
				fileout.writelines(out_export)
			elif args.export is not None:	
				out_export = "\"" + args.url + "/" + line + "\":\"" + str(resp.status_code) + "\","
				fileout.writelines(out_export)
			#Export XLS
			if args.exportXLS is not None and id == 1:
				fileout_sheet.write(cont_lines, 0, args.url + "/" + line + "." + args.extension)
				fileout_sheet.write(cont_lines, 1, str(resp.status_code))
			elif args.exportXLS is not None:	
				fileout_sheet.write(cont_lines, 0, args.url + "/" + line)
				fileout_sheet.write(cont_lines, 1, str(resp.status_code))
			print out
			if args.info is True and args.exportXLS is not None:
				Info(resp, 1)
				print "Methods (" + args.url + "/" + line + "):", methods.headers['allow']
				fileout_sheet.write(cont_lines, 4, methods.headers['allow'])
				cont_lines +=1
			elif args.info is True:
				Info(resp, 1)
				print "Methods (" + args.url + "/" + line + "):", methods.headers['allow']
			elif args.exportXLS is not None:
				cont_lines +=1
				
			print "\n---------------------------------------------------------------------------------------------------\n",
			print "---------------------------------------------------------------------------------------------------\n\n",
		
		
	#Obtaining information
	response = Socket(args.url,int(args.port),"GET","","",0)
	print "Status:", response.status_code
	Info(response, 0)
	print "Based Response:\n"
	print response.headers
	print "\n"
	response2 = Socket(args.url,int(args.port),"OPTIONS","/","",0)
	print "HTTP Methods Allowed:", response2.headers['allow']
	print "\n"

	print "***************************************************************************************************"
	print "+			URL direction			+++		Response		+"
	print "***************************************************************************************************\n"

	def do_stuff(q):
	  global cont, Socket
	  while True:
		try:
			line = q.get()
		except:
			break
		resul = ""
		resulExt = ""
		line = line.strip()
		
		#Delay
		if args.delay is not None:
			sleep(float(args.delay))
		if args.extension is not None:
			resul = Socket(args.url,int(args.port),"GET",line,"",0)
			resulExt = Socket(args.url,int(args.port),"GET",line,args.extension,1)
			if args.info is True:
				methods = Socket(args.url,int(args.port),"OPTIONS","/" + line,args.extension,0)
				methodsExt = Socket(args.url,int(args.port),"OPTIONS","/" + line,args.extension,1)
			else:
				methods = ""
				methodsExt = ""
		else:
			resul = Socket(args.url,int(args.port),"GET",line,"",0)
			if args.info is True:
				methods = Socket(args.url,int(args.port),"OPTIONS","/" + line,"",0)
			else:
				methods = ""
		cont = cont + 1
		
		#Recursive 
		if (args.recursive is True) and ("200" in str(resul.status_code)):
			file2 = open(args.dictionary, 'r')
			for line2 in file2:
				line2 = line2.strip()
				rline = line + "/" + line2
				q.put(rline)
			file2.close()
		
		if args.extension is not None:
			results(line, resul, methods, 0)
			results(line, resulExt, methodsExt, 1)
		else:
			results(line, resul, methods, 0)
		
		q.task_done()
	
	tstart = time()
	if args.thread is not None:
		for i in range(int(args.thread)):
		  worker = Thread(target=do_stuff, args=(q,))
		  worker.setDaemon(True)
		  worker.start()
	else:
		  worker = Thread(target=do_stuff, args=(q,))
		  worker.setDaemon(True)
		  worker.start()
	q.join()

	tend = time()


		
	#Final result
	print "RESULTS"
	print "***************************************************************************************************"
	tfinal = tend - tstart
	print "Execution time: %.2f" % tfinal
	print "Total requests: " + str(cont)
	if args.export is not None:
		print "Exported results to \"" + args.export + ".json\""
	elif args.exportXLS is not None:
		print "Exported results to \"" + args.exportXLS + ".xlsx\""
	for k, v in responds.items():
		if v is not 0:
			print "--> Code " + str(k) + " responds: " + str(v)
	print "***************************************************************************************************\n"

except Exception as e:
	print "Error during the execution."
	
finally:
	if args.export is not None:
		linea = fileout.tell()
		fileout.seek(linea - 1)
		fileout.writelines("}")
		fileout.close()
	elif args.exportXLS is not None:
		fileoutXLS.close()
	
