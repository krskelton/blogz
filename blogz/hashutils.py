import hashlib

#this takes the users password and stores it as a hash in the database
def make_pw_hash(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

#verifies the users password when they come to login
def check_pw_hash(password, hash):
	if make_pw_hash(password) == hash:
		return True
	return False