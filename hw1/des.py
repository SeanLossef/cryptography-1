# Changes permutation of data based on permutation scheme
def permute(data,perm):
	output = list("0"*len(perm))
	for i in range(len(output)):
		output[i] = data[perm[i]-1]
	return "".join(output)

# Returns an int based on a binary string
def parseBin(data):
	if (data == "00"):
		return 0
	if (data == "01"):
		return 1
	if (data == "10"):
		return 2
	if (data == "11"):
		return 3
	return 0

# Returns substitution given 4 bit input and sub box id
def substitute(data,box):
	s0 = [["01","00","11","10"],
			["11","10","01","00"],
			["00","10","01","11"],
			["11","01","11","10"]]
	s1 = [["00","01","10","11"],
			["10","00","01","11"],
			["11","00","01","00"],
			["10","01","00","11"]]

	col = parseBin(data[1] + data[2])
	row = parseBin(data[0] + data[3])

	if (box == 0):
		return s0[row][col]
	return s1[row][col]

# Left shifts given data by 1 position
def leftShift(data):
	return data[1:] + data[:1];

def xor(a,b):
	output = list("0"*len(a))
	for i in range(len(a)):
		if (a[i] == b[i]):
			output[i] = "0"
		else:
			output[i] = "1"
	return "".join(output)

# Returns key[n+1] given key[n]
def generateKeys(k):
	k = permute(k, [3,5,2,7,4,10,1,9,8,6])
	l = leftShift(k[:5])
	r = leftShift(k[5:])
	k1 = permute(l+r, [6,3,7,4,8,5,10,9])
	l = leftShift(l)
	r = leftShift(r)
	k2 = permute(l+r, [6,3,7,4,8,5,10,9])
	return [k1,k2]

def fFunction(data,key):
	data = permute(data, [4,1,2,3,2,3,4,1])
	data = xor(data,key)

	l = substitute(data[:4], 0)
	r = substitute(data[4:], 1)

	return permute(l+r, [2,4,3,1])

def encrypt(p,k):
	keys = generateKeys(k)

	# Initial Permutation
	p = permute(p, [2,6,3,1,4,8,5,7])

	# Round 1
	l = p[:4]
	r = p[4:]
	l = xor(fFunction(r, keys[0]), l)
	p = r + l

	# Round 2
	l = p[:4]
	r = p[4:]
	l = xor(fFunction(r, keys[1]), l)
	p = l + r

	# Inverse Initial Permutation
	return permute(p, [4,1,3,5,7,2,8,6])

def decrypt(c,k):
	keys = generateKeys(k)

	# Initial Permutation
	c = permute(c, [2,6,3,1,4,8,5,7])

	# Round 1
	l = c[:4]
	r = c[4:]
	l = xor(fFunction(r, keys[1]), l)
	c = r + l

	# Round 2
	l = c[:4]
	r = c[4:]
	l = xor(fFunction(r, keys[0]), l)
	c = l + r

	# Inverse Initial Permutation
	return permute(c, [4,1,3,5,7,2,8,6])

def main():
	##### CHANGE THESE PARAMS TO CHANGE PLAINTEXT AND KEY #####
	p = "00101000"
	k = "1100011110"

	print "Plain Text: " + p
	c = encrypt(p,k)
	print "Cipher Text: " + c

	p = decrypt(c,k)
	print "Decrypted Cipher Text: " + p

  
if __name__== "__main__":
	main()