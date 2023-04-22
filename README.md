# Real-time Bidding System

## Author: Ken Wu, Jack Chuang, Thomas Huang

1. High-level idea and key challenges: Our project is to develop a real-time bidding system, where buyers and sellers can bid on items in real-time over the network. The key challenge is to provide a reliable, low-latency communication platform for all parties involved in the bidding process. This includes handling a large number of simultaneous connections, ensuring data integrity, and minimizing the response time.

2. Applying Socket programming using UDP and TCP: We plan to use Socket programming to develop the key networking functions of the application. We will use UDP for real-time updates and notifications to quickly inform buyers and sellers of the latest bids and prices. We will use TCP for secure and reliable data transfer during the bidding process, ensuring that all bids are accurately received and recorded. By using both protocols, we can balance the need for speed and reliability.

3. External sources: We will use a starter code to build the basic infrastructure of the system, including the user interface and database connectivity. We will also use a third party authentication service to ensure secure user login and session management. However, our group's contribution will be developing the networking functions using Socket programming.

### Installation
---
Use the package manager pip to install some modules.

```shell
pip install -r requirements.txt
```

### Execution
---
Run the application with:


### Possible improvements
---


