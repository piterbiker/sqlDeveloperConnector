from konnekt import polaczenieOracle

# polaczenieOracle(domyslnePolacz=None, testWeryfikacji=True)
db = polaczenieOracle()
c1 = db.cursor()

# testowe zapytanie do bazy do wykonania
querystring = "select SYSDATE, (SYSDATE - interval '1' day) from DUAL"

try: 
    c1.execute(querystring)
except Exception as e:
    bladl = 'Blad :%s' % (e)   
    print(bladl)
    pass
else:
    for row in c1:
        print ("%s %s" % (row[0], row[1]))
    input('Gotowe!')
finally:
    db.close()
