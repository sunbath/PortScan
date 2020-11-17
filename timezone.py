#!/usr/bin/env python3
import socket
import subprocess
import sys

from datetime import datetime,timezone
from tabulate import tabulate


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

print(aslocaltimestr(datetime.utcnow()))