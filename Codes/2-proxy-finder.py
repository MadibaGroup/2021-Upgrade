import json
import requests
import time


str1=""

def find_proxy_addresses(_data):
  global str1
  if "result" in _data:
    for i in range(len(_data["result"])):
      if "action" in _data["result"][i]:
        if "callType" in _data["result"][i]["action"]:
          if(_data["result"][i]["action"]["callType"] == "delegatecall"):
            if "input" in _data["result"][i]["action"]:
              if "input" in _data["result"][i-1]["action"]:
                if(_data["result"][i]["action"]["input"] == _data["result"][i-1]["action"]["input"]):
                  str1 += _data["result"][i]["action"]["from"] + "," + _data["result"][i]["transactionHash"] + ","+ _data["result"][i]["action"]["to"]  + "\n"

start_block = int(input("Enter Start Block Number: "))

end_block =  int(input("Enter End Block Number: "))

block_number=""
filename = ""

k=0
fp = open("Proxy_addresses_and_transacionHash_to_addresses.txt", "a")
frm = open('missed_blocks.txt','a')

for i in reversed(range(start_block,end_block)):
  if i%100 == 0:
    fp.write(str1)
    str1=''
  block_number=i
  filename= str(block_number) + '.json'
  try:
    f = open(filename,)
    data = json.load(f)
    find_proxy_addresses(data)
    f.close()
    print(k)
    k+=1
  except IOError:
    print("File" + filename + "not accessible")
    frm.write(filename + '\n')





fp.write(str1)
fp.close()



##########################
######  1. 12854595
######  2. 12813795
######  3. 12700000
######  3. 12600000
######  3. 
######  3. 
######  3. 


##########################
