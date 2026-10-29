# What is the TCP 3-Way Handshake and Why Backend Engineers should understand it

> Source: `What is the TCP 3-Way Handshake and Why Backend Engineers should understand it.txt` · Transcript 38 of 43

## 📝 Description
Explains the **TCP three-way handshake**: why it exists (synchronizing sequence numbers) and why backend engineers should care about its cost.

## ⚠️ Problem
Before data is sent, TCP must be sure that packets can be acknowledged (reliability) and ordered (sequence numbers), and both sides must agree where each other's sequence starts.

## ✅ Solution
A three-packet exchange: **SYN**, **SYN-ACK**, **ACK**.

## 🔍 Explanation
1. **Acknowledgments:** each packet is acknowledged. A missing ACK triggers retransmission.
2. **Sequence numbers:** identify and order packets (out-of-order arrival is fixed by reordering).
3. **Synchronization:** each side picks a **random** starting sequence (random helps against replay and SYN attacks) and tells the other.
4. **Step 1, SYN:** client → server, "my sequence is 700".
5. **Step 2, SYN-ACK:** server → client, "my sequence is 200, and I got your 700, so I expect 701". The server's SYN and ACK are combined in one packet, so the handshake takes three packets, not four.
6. **Step 3, ACK:** client → server, "I got your 200, expecting 201".
7. **Then data:** the GET starts at 701. The ACK for it is 701 + the request size (a 10-byte request → 711).
8. **ACK ≠ response:** an ACK only says "received". It isn't the application response.
9. **Cost:** three packets to open and about two more to close, which is why QUIC/UDP designs avoid it.

## 💻 Relevant Code
Watch a handshake with tcpdump:
```bash
sudo tcpdump -i any -n 'tcp port 80 and (tcp[tcpflags] & (tcp-syn|tcp-ack) != 0)' -c 6
# Flags [S]  -> SYN
# Flags [S.] -> SYN-ACK
# Flags [.]  -> ACK
```

## 🤖 Claude's Notes
- The "ghost byte": SYN consumes one sequence number, which is why 700 → 701.
- Connection reuse (keep-alive, pools) amortizes this cost across many requests.

## 🎯 Key Takeaways
- Handshake = synchronize sequence numbers.
- It costs a round trip before any data is sent.
- Reuse connections to avoid paying it repeatedly.

## ❓ Questions
1. Why are the SYN and ACK from the server in one packet?
2. Why are initial sequence numbers random?
3. What does ACK 701 mean?

## 🔁 Follow-up Questions
1. How does TCP close a connection (FIN/ACK)?
2. How does QUIC avoid this handshake?

## 🤔 Questions to Think About
- How many handshakes does your app perform per user action?
- What do you lose if you skip a connection pool?
