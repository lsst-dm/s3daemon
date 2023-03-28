s3daemon
========

Client/server for pushing objects to S3 storage.

The server is intended to be able to maintain long-lived TCP connections, avoiding both authentication delays and TCP slow start on long bandwidth-delay product network segments.
Enabling multiple simultaneous parallel transfers also is intended to maximize usage of the network.

The client is intended to allow "fire-and-forget" submissions of transfer requests by file-writing code.
