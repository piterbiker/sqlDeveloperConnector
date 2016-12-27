import redis
from konnekt import polaczenieOracle

# oracle connection from konnekt module
db = polaczenieOracle(1, None)

# Create a connection to the Redis serer
rdb = redis.StrictRedis()


def getAttributeName(oracleConn, queryAttr):
    """
    Get attribute name from Oracle table by primary key field
    """
    c1 = oracleConn.cursor()
    attrNames = []

    try: 
        c1.execute(queryAttr)
    except Exception as e:
        err1 = 'Error when execute %s: %s' % (queryAttr, e)   
        print(err1)
    else:
        for i in range(0, len(c1.description)):
            attrNames.append(c1.description[i][0])

    finally:
        c1.close()
        return attrNames


def getObjectById(
        oracleConn,              # connection to Oracle database (source)
        redisConn,                # connection to Redis database (destination)
        tableName,              # table name in Oracle database
        primaryKey,             # primary key field
        primaryKeyValue    # promary field value (search object))
        ):

    c2 = oracleConn.cursor()
    queryString = "select * from {}".format(tableName)
    
    # default settings: TODO for all record in source table
    if primaryKey:
        redisKey = "{}[{}:{}]".format(tableName.lower(), primaryKeyValue, primaryKey.lower())
        subQueryString = " where {} = {}".format(primaryKey, primaryKeyValue)
        queryString += subQueryString

    attrNames = getAttributeName(oracleConn, queryString)

    if redisKey:
        if redisConn.exists(redisKey):
            for attr in attrNames:
                redisAttr = "{}[{}:{}]".format(tableName.lower(), primaryKeyValue, attr.lower())
                # print all value in Redis databese with ID equal to searching primary key in Oracle table 
                print (redisConn.get(redisAttr))
        
        else:
            try: 
                c2.execute(queryString)
            except Exception as e:
                err2 = 'Error when execute %s: %s' % (queryString, e)   
                print(err2)
            else:
                row = c2.fetchone()
                for cols in range(0, len(row)):
                    redisSetKey = "{}[{}:{}]".format(tableName.lower(), primaryKeyValue, c2.description[cols][0].lower())
                    redisSetValue = row[cols]
                    try:
                        # add all keys to Redis database with value from record in Oracle table witch searching primary key 
                        redisConn.set(redisSetKey, redisSetValue)
                    except Exception as e:
                        err3 = 'Error when set %s to Redis Database: %s' % (redisSetKey, e)   
                        print(err3)
                    else:
                        print('Sucessfully added key %s to Redis Database' % (redisSetKey))

            finally:
                c2.close()
                db.close()


if __name__ == "__main__":
    getObjectById(db, rdb, 'COUNTRIES', 'ID', 1)

