import requests
import json
from datetime import datetime

#http://52.229.94.153:8080
def uploadData(referenceNumber,count,authorizationId,static_ip):
        dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")# dd/mm/YY H:M:S
        link = 'http://'+ static_ip + ':8080/data/upload/' + authorizationId
        headers={'Content-type':'application/json', 'Accept':'application/json'}
        data = json.dumps({"referenceNumber" : referenceNumber,"count" : count,"timeStamp" : dt_string})
        response = requests.post(link, data = data,headers=headers)
        print(response.text)#print response
        print("Data sent to server")

 #Just to show how its runs must be removed
#referenceNumber = 0                   #ref number of court
#count = 2228                          #count of people on court
#authorizationId = "2OCC9876543210"    #use this auth Id its already registered in backend and is owned ny lyndwood manager and this device is named test data upload
#static_ip = "52.229.94.153"               #ip address of server
# uploadData(referenceNumber,count,authorizationId,static_ip)
