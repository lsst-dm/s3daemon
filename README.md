s3daemon
========

Client/server for pushing objects to S3 storage.

The server is intended to be able to maintain long-lived TCP connections, avoiding both authentication delays and TCP slow start on long bandwidth-delay product network segments.
Enabling multiple simultaneous parallel transfers also is intended to maximize usage of the network.

The client is intended to allow "fire-and-forget" submissions of transfer requests by file-writing code.

Prerequisites
-------------

As specified in ``requirements.txt``, the ``aiobotocore`` Python package must be available for the server.
This can be installed into a system Python with ``pip``, or it can be installed into a Conda environment that is activated when the server is started.
``micromamba`` (https://mamba.readthedocs.io/en/latest/micromamba-installation.html) or ``mambaforge`` (https://mamba.readthedocs.io/en/latest/mamba-installation.html) are the recommended ways of obtaining a Conda Python.

The client requires only a vanilla Python 3.x.

TCP port 15555 on ``localhost`` is used for client/server communication.
This port number is currently hard-coded but could be made configurable if needed.

s3daemon.py
-----------

``s3daemon.py`` is the server that maintains a connection pool to the object store and mediates the transmissions.

It is configured via three environment variables:

- ``S3_ENDPOINT_URL``: The URL to the object store endpoint (e.g. ``https://s3dfrgw.slac.stanford.edu``).
- ``AWS_ACCESS_KEY_ID``: The access key credential for the object store.
- ``AWS_SECRET_ACCESS_KEY``: The secret key credential for the object store.

Note that having the credentials in the environment may allow them to be visible to other users of the host on which the server runs.

The server accepts client connections, receives filename/destination pairs, opens the file, and uses ``put_object`` to send it to the object store.
Note that the file must be readable by the UID that the server runs under.
A connection pool (currently hard-coded to 25 connections, but can be made configurable) and the ``tcp_keepalive`` parameter are used to minimize connection overhead.
Python ``asyncio`` is used to allow potential interleaving of multiple transmissions at the same time.

Currently, the start time (in Unix seconds since the epoch) and total send time for each object are written to standard output for performance monitoring.

send.py
-------

``send.py`` is the client.
It takes two command line parameters: the filename to be transmitted and the object store destination in ``{alias}/{bucket}/{key}`` format.
The filename must not contain spaces.
The alias is present for compatibility with the ``mc`` client and is ignored.
The key may contain slashes.

If a successful result is returned from the server, there is no output, and the exit status is 0.
Otherwise, the error will be output to standard error, and the process exit status will be 1.
