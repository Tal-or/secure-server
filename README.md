# secure-server

Description:
Secure server application developed in modern Python3 language
Server is listening on the loopback interface on port 25000.

## Vulnerabilities Protection:
1. Encryption: Communication with the server via encrypted SSL connection using TLSv1.3.
2. Authentication: Server auth using Basic with user/password credentials.
3. Code Injection Protection: Serialization/Deserialization done with JSON structures only, which protects against insecure deserialization
4. Exception Handling: Handling exception mechanism in case of invalid data being sent from the user.

## Security Flaws:
1. In order to allow maximum flexibility in terms of python commands execution on server side,
   we're using eval which is very dangerous to use.
   For mitigation purposes the command length limit is 0.5K bytes long and there are blacklisted words and characters such as 'sudo' and backslashes
   Also, connection to server is done using credentials which are known only for valid users.  

## Usage Instructions:
1. In the secure-server project directory go to src directory
2. Run the server using: ./main.py or python3 main.py
