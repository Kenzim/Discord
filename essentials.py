import os
import errno
import socket
from contextlib import asynccontextmanager
import asyncio


def ensure_file_existence(path):
    try:
        open(path, 'r')
    except FileNotFoundError:
        try:
            if os.path.dirname(path) != '':
                os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
        open(path, 'w+')
    else:
        pass


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False

    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    return True


@asynccontextmanager
async def run_in_background(routine):
    task = asyncio.create_task(routine)
    try:
        yield task
    finally:
        await task
