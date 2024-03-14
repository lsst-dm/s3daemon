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
import time

import aiobotocore.session
import botocore

port = int(os.environ.get("PORT", 15555))

endpoint_url = os.environ["S3_ENDPOINT_URL"]
access_key = os.environ["AWS_ACCESS_KEY_ID"]
secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
max_connections = int(os.environ.get("MAX_CONNECTIONS", 25))

config = botocore.config.Config(
    max_pool_connections=max_connections,
    tcp_keepalive=True,
    s3=dict(
        payload_signing_enabled=False,
        addressing_style="path",
    ),
)

pylog_longLogFmt = "{levelname} {asctime} {name} - {message}"
log_file = os.environ.get("S3DAEMON_LOG")
if log_file is not None:
    logging.basicConfig(filename=log_file, format=pylog_longLogFmt, style="{")
else:
    logging.basicConfig(format=pylog_longLogFmt, style="{")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


async def handle_client(client, reader, writer):
    """Handle a client connection to the server socket.

    Parameters
    ----------
    client : `S3`
        The S3 client to use to talk to the server.
    reader : `asyncio.StreamReader`
        A stream connected to the socket to read the filename/destination pair.
    writer : `asyncio.StreamWriter`
        A stream connected to the socket to write back status information.
    """
    filename, dest = (await reader.readline()).decode("UTF-8").rstrip().split(" ")
    start = time.time()
    # ignore the alias
    _, bucket, key = dest.split("/", maxsplit=2)
    result = "Success"
    with open(filename, "rb") as f:
        try:
            await client.put_object(Body=f, Bucket=bucket, Key=key)
            writer.write(b"Success")
        except Exception as e:
            writer.write(bytes(repr(e), "UTF-8"))
            result = f"Exception {e}"
    log.info("%f %f sec: %s", start, time.time() - start, result)


async def main():
    """Run the daemon server."""
    global access_key, secret_key, endpoint_url, config, port

    """Start the server."""
    session = aiobotocore.session.get_session()
    async with session.create_client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url,
        config=config,
    ) as client:

        async def client_cb(reader, writer):
            await handle_client(client, reader, writer)

        server = await asyncio.start_server(client_cb, "localhost", port)
        log.info("Starting server")
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
