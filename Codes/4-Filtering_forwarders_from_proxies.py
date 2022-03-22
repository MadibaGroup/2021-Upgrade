import json
import requests
import time

a= ""

def json_response(_address):
  url = "https://api.archivenode.io/MyToken"
  headers = {"content-Type: application/json"}
  payload = {
    "method":"eth_getCode",
    "params":[_address],
    "id":1,
    "jsonrpc":"2.0"
    }
  response = requests.post(url, data=json.dumps(payload)).json()
  return response



###############################
number_of_file = input("enter the number: ")
f = open("Unique_proxy_addresses_and_to_addresses"+ number_of_file+ ".txt", "r")
i=0

fp= open("Upgradeable_proxy_addresses_without_forwarders"+ number_of_file+ ".txt", "w")

fqr= open("Unique_proxy_addresses_and_to_addresses200.txt", "a")
k=0

for line in f:
    print(i)
    unique_address= line.split(',')[0]
    to_address1= line.split(',')[1].replace('\n','')
    to_address= to_address1.replace('0x','')
    corrected = unique_address.replace('\n','')
    if i%10==0:
        time.sleep(1)
    try:
      response= json_response(corrected)
      i+=1
      if "result" in response:
          code = response["result"]
          if code.find(to_address) != -1 :
                print(corrected)
          else:
            a+= corrected + ',' + to_address1 +'\n'
            k+=1
            if k% 50 == 0:
              fp.write(a)
              a=''
    except:
      time.sleep(20)
      i+=1
      print("W8")
      fqr.write(line)
    

fp.write(a)
f.close()
fp.close()
###############################