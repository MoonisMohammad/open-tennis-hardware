import requests
import json
from datetime import datetime

#http://52.229.94.153:8080
def uploadData(referenceNumber,count,authorizationId,static_ip):
        dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")# dd/mm/YY H:M:S
        link = 'http://'+ static_ip + ':8080/data/upload/' + authorizationId
        headers={'Content-type':'application/json', 'Accept':'application/json'}
        data = json.dumps({"referenceNumber" : referenceNumber,"count" : count,"timeStamp" : dt_string})
        response = requests.post(link, data = json.dumps({"referenceNumber" : referenceNumber,"count" : count,"timeStamp" : dt_string}),headers=headers)
        print(response.text)#print response

 


