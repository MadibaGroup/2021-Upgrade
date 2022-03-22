import json
import requests
import time


def json_response(_para):
  url = "https://api.archivenode.io/MyToken"
  headers = {"content-Type: application/json"}
  payload = {
    "method":"trace_block",
    "params":[_para],
    "id":1,
    "jsonrpc":"2.0"
    }
  response = requests.post(url, data=json.dumps(payload)).json()
  return response

start_block = int(input("Enter Start Block Number: "))

end_block =  int(input("Enter End Block Number: "))


block_number=""
filename = ""
for i in reversed(range(start_block,end_block)):
  block_number=i
  try:
    data = json_response(block_number)
    print(i)
    filename= str(block_number) + '.json'
    with open(filename, 'w') as fp:
      json.dump(data, fp)
    fp.close()
  except:
    print("can't fetch block number: ",i)



##########################
######  12864595   #######
##########################





#################################################################################################
#def find_proxy_addresses(_data):
#   for i in range(len(_data["result"])):
#     if "callType" in _data["result"][i]["action"]:
#       if(_data["result"][i]["action"]["callType"] == "delegatecall"):
#         if "input" in _data["result"][i]["action"]:
#           if "input" in _data["result"][i-1]["action"]:
#             if(_data["result"][i]["action"]["input"] == _data["result"][i-1]["action"]["input"]):

#               a.append([_data["result"][i]["action"]["from"] , _data["result"][i]["transactionHash"]])
#           # print(_data["result"][i]["action"]["from"])
###################################################################################################