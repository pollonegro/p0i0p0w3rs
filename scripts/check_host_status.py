#!/usr/bin/python

import httplib,sys
from urlparse import urlparse

global code_200
global code_301
global code_302
global code_401
global code_403
global code_404

def check_status():

	code_200 = 0
	code_301 = 0
	code_302 = 0
	code_401 = 0
	code_403 = 0
	code_404 = 0

	with open("hostnames.txt", "r") as hostnames:
		for hostname in hostnames:

			print "Hostname: " + hostname 
			host = hostname.strip("\n")
			http_url = "http://" + host 
			https_url = "https://" + host

			try:

				url = urlparse(http_url)
        			conn = httplib.HTTPConnection(url.netloc)
        			conn.request("HEAD", url.path)

        			code = str(conn.getresponse().status)

				if code == '200':

                			code_200 +=1

        			elif code == '301':

                			code_301 += 1

        			elif code == '302':

                			code_302 += 1

        			elif code == '401':

                			code_401 += 1

        			elif code == '403':

                			code_403 += 1

				else:

					print "No response"

				print "Connect port 80"

			except Exception:
				print "No response port 80"
				pass

			finally:

				try:
					url = urlparse(https_url)
                                	conn = httplib.HTTPConnection(url.netloc)
                                	conn.request("HEAD", url.path)

                                	code = str(conn.getresponse().status)

                                 	if code == '200':

                                        	code_200 +=1

	                                elif code == '301':

        	                                code_301 += 1

                	                elif code == '302':

                        	                code_302 += 1

                                	elif code == '401':

                                        	code_401 += 1

	                                elif code == '403':

	                                        code_403 += 1

        	                        elif code == '404':

						code_404 +=1

					else:

                	                        print "No response"

					print "Connect port 443"

				except Exception:

					print "No response 443"
					pass

				finally:

					print ("-----------------------------")


	print "Statistics"
	print "Code 200 " + str(code_200)
	print "Code 301 " + str(code_301)
	print "Code 302 " + str(code_302)
	print "Code 401 " + str(code_401)
	print "Code 403 " + str(code_403)
	print "Code 404 " + str(code_404)

check_status()




