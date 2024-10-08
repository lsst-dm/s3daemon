# This file is part of s3daemon.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import os
import socket
import time

import aiobotocore.session
import botocore

max_connections = int(os.environ.get("S3DAEMON_MAX_CONNECTIONS", 25))
connect_timeout = float(os.environ.get("S3DAEMON_CONNECT_TIMEOUT", 5.0))
max_retries = int(os.environ.get("S3DAEMON_MAX_RETRIES", 2))
max_clients = int(os.environ.get("S3DAEMON_MAX_CLIENTS", 25))

config = botocore.config.Config(
    max_pool_connections=max_connections,
    tcp_keepalive=True,
    connect_timeout=connect_timeout,
    s3=dict(
        payload_signing_enabled=False,
        addressing_style="path",
    ),
    retries=dict(
        total_max_attempts=max_retries,
        mode="adaptive",
    ),
    disable_request_compression=True,
)

host = os.environ.get("S3DAEMON_HOST", "localhost")
port = int(os.environ.get("S3DAEMON_PORT", 15555))
endpoint_url = os.environ["S3_ENDPOINT_URL"]
access_key = os.environ["AWS_ACCESS_KEY_ID"]
secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]

pylog_longLogFmt = "{levelname} {asctime} {name} - {message}"
if "S3DAEMON_LOG" in os.environ:
    logging.basicConfig(filename=os.environ["S3DAEMON_LOG"], format=pylog_longLogFmt, style="{")
else:
    logging.basicConfig(format=pylog_longLogFmt, style="{")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


async def handle_client(client, conn):
    """Handle a client connection to the server socket.

    Parameters
    ----------
    client : `S3`
        The S3 client to use to talk to the server.
    conn : `socket.Socket`
        The socket connected to the client.
    """
    filename, dest = conn.recv(4096).decode("UTF-8").rstrip().split(" ")
    start = time.time()
    # ignore the alias
    _, bucket, key = dest.split("/", maxsplit=2)
    try:
        with open(filename, "rb") as f:
            await client.put_object(Body=f, Bucket=bucket, Key=key)
            conn.send(b"Success")
            log.info("%f %f sec - %s", start, time.time() - start, key)
    except Exception as e:
        conn.send(bytes(repr(e), "UTF-8"))
        log.exception("%f %f sec - %s", start, time.time() - start, key)
    conn.close()


async def go():
    """Start the server."""
    session = aiobotocore.session.get_session()
    async with session.create_client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url,
        config=config,
    ) as client:
        sem = asyncio.Semaphore(max_clients)
        background_tasks = set()
        log.info("Starting server")
        with socket.create_server((host, port)) as s:
            # We don't want to block in accept(); we need to run other tasks.
            s.setblocking(False)
            while True:
                # Do not allow more accepts if we're already handling the
                # maximum number of clients.
                await sem.acquire()
                while True:
                    try:
                        conn, _ = s.accept()
                        break
                    except (TimeoutError, BlockingIOError):
                        # Allow other tasks to run.
                        await asyncio.sleep(0)
                task = asyncio.create_task(handle_client(client, conn))
                # Add to set to avoid premature cleanup.
                background_tasks.add(task)
                # Release semaphore when task is handled.
                task.add_done_callback(lambda _: sem.release())
                # Remove from set when finished.
                task.add_done_callback(background_tasks.discard)


def main():
    """CLI script entry point."""
    asyncio.run(go())


if __name__ == "__main__":
    main()
