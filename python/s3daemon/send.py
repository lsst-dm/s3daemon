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

import os
import socket
import sys

port = int(os.environ.get("PORT", 15555))


def send(filename, dest):
    """Send a filename/destination pair to the server.

    Parameters
    ----------
    filename : `str`
        Name of the file to be uploaded.  May not contain spaces.
    dest : `str`
        Destination in ``{alias}/{bucket}/{key}`` format.
        The key may contain slashes.
    """
    global port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("localhost", port))
        sock.sendall(bytes(f"{filename} {dest}\n", "UTF-8"))
        received = str(sock.recv(4096), "utf-8")
        sock.close()
        if received.startswith("Success"):
            sys.exit(0)
        else:
            print(received, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    send(sys.argv[1], sys.argv[2])
