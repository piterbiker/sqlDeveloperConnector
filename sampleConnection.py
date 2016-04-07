from konnekt import polaczenieOracle

# polaczenieOracle(domyslnePolacz=None, testWeryfikacji=True)
db = polaczenieOracle()
c1 = db.cursor()

# testowe zapytanie do bazy do wykonania
querystring = ''

try: 
    c1.execute(querystring)
except Exception, e:
    bladl = 'Blad :%s' % (e.message)   
    print(bladl)
    pass
else:
    for row in c1:
        print "%s %s" % (row[0], row[1])
    raw_input('Gotowe!')
finally:
    db.close()
