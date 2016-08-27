# This is not part of the actual server

from hashlib import sha256
password = (input() + '2016')[::-1] + 'mysalt'
md = sha256(password.encode())
print(md.hexdigest())
