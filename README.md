# Secure-ESP32-Communication
A secure Python client communicates with an ESP32 server via serial connection. Utilising HMAC-SHA256, AES-256, and RSA-2048, it ensures encrypted, authenticated, and time-sensitive IoT transactions. Features Tkinter GUI, LED control, and session management for enhanced security.


1. The server should have a get temperature function and also an establish and close the session function
2. Protocol for initialisation, sending and receiving.
3. I need protocol in both the client and the server.
4. In the server you should have a directory for the functionalities, get temperature, establish and close session, toggle led
5. Main should implement the functionalities of the server.
6. In the client we need directory for the functionalities, one for the protocol and one for the gui
7. initialise serial in the main
8. The server and the client need to communicate. The client sends the data, the server receives it and sends it back to the client.
