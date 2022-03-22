import json
import requests
import time

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
  code = response["result"]
  return code


filename = "Upgradeable_proxy_addresses_without_forwarders.txt"
f= open (filename, 'r')
fp = open ('Bytecodes.txt', 'w')

kk=0
for line in f:
    print(kk)
    kk+=1
    address = line.split(',')[0]
    try:
      bytecode = json_response(address)
      fp.write(address + ',' + bytecode + '\n')
      
    except:
      time.sleep(20)
      print('W8')
      bytecode = json_response(address)
      fp.write(address + ',' + bytecode + '\n')
f.close()
fp.close()
