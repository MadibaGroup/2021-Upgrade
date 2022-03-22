a=""
b=[]

f = open("Proxy_addresses_and_transacionHash_to_addresses.txt", "r")
k=0
for line in f:
    print(k)
    k+=1
    address=line.split(",")[0]
    toaddress= line.split(",")[2]
    toaddresses= toaddress.replace('\n','')
    if address not in b:
      a+= address + ','+ toaddresses  +'\n' 
      b.append(address)

fp= open("Unique_proxy_addresses_and_to_addresses.txt", "w")
fp.write(a)
f.close()
fp.close()

