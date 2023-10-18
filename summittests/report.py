import re
import sys
from typing import Dict, TextIO

import matplotlib.pyplot as plt
import numpy as np

FIELDRE = re.compile(r'INFO (.+) __main__ - ([0-9]+.[0-9]+) ([0-9]+.[0-9]+)')


def oneplot(host, times, filecount):
    """Plot a histogram of the times for one host"""
    print(f"{host} {filecount} files Mean:{np.mean(times):.2f} max:{np.max(times):.2f} "
          f"min: {np.min(times):.2f} std:{np.std(times):.2f}, var:{np.var(times):.2f} seconds")
    bins = np.arange(2, 40.0, 1)
    plt.clf()
    plt.hist(times, bins=bins)
    plt.title(f"{host} {filecount} files")
    plt.ylabel("Number of files")
    plt.xlabel("Time (seconds)")
    plt.axvline(x=7, color='r', label='requirement')

    plt.savefig(f"plots/{host}.png")
    pass


def plot(results):
    """Plot a histogram of the times for all hosts"""
    alltimes = []
    filecount = 0
    hosts = sorted(results.keys())
    for host in hosts:
        times_from_log = results[host]
        times = [t[2] for t in times_from_log]
        alltimes.append(times)
        oneplot(host, times, len(times))
        filecount += len(times)
    if len(results.keys()) > 1:
        oneplot("all", alltimes, filecount)


def load(host: str, fin: TextIO, results: Dict) -> Dict:
    """Load the times from one file"""
    times = []
    for line in fin:
        if 'Starting' in line:
            continue
        fields = FIELDRE.match(line)
        if not fields:
            print(f"Could not parse {line} for {host}", sys.stderr)
            continue
        time = [fields.group(1), float(fields.group(2)), float(fields.group(3))]
        times.append(time)
    results[host] = times
    return results


def process(files: list) -> Dict:
    """Process all the files make a dict of times"""
    results = {}
    name1 = re.compile(r'.*/*(lsstcam-dc[0,1][0-9])-.*')
    name2 = re.compile(r'(.+[0,1][0-9])-.')
    for f in files:
        match = name1.match(f)
        if match is None:
            match = name2.match(f)
        if match is None:
            print(f"Could not get host from {f}", sys.stderr)
            host = f.replace('.log', '')
        else:
            host = match.group(1)
        with open(f, 'r') as fin:
            load(host, fin, results)

    return results


if __name__ == '__main__':
    files = sys.argv[1:]
    results = process(files)
    plot(results)
