#!/usr/bin/env python
import requests
import urllib
import socket
from termcolor import colored
import xlsxwriter
import argparse

n200 = 0
n302 = 0
n404 = 0
n80 = 0
n301 = 0
n443 = 0
total = 0
contador = 1

#Argumentos del programa en este caso -f y -ex
parser = argparse.ArgumentParser(description='Version: 1 - This script ...')
parser.add_argument('-f','--file', help='Indicate ip list file to process\n\n', required=True)
parser.add_argument('-ex','--exportXLSX', help='Export results to a XLSX file\n\n', required=True)
args = parser.parse_args()

print(colored(' **************************************************** ', 'yellow'))

#Funcion que nos suma los codigos de estado de las distintas web que visitamos
def processStatusCode(status_code):
    global n200
    global n302
    global n404
    global n301
    if r.status_code == 200:
        n200 += 1
    elif r.status_code == 302:
        n302 += 1
    elif r.status_code == 404:
        n404 += 1
    elif r.status_code == 301:
        n301 += 1

try:
    def excelWriter(r1,r2,r3):
        global contador
        fileout_sheet.write(contador, 0, r1)
        fileout_sheet.write(contador, 1, r2)
        fileout_sheet.write(contador, 2, r3)
        contador += 1

    #Si hemos puesto el parametro exportXLSX lo que va a realizar las siguientes lineas 
    #de comando es escribrirnos las cabeceras del documento excel 
    if args.exportXLSX is not None:
        fileoutXLSX = xlsxwriter.Workbook(args.exportXLSX + '.xlsx')  
        fileout_sheet = fileoutXLSX.add_worksheet()
        bold = fileoutXLSX.add_format({'bold': True})
        fileout_sheet.write(0, 0, 'URL', bold)
        fileout_sheet.write(0, 1, 'STATUS CODE', bold)
        fileout_sheet.write(0, 2, 'REDIRECT', bold)

    if args.file is not None:
        #contador = 1
        try:
            with open(args.file, 'r') as file:
                print(colored(' Processing file:   ' + str(args.file), 'blue'))
                for line in file.readlines():   
                    line_ip = line.split('\n')[0]
                    total += 1
                    try:
                        #URL = 'https://app.cajamar.es'
                        try:
                            global URL
                            URL = line_ip    
                            r = requests.get(URL, allow_redirects=False)
                            print('-------------------------------')
                            #print(r)

                            #Comprobamos si el status code es 404 y si es asi que nos imprima
                            #en el excel  la url el estatus code 404 y null y nos muestra en pantalla
                            #el mensaje de error Status Code 404.
                            if r.status_code == 404 and args.exportXLSX is not None:
                                excelWriter(r.url, r.status_code, 'null')
                                print(' Status Code: ',r.status_code)
                                processStatusCode(r.status_code)

                            #Imprimimos por pantalla los datos d e las diferentes direcciones urls
                            #En este caso la url, el codigo de estado, y la ultima redirección
                            print(colored(' URL:               {}'.format(r.url), 'red'))
                            fileout_sheet.write(contador, 0, r.url)
                            fileout_sheet.write(contador, 1, r.status_code)
                            fileout_sheet.write(contador, 2, r.headers['Location'])
                            
                            #En estas lineas se escriben en el documento excel las webs (url, codigo de estado
                            #y mredireccion de las urls que contengan un status code diferente de 404)
                            
                            if args.exportXLSX is not None:

                                if r.status_code != 404:
                                    excelWriter(r.url, r.status_code, r.headers['Location'])


                                """
                                if r.status_code != None and r.status_code == 404:
                                    r2 = r.history
                                    excelWriter(r2.url, r2.status_code, r2.headers['Location'])
                                    n404 += 1
                                """

                            print(' Status code:       {}'.format(r.status_code))
                            processStatusCode(r.status_code)

                            print(' Destination:       {}'.format(r.headers['Location']))

                            if 'https://' in r.headers['Location']:
                                n443 += 1
                            else:
                                pass
                                


                        except Exception as e:
                            #print(' Request Error: {}'.format(e))
                            pass

                    except Exception as e:
                        print(' Warning: {} {}'.format(URL, e))
                        pass

                print('-------------------------------------------------------------------')


                print(colored(' Status Codes:','yellow'))


                if n200 == 0:
                    print(colored('                    200({})'.format(n200),'yellow'))
                else:
                    print(colored('                    200({})'.format(n200),'yellow'))
                if n301 == 0:
                    print(colored('                    301({})'.format(n301),'yellow'))
                else:
                    print(colored('                    301({})'.format(n301),'red'))
                if n302 == 0:
                    print(colored('                    302({})'.format(n302),'yellow'))
                else:
                    print(colored('                    302({})'.format(n302),'red'))
                if n404 == 0:
                    print(colored('                    404({})'.format(n404),'yellow'))
                else:
                    print(colored('                    404({})'.format(n404),'red'))

                print(colored(' Redirections:      443({})'.format(n443),'green'))
                print(colored(' Total host:           ({})'.format(total),'yellow'))
                print('-------------------------------------------------------------------')

                if args.exportXLSX is not None:
                        print(colored(' --- Excel file ' + str(args.exportXLSX) + '.xlsx has been generated ---' + '\n', 'yellow'))

        except Exception as e:
            print(' Fatal Error: {}'.format(e))

        finally:
            if args.exportXLSX is not None:
                fileoutXLSX.close()

    print(colored(' **************************************************** ', 'yellow'))

except Exception as e:
    print(' Fatal Error: {}'.format(e))

