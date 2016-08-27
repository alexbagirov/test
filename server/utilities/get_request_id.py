import time
from hashlib import sha256

code = input()
st = str(time.time()).replace('.', '') + code

md = sha256(st.encode())
print(md.hexdigest())
