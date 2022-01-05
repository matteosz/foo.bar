import base64

with open('encrypted.txt','r') as f:
    message = f.read()

user = 'mattsuez01'

result = []
for i, c in enumerate(base64.b64decode(message)):
    result.append(chr(c ^ ord(user[i % len(user)])))

print ('Decrypted string: ' + ''.join(result))


