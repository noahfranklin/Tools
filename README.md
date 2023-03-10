# Tools

JWT Token Test 

The above code is designed to perform the following test cases for JWT token vulnerability:

    Extract the JWT token from the response of the given URL.
    Generate a set of random strings of the same length as the signature.
    Try each random string as the new signature and submit the modified JWT token to the URL.
    If the modified JWT token is accepted by the application, report that a vulnerability has been found and print the random string used as the new signature.
    If no vulnerability is found using the random strings as the signature, use hashcat to brute force the signature using the specified dictionary file.
    If the signature is successfully cracked using hashcat, report that a vulnerability has been found and print the cracked signature.
    If no vulnerability is found using either method, report that no vulnerability was found.
