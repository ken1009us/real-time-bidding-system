# IS496: Computer Networks (Spring 2023) Mini Project - Real-time Bidding System


Team member and NetID

- Member 1: Ken Wu (shwu2) 
- Member 2: Thomas Huang (yenshuo2) 
- Member 3: Jack Chuang (yzc2)


## Background

Our project's objective is to create a real-time bidding system that will enable buyers and sellers to make network-based real-time bids on goods. All parties engaged in the bidding process will have access to a dependable, low-latency communication platform via the system. Buyers and sellers searching for a quick and safe way to engage in auctions are the application's target users. Our program will enable customers to bid on numerous items simultaneously in addition to allowing merchants to list their products and launch the bidding. The application will make the bidding process more efficient, provide up-to-date information, and maintain data integrity. This is crucial in high-stakes auctions since every second counts.

## Preparation

```shell
import socket
import threading
import sys, argparse, subprocess, os
```

## Execution

Please connect to your student machines first.

```shell
$ ssh YOUR_NET_ID@student00.ischool.illinois.edu

$ ssh YOUR_TEAM_MEMBER_NET_ID@student01.ischool.illinois.edu
```

The server is running on student00, the client should be tested on student student01/student02/student03.



### Real-time Bidding System

Our implementation includes both the client and server sides of a bidding system that transfers data over TCP. The client is in charge of choosing the command.  

Bidding System client that takes in:

- The hostname of the server (argument 1).
- The port number on the server (argument 2).
- The user name of the client (argument 3).

```shell
YOUR_NET_ID@is-student00:~$ /YOUR_PATH/python3 client.py -hn [HOST_NAME] -p [PORT_NUMBER] -un [USER_NAME]
```

Bidding System server that takes in:

- The port number on the server (argument 1).
- The port number on the server (argument 2).

Run the socket server program.

```shell
YOUR_NET_ID@is-student00:~$ /YOUR_PATH/python3 server.py -hn [HOST_NAME] -p [PORT_NUMBER]
```

Then the terminal will show the messages below:

```
[INFO] Waiting for connection on port 9999...

```

Run the socket client program.

```shell
YOUR_TEAM_MEMBER_NET_ID@is-student01:~$ /YOUR_PATH/python3 client.py -hn [SERVER_HOST_NAME] -p [PORT_NUMBER] -un [USER_NAME]
```

Then the server terminal will show the messages based on New User or Existing User:

New User:

```shell
Enter user's password:
```

Existing User:

```shell
Register user's password: 
```

After connection established, client sends command to server; then server responds accordingly.


####BID: 
This command allows the user to place a bid on a specific auction item. Once enter the command, server will send the biddable items to client. The user would provide the item name and the amount they wish to bid, and the server would validate the bid and update the result accordingly. If the bid is successful, the server would respond with a success message. If the bid is invalid or unsuccessful, the server would respond with an error message.

####AUCT: 
This command allows the user to create a new auction item. The user would be asked to provide details about the item, such as item name and starting price. (Currently, the auction time by default is set to 180 seconds for testing purpose)


####GETALL: 
This command allows the user to retrieve information about all the auction items currently in the database. Each items has the information of current price, current owner(highest bid), and whether the item is biddable. 

####EX: 
This command allows the user to exit or quit the bidding interface. On receiving the operation, the server closes the socket descriptor for the client. This ensures proper termination of the communication and releases the resources used by the client and server.


If client quits, server return to 

```
"[INFO] Waiting for connection on port 9999..."
```
