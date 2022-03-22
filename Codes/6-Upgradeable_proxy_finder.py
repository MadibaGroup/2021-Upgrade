import os 
import subprocess as sp
import re
import json
import requests
import time

###########################################################################

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
###########################################################################

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
  if "result" in response:
        code = response["result"].replace('0x','')
  return code

###########################################################################

def decompilation(_bytecode):
    output = sp.getoutput('panoramix ' + _bytecode)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = ansi_escape.sub('', output)
    return result


###########################################################################

def delegated_lines_in_fallback (_code_lines):
    delegate_lines = []
    for rr in range(len(_code_lines)):
        if "payable:" in _code_lines[rr]:
            for kk in range(rr,len(_code_lines)):
                if "delegate" in _code_lines[kk]:
                    delegate_lines.append(_code_lines[kk])
                    break
    return delegate_lines


###########################################################################

def storage_variable(_code_lines):
    storage_variables = []
    storage_addresses = []
    for i in range(len(_code_lines)):
        if "def storage:" in _code_lines[i]:
            for k in range(i+1,len(_code_lines)):
                words = _code_lines[k].split(' ')
                for word in words:
                    if word != '':
                        storage_variables.append(word)
                        break
                for i in range(len(words)):
                    if words[i] == 'storage':
                        storage_addresses.append(words[i+1])
                if _code_lines[k] == '':
                    break
    return storage_variables, storage_addresses

###########################################################################

def match_finder(_storage_variables , _delegate_lines):
    implementation_address = []
    implementation_slot = []
    for i in range(len(_storage_variables[0])):
        for lines1 in _delegate_lines:
            if _storage_variables[0][i] in lines1:
                if _storage_variables[0][i] not in implementation_address:
                    implementation_address.append(_storage_variables[0][i])
                    implementation_slot.append(_storage_variables[1][i])
    for addr in implementation_slot:
        for j in range(len(_storage_variables[1])):
            if _storage_variables[1][j] == addr:
                if _storage_variables[0][j] not in implementation_address:
                    implementation_address.append(_storage_variables[0][j])
    for line in _delegate_lines:
        if "sha3" in line:
                inputs = line[line.find('sha3(') : line.rfind(')]')+1]
                implementation_address.append(inputs)

    return implementation_address

###########################################################################

def assignment_checker(_code_lines , _imps):
    for var in _imps:
        for i in range(len(_code_lines)):
            if var in _code_lines[i]:
                if "=" in _code_lines[i]:
                    if "if" not in _code_lines[i]:
                        picked_var = _code_lines[i].split('=')[1].replace(' ','')
                        picked_var1= inputs = picked_var[picked_var.find('(')+ 1 : picked_var.rfind(')')]
                        for k in reversed(range(0,i)):
                            if "def" in _code_lines[k]:
                                s = _code_lines[k]
                                inputs = s[s.find('(')+ 1 : s.rfind(')')]
                                if findWholeWord(picked_var)(inputs):
                                    return True
                                if findWholeWord(picked_var1)(inputs):
                                    return True
                                
    return False

###########################################################################
def another_variable_assignment(_code_lines , _imps, _storage_variables):
    implementation_addresses=[]
    for var in _imps:
        for i in range(len(_code_lines)):
            if var in _code_lines[i]:
                if "=" in _code_lines[i]:
                    if "if" not in _code_lines[i]:
                        picked_var = _code_lines[i].split('=')[1].replace(' ','')
                        #print(picked_var)
                        #print(_storage_variables)
                        if picked_var in _storage_variables[0]:
                            implementation_addresses.append(picked_var)
                            #print(picked_var)
    return implementation_addresses

    #########################################################
def beacon_finder (_delegate_lines):
    for lines12 in _delegate_lines:
        if "ext_call.return" in lines12:
            return True
        else:
            return False


    #########################################################
        #########################################################   0x50338DFB3f9F324168b0c4817d53fEA51A0B66EC  This address

def delegate_parameters_check (_code_lines):
    for rrr in range(len(_code_lines)):
        if "payable:" in _code_lines[rrr]:
            for kkk in range(rrr,len(_code_lines)):
                if "delegate" in _code_lines[kkk]:
                    #print(_code_lines[kkk])
                    delegatedd= _code_lines[kkk]
                    input11 = delegatedd[delegatedd.find('delegate ')+ 9 : delegatedd.rfind(' with:')+1]
                    for ll in reversed(range(0,kkk)):
                            if "def" in _code_lines[ll]:
                                sl = _code_lines[ll]
                                #print(sl)
                                inputs12 = sl[sl.find('(')+ 1 : sl.rfind(')')]
                                #print(inputs12)
                                if len(inputs12) !=0:
                                    if findWholeWord(input11)(inputs12):
                                        return True
                                break
    
    return False    
# def ultraUpgrade ( _code_lines, _delegate_lines):
#     for lines12 in _delegate_lines:
#         picked_var1= lines12[lines12.find('delegate ')+ 1 : lines12.rfind(' with:')]
#         for i in range(len(_code_lines)):

#             for k in reversed(range(0,i)):



    #########################################################

    
f = open('Bytecodes.txt', 'r')
fp1= open('Final_upgradeable_proxies.txt', 'a')
fp2= open('Final_Non-upgradeable_proxies.txt', 'a')
fp3= open('Final_Errors.txt', 'a')
fp4= open('Final_beacon_proxies.txt', 'a')
fp5= open('Final_Skeptical_upgradeable_proxies.txt', 'a')
mm=0
line_number1=int(input("enter the last line number before failure: "))

for line in f:
    if line_number1 <= mm:
        mm+=1
        address = line.split(',')[0]
        code= line.split(',')[1].replace('\n','')
        bytecode = code.replace('0x' , '')
        result = decompilation(bytecode)
        lines = result.split('\n')
        delegated_lines = delegated_lines_in_fallback(lines)
        address_storage_variables = storage_variable(lines)
        imps = match_finder(address_storage_variables, delegated_lines)
        if beacon_finder(delegated_lines) :
            fp4.write(address + '\n')
            print("Hey Its Beacon")
        newElements = another_variable_assignment(lines , imps, address_storage_variables)
        for nn in range(len(newElements)):
            imps.append(newElements[nn])
        try:
            if assignment_checker (lines , imps):
                fp1.write(address + '\n')
                print("upgradeable")
            elif delegate_parameters_check (lines):
                fp5.write(address + '\n')
                print("upgradeable But CARE")
            else:
                fp2.write(address + '\n')
                print("NOT UPGRADEABLE")
        except:
            print("Error happend on " + address)
            fp3.write(address + '\n')
    else:
        mm+=1
    print(mm)
    
    
f.close()
fp1.close()
fp2.close()
fp3.close()
fp4.close()
fp5.close()