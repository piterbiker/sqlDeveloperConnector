import os
from xml.dom import minidom
import cx_Oracle
import getpass
from walidacja import get_integer, get_string
from konnektKonfig import sciezkaZr, sciezkaCel

def connParseXml():
    """
    funkcja connParseXml() parsuje plik polaczen programu SQL Developer 4.1 i tworzy tablice polaczen
    """
    # plik polaczen SQL Developer 4.1
    xmlFile = 'connections.xml'

    # pelna sciezka pliku polaczen SQL Developer 4.1
    connFile = os.path.join(sciezkaZr, xmlFile)

    # parsowanie pliku XML polaczen
    drzewo = minidom.parse(connFile)
    el1 = drzewo.getElementsByTagName("Reference")

    # budowanie tablicy polaczen
    polacz = []
    for i in el1:
        polaczenia = i.getAttribute("name")

        # budowanie slownika pojedynczego polaczenia
        slownik = {}
        dane = i.getElementsByTagName("StringRefAddr")
        for j in dane:
            test = j.getAttribute('addrType')

            if test == "OracleConnectionType":
                typPol = j.childNodes[1].childNodes[0].data
            
            if typPol.upper() == 'BASIC':

                if test == "ConnName":
                    slownik['nazwa'] = j.childNodes[1].childNodes[0].data
                if test == "sid":
                    slownik['sid'] = j.childNodes[1].childNodes[0].data
                if test == "port":
                    slownik['port'] = int(j.childNodes[1].childNodes[0].data)
                if test == "user":
                    slownik['user'] = j.childNodes[1].childNodes[0].data
                if test == "hostname":
                    slownik['hostname'] = j.childNodes[1].childNodes[0].data

            if typPol == 'TNS':

                if test == "ConnName":
                    slownik['nazwa'] = j.childNodes[1].childNodes[0].data
                if test == "user":
                    slownik['user'] = j.childNodes[1].childNodes[0].data
                if test == "customUrl":
                    slownik['dns'] = j.childNodes[1].childNodes[0].data

        polacz.append(slownik)

    # zapis tablicy polaczen slownikowych do lokalnego pliku
    zapisKonfiguracji(polacz)

    # funkcja zwraca tablice polaczen
    return polacz


def polaczenieOracle(domyslnePolacz=None, testWeryfikacji=True):
    """
    funkcja polaczenieOracle polaczenia do bazy Oracle, zwraca zmienna polaczenia
    domyslnePolacz: ID polaczenia z tablicy polaczen, domyslne pierwsze
    testWeryfikacji: czy wyswietlac info o weryfikacji polaczen
    """

    # pobranie tablicy polaczen wygenerowanej przez funcje connParseXml()
    polacz = connParseXml()

    # wyswietlanie listy dostepnych polaczen ze zmiennej tablicowej polacz
    if domyslnePolacz == None:
        print ('Wybierz polaczenie:\n')
        licznik=0
        liczbaPol = len(polacz)
        maks = liczbaPol-1
        for polaczenie in polacz:
            print ("\t[%d]: %s" % (licznik, polaczenie['nazwa']))
            licznik = licznik+1
        nrPolaczenia = get_integer('-> ', 'nrPolaczenia', 0, 0, maks, True)
    else:
        nrPolaczenia = domyslnePolacz

    # wyswietlanie info o weryfikacji polaczen
    if testWeryfikacji == True:
        weryfikacja = get_integer('Weryfikowac dane polaczenia ' + polacz[nrPolaczenia]['nazwa'] + '?', 'weryfikacja', 0, 0, 1, True)
        weryfikacja = int(weryfikacja)
    else:
        weryfikacja = 0

    # wybor parametrow polaczenia    
    print ("\nPolaczenie %s:\n" % (polacz[nrPolaczenia]['nazwa']))
    uzytkownik = get_string("\tUzytkownik: ", "uzytkownik", default=polacz[nrPolaczenia]['user'])
    inform1 = "\tHaslo uzytkownika %s" % (uzytkownik)
    haselko = getpass.getpass(inform1)

    # polaczenia typu Basic
    if 'hostname' in polacz[nrPolaczenia]:
        typPolaczenia = 'SID'
    
        if weryfikacja == 1:
    
            hostip = get_string("\tHost IP: ", "hostip", default=polacz[nrPolaczenia]['hostname'])
            porcik = get_integer("\tNumer portu: ", "porcik", polacz[nrPolaczenia]['port'], 1, 10000, False)
            orid = get_string("\tOracle ID: ", "orid", default=polacz[nrPolaczenia]['sid'])
    
        else:
            hostip = polacz[nrPolaczenia]['hostname']
            porcik = polacz[nrPolaczenia]['port']
            orid = polacz[nrPolaczenia]['sid']
    
        conn_str = "%s/%s@%s:%d/%s" % (uzytkownik, haselko, hostip, porcik, orid)
    
    # polaczenia typu TNS
    elif 'dns' in polacz[nrPolaczenia]:
        typPolaczenia = 'DNS'
    
        if weryfikacja == 1:
    
            dns = get_string("\tDNS: ", "dns", default=polacz[nrPolaczenia]['dns'])
    
        else:
            dns = polacz[nrPolaczenia]['dns']
    
        conn_str = "%s/%s@%s" % (uzytkownik, haselko, dns)

    input("\nLancuch polaczenia: %s" % (conn_str))

    # tworzenie zmiennej polaczenia
    try:
        db = cx_Oracle.connect(conn_str)
    except Exception as e:
        bladl = 'Blad polaczenia %s:\n%s' % (conn_str, e.message)   
        input(bladl)
        db = None
    else:       
        print ('\nWersja serwera: ' + db.version)
    finally:
        return db


# funkcja zapisu tablicy polaczen slownikowych do lokalnego pliku
def zapisKonfiguracji(dozapisu):
    polaczStr = str(dozapisu)
    polaczStr = polaczStr.replace("[", "[\n")
    polaczStr = polaczStr.replace("]", "\n]")
    polaczStr = polaczStr.replace("}, {", "}, \n{")
    polaczStr = 'polacz = ' + polaczStr

    plikKonfig = 'konfig.py'
    
    open1 = open(os.path.join(sciezkaCel, plikKonfig), 'w')
    open1.write(polaczStr)
    open1.close()


