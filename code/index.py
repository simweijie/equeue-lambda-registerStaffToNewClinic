import sys
import logging
import pymysql
import json
import os

#rds settings
rds_endpoint = os.environ['rds_endpoint']
username=os.environ['username']
password=os.environ['password']
db_name=os.environ['db_name']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Connection
try:
    connection = pymysql.connect(host=rds_endpoint, user=username,
        passwd=password, db=db_name)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def handler(event, context):
    cur = connection.cursor()  
## Retrieve Data
    ##CLINIC
    query1 = "INSERT INTO Clinic(name) VALUES ('{}')".format(event['clinicName'])
    cur.execute(query1)
    query2 = "SELECT id from Clinic where name = '{}'".format(event['clinicName'])
    cur.execute(query2)
    clinicId = cur.fetchone()[0]
    print("clinicId: ", clinicId)
    ##BRANCH
    index = 0
    staffBranchId = 0
    branches = event["branches"]
    for branch in branches:
        query3 = "INSERT INTO Branch(name,district,addr,postal,contactNo,latt,longt,clinicId) \
            VALUES('{}','{}','{}','{}','{}','{}','{}','{}')"\
                .format(branch['branchName'],branch['district'],branch['addr'],branch['postal'],\
                    branch['contactNo'],branch['latt'],branch['longt'],clinicId)
        cur.execute(query3)
        query4 = "SELECT id from Branch where name = '{}'".format(branch['branchName'])
        cur.execute(query4)
        branchId = cur.fetchone()[0]
        print("branchId: ", branchId)
        if(index ==0):
            staffBranchId= branchId
            index+=1
        openingHours = branch["openingHours"]
        for openingHour in openingHours:
            query = "INSERT INTO OpeningHours(opens,closes,dayOfWeek,branchId) VALUES('{}','{}','{}','{}')".format(openingHour['opens'],openingHour['closes'],openingHour['dayOfWeek'],branchId)
            cur.execute(query)
    ##STAFF
    query5 = "INSERT INTO Staff(email,password,name,addr,contactNo,job,status,isAdmin,branchId) \
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
        .format(event['email'], event['password'], event['name'], event['addr'], event['contactNo'], event['job'],'A','Y',staffBranchId)
    cur.execute(query5)
    connection.commit()
    print(cur.rowcount, "record(s) affected")
## Construct body of the response object
    transactionResponse = {}
# Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type']='application/json'
    responseObject['headers']['Access-Control-Allow-Origin']='*'
    responseObject['body'] = json.dumps(transactionResponse, sort_keys=True,default=str)
    
    #k = json.loads(responseObject['body'])
    #print(k['uin'])

    return responseObject