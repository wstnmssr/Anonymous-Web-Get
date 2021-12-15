# Anonymous-Web-Get
A small project to download files via stepping stones, retaining anonymity


The reader is the interface to the stepping stone chain. The reader takes one 
command line argument, the URL of the file to retrieve.  In addition, the reader will read a local 
configuration file that contains the IP addresses and port numbers of all the available stepping-
stones. Note that having this file on your computer does not compromise the anonymity of the 
chain: one would still have to prove that your computer was used to retrieve a particular 
document, in other words having knowledge of the stepping stones does not imply you used them. 
 
The stepping-stone: The SS acts both as a server and a client. There is one SS running on each 
machine. When the SS starts it prints out the hostname and port it is listening to, and then waits 
for connections.  Once a connection arrives, the SS reads the list of remaining SS's in the request 
and if the list is not empty, strips itself from the list and forwards the request to a randomly 
chosen SS in the list. If the SS is the last entry on the list, it extracts the URL of the desired 
document, executes the system() command to issue a wget to retrieve the document, and then 
forwards the document back to the previous SS. Once the document is forwarded, the SS erases 
the local copy of the file and tears down the connection
