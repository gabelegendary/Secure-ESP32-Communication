# CLIENT REQUIREMENTS

[ReqId:01v01] The client shall have a user interface function to initialize the ESP32 connection.

[ReqId:02v01] The client shall provide a function to establish a secure session with the ESP32 server.

[ReqId:03v01] The client shall provide a function to terminate the established session.

[ReqId:04v01] The client shall feature a user interface function to retrieve the temperature of the ESP32 core.

[ReqId:05v01] The client shall include a user interface function to toggle the LED connected to the ESP32.

[ReqId:06v01] The client shall log the state, status, and results of the requests made during a session.

[ReqId:07v01] The client shall provide a function to clear the log.

[ReqId:08v01] The client shall dynamically disable the "Get Temperature" and "Toggle LED" buttons if there is no active session.

[ReqId:09v01] The client shall change the label of the session button to "Establish Session" if there is no session and to "Close Session" if there is an active session.

## SERVER REQUIREMENTS

[ReqId:01v01] The server shall have a user interface function to initialize the communication with the connected ESP32.

[ReqId:02v01] The server shall support the initiation of a secure session with the client.

[ReqId:03v01] The server shall handle the termination of the active session.

[ReqId:04v01] All transactions between the client and server shall be protected using HMAC-SHA256.
The HMAC key used for protection shall be: Fj2-;wu3Ur=ARl2!Tqi6IuKM3nG]8z1+.

[ReqId:05v01] RSA-2048 shall be used for secure key exchange (e.g., AES-256 key and initialization vector).

[ReqId:06v01] The server shall be designed to handle only one session at a time.

[ReqId:07v01] A session between the client and the server shall expire after 1 minute of inactivity.
