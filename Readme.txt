

- Secure Netcat

- sncstart.py 
Snc class has been created which internally creates server/client based on the inputs.

- snc
snc contains only the main function which will call the snc class's start function.

- sncserver.py
SncServer class 

- sncclient.py
SncClient class

- utility.py
Utility class containing helper functions

- aeshelper.py
AesHelper class containing encrypt and decrypt functions.

Order of execution.
The server by default runs on localhost. For other interface address, kindly edit SncServer class's __init__ function.
For Server - ./snc -l --key [16characters string] port < inputfile > outputfile
For Client - ./snc --key [16 character string] host port < inputfile > outputfile

The application has been tested with a file containing 20,700,3300 lines.

