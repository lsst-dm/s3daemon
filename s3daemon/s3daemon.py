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
import os
import time

import aiobotocore.session
import botocore

config = botocore.config.Config(
    max_pool_connections=25,
    tcp_keepalive=True,
    s3=dict(
        payload_signing_enabled=False,
        addressing_style="path",
    ),
)

PORT = 15555
endpoint_url = os.environ["S3_ENDPOINT_URL"]

async def handle_client(client, reader):
    """Handle a client connection to the server socket.

    Parameters
    ----------
    client : `S3`
        The S3 client to use to talk to the server.
    reader : `asyncio.StreamReader`
        A stream connected to the socket to read the filename/destination pair.
    """
    filename, dest = (await reader.readline()).decode("UTF-8").rstrip().split(" ")
    start = time.time()
    # ignore the alias
    _, bucket, key = dest.split("/", maxsplit=2)
    with open(filename, "rb") as f:
        await client.put_object(Body=f, Bucket=bucket, Key=key)
    print(start, time.time() - start, "sec")


async def main():
    """Start the server."""
    session = aiobotocore.session.get_session()
    async with session.create_client("s3", endpoint_url=endpoint_url, config=config) as client:
        async def client_cb(reader, writer):
            await handle_client(client, reader)

        server = await asyncio.start_server(client_cb, "localhost", PORT)
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
