#!/usr/bin/env python
import shodan
import re
import socket
import os, sys
import requests
import urllib2
import dns.resolver
import dns.resolver
import xlsxwriter
from time import sleep
import argparse
from ipaddress import ip_address
import struct


api_key = 'TrJLuBlD3vfXGPXYBF8CGYTXuweS6hat'                # <------------- API KEY HERE ---------- <<<<
hostnames3 = ''
puertosLimpios3 = ''
cveLimpio3 = ''

parser = argparse.ArgumentParser(description='Version: 1.1 - This script intend to obtain information with Shodan')
parser.add_argument('-t','--target', help="Indicate ip/domain/range to process \n\n",required=False)
parser.add_argument('-f','--file', help='Indicate ip list file to process\n\n', required=False)
parser.add_argument('-s','--silent', help="Dont show nothing in screen \n\n",required=False, action='store_true')
parser.add_argument('-a','--api', help="Set a custom Shodan API key \n\n",required=False)
parser.add_argument('-ex','--exportXLS', help='Export the results to a XLSX file\n\n', required=False)
args = parser.parse_args()


if args.exportXLS is not None:
    fileoutXLS = xlsxwriter.Workbook(args.exportXLS + '.xlsx')  
    fileout_sheet = fileoutXLS.add_worksheet()
    bold = fileoutXLS.add_format({'bold': True})
    fileout_sheet.write(0, 0, 'IP', bold)
    fileout_sheet.write(0, 1, 'ISP', bold)
    fileout_sheet.write(0, 2, 'ASN', bold)
    fileout_sheet.write(0, 3, 'LOCATION', bold)
    fileout_sheet.write(0, 4, 'PORTS', bold)
    fileout_sheet.write(0, 5, 'CVEs', bold)   
    fileout_sheet.write(0, 6, 'UPDATED', bold)
    contador = 1

if args.api is not None:
    api_key = args.api

api = shodan.Shodan(api_key)

def formatParams (results):

    global hostnames3
    global puertosLimpios3
    global cveLimpio3

    #Format parameters
    hostnames1 =  str(results.get('hostnames')).replace("', u'", " | ")
    hostnames2 =  hostnames1.replace("[u'", "")
    hostnames3 =  hostnames2.replace("']", "")
    puertosLimpios =  str(results['ports']).replace("[", "")
    puertosLimpios2 =  str(puertosLimpios).replace("]", "")
    puertosLimpios3 =  str(puertosLimpios2).replace(",", " -")
    cveLimpio =  str(results.get('vulns')).replace("', u'", " | ")
    cveLimpio2 =  cveLimpio.replace("[u'", " ")
    cveLimpio3 =  cveLimpio2.replace("']", " ")

def process (results):    

    formatParams (results)

    global hostnames3
    global puertosLimpios3
    global cveLimpio3

    #Print information
    if args.silent is False:

        print(' ****************************************************************** ')
        print('IP:           {}'.format(results['ip_str']))                       
        print('Hostnames:    {}'.format(hostnames3))
        print('ISP:          {}'.format(results['isp']))
        print('ASN:          {}'.format(results['asn']))
        
        try:
            ubicacion = '{} {} {} {}'.format(
            check(results['country_code3']),
            check(results['country_name']),
            check(results['city']),
            check(results['postal_code'])
            )

            print('Location:     {}'.format(ubicacion))

        except Exception,e:
            pass
        
        print('Ports:        {}'.format(puertosLimpios3))
        print('CVEs:         {}'.format(cveLimpio3))
        # ------------- VCE SECTION - SOMETIMES DESACTIVATED WHEN IMPLEMENTING BY SHODAN --------------

        print('Updated:      {}'.format(results.get('last_update')[0:10]))
        print(' ****************************************************************** ')

        for data in results['data']:
            puerto = data['port']

            print('-*- Port:     ' + str(data['port']))
            print('    Protocol: ' + str(data['transport']))
            
            try:
                if str(data['os']) == "None":
                    data['os'] = "N/A"
                else:
                    print('    OS:       ' + str(data['os']))
            
            except Exception,e:
                continue

            try:
                print('    Product:  ' + str(data['product']))
            
            except Exception,e:
                data['product'] = "N/A"
                continue
            
            try:
                print('    Version:  ' + str(data['version']))
            
            except Exception,e:
                data['version'] = "N/A"
                continue                  

        print('\n')

def check(param):
    if param==None:
        return ''
    else:
        return param

def excelWriter (results):

    formatParams (results)
    global hostnames3
    global puertosLimpios3
    global contador
    global cveLimpio3


    fileout_sheet.write(contador, 0, results['ip_str'])
    fileout_sheet.write(contador, 1, hostnames3)

    if str(results['isp']) == " ":
        fileout_sheet.write(contador, 2, 'N/A')
    else:
        fileout_sheet.write(contador, 2, str(results['isp']))

    ubicacion = '{} {} {} {}'.format(
        check(results['country_code3']),
        check(results['country_name']),
        check(results['city']),
        check(results['postal_code'])
    )

    fileout_sheet.write(contador, 3, ubicacion)
    fileout_sheet.write(contador, 4, puertosLimpios3)
    fileout_sheet.write(contador, 5, cveLimpio3)
    fileout_sheet.write(contador, 6, results.get('last_update')[0:10])

    contador += 1

print(' ****************************************************************** ')
       
if api_key == '':
    print('Shodan API key not defined, edit the script or use (-a) option.')
    sys.exit(1)

else:
    try:
        if args.target is not None: 

        	if '/' in args.target:

                print('Processing Range: ' + args.target)
                print(' ****************************************************************** ')

                #CONVERTING RANGE TO IPs -----------------------------------------------------
                class InvalidIPAddress(ValueError):
                    """The ip address given to ipaddr is improperly formatted"""


                def ipaddr_to_binary(ipaddr):
                    """
                    A useful routine to convert a ipaddr string into a 32 bit long integer
                    """
                    # from Greg Jorgensens python mailing list message
                    q = ipaddr.split('.')
                    return reduce(lambda a, b: long(a) * 256 + long(b), q)


                def binary_to_ipaddr(ipbinary):
                    """
                    Convert a 32-bit long integer into an ipaddr dotted-quad string
                    """
                    # This one is from Rikard Bosnjakovic
                    return socket.inet_ntoa(struct.pack('!I', ipbinary))


                def iprange(ipaddr):
                    """
                    Creates a generator that iterates through all of the IP addresses.
                    The range can be specified in multiple formats.

                        "192.168.1.0-192.168.1.255"    : beginning-end
                        "192.168.1.0/24"               : CIDR
                        "192.168.1.*"                  : wildcard
                    """
                    # Did we get the IP address in the span format?
                    span_re = re.compile(r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   # The beginning IP Address
                                             \s*-\s*
                                             (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   # The end IP Address
                                          ''', re.VERBOSE)

                    res = span_re.match(ipaddr)
                    if res:
                        beginning = res.group(1)
                        end = res.group(2)
                        return span_iprange(beginning, end)

                    # Did we get the IP address in the CIDR format?
                    cidr_re = re.compile(r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   # The IP Address
                                             /(\d{1,2})                             # The mask
                                          ''', re.VERBOSE)

                    res = cidr_re.match(ipaddr)
                    if res:
                        addr = res.group(1)
                        cidrmask = res.group(2)
                        return cidr_iprange(addr, cidrmask)

                    # Did we get the IP address in the wildcard format?
                    wild_re = re.compile(r'''(\d{1,3}|\*)\.
                                             (\d{1,3}|\*)\.
                                             (\d{1,3}|\*)\.
                                             (\d{1,3}|\*)   # The IP Address
                                          ''', re.VERBOSE)

                    res = wild_re.match(ipaddr)
                    if res:
                        return wildcard_iprange(ipaddr)

                    raise InvalidIPAddress


                def span_iprange(beginning, end):
                    """
                    Takes a begining and an end ipaddress and creates a generator
                    """
                    b = ipaddr_to_binary(beginning)
                    e = ipaddr_to_binary(end)

                    while (b <= e):
                        yield binary_to_ipaddr(b)
                        b = b + 1


                def cidr_iprange(ipaddr, cidrmask):
                    """
                    Creates a generator that iterated through all of the IP addresses
                    in a range given in CIDR notation
                    """
                    # Get all the binary one's
                    mask = (long(2) ** long(32 - long(cidrmask))) - 1

                    b = ipaddr_to_binary(ipaddr)
                    e = ipaddr_to_binary(ipaddr)
                    b = long(b & ~mask)
                    e = long(e | mask)

                    while (b <= e):
                        yield binary_to_ipaddr(b)
                        b = b + 1


                def wildcard_iprange(ipaddr):
                    """
                    Creates a generator that iterates through all of the IP address
                    in a range given with wild card notation
                    """
                    beginning = []
                    end = []

                    tmp = ipaddr.split('.')
                    for i in tmp:
                        if i == '*':
                            beginning.append("0")
                            end.append("255")
                        else:
                            beginning.append(i)
                            end.append(i)

                    b = beginning[:]
                    e = end[:]

                    while int(b[0]) <= int(e[0]):
                        while int(b[1]) <= int(e[1]):
                            while int(b[2]) <= int(e[2]):
                                while int(b[3]) <= int(e[3]):
                                    yield b[0] + '.' + b[1] + '.' + b[2] + '.' + b[3]
                                    b[3] = "%d" % (int(b[3]) + 1)

                                b[2] = "%d" % (int(b[2]) + 1)
                                b[3] = beginning[3]

                            b[1] = "%d" % (int(b[1]) + 1)
                            b[2] = beginning[2]

                        b[0] = "%d" % (int(b[0]) + 1)
                        b[1] = beginning[1]


                if __name__ == '__main__':
                    for ip in iprange(args.target):
                        
                        try:
                            ipv4 = socket.gethostbyname(ip)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
                        except Exception,e:
                            print(' !!!  IP not found: !!! {} '.format(ip))
                                                
                        try:
                            results = api.host(ipv4)
                            process(results)

                            #Export results to XLS file
                            if args.exportXLS is not None:           
                                excelWriter(results)  

                        except Exception,e:
                            print('Warning: {} {}'.format(ip, e))
                            #continue
                            sleep(1)


            else:
                print('Processing IP / Host: ' + args.target)
                try:
                    ipv4 = socket.gethostbyname(args.target)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                except Exception,e:
                    print(' !!!  IP / Host not found: !!! {} '.format(args.target))
                                        
                try:
                    results = api.host(ipv4)
                    process(results)

                    #Export results to XLS file
                    if args.exportXLS is not None:           
                        excelWriter(results)  

                except Exception,e:
                    print('Warning: {}'.format(e))
                    #continue
                    sleep(1)


        else:

            print('Processing file: ' + str(args.file)) 
            with open(args.file, 'r') as file:
                for line in file.readlines():   
                    line_ip = line.split('\n')[0]
                    sleep(.500)
                    try:
                        ipv4 = socket.gethostbyname(line_ip)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
                    except Exception,e:
                        print(' !!!  IP not found: !!! {} '.format(line_ip))
                        continue
                                            
                    try:
                        results = api.host(ipv4)
                        process(results)

                        #Export results to XLS file
                        if args.exportXLS is not None:                

                            excelWriter(results)

                    except Exception,e:
                        print('Warning: {}'.format(e))
                        continue
                        sleep(1)               
                                    
        if args.exportXLS is not None: 
            print('------ Excel file ' + str(args.exportXLS) + ' has been generated ------' + '\n')

        print('------ The execution has been completed ------' + '\n')

    except Exception as e:
        print 'Error: %s' % e
        sys.exit(1)

    finally:
        if args.exportXLS is not None:
            fileoutXLS.close()