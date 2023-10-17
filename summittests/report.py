import numpy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import re

from typing import List, Dict, TextIO

FIELDRE = re.compile(r'INFO (.+) __main__ - ([0-9]+.[0-9]+) ([0-9]+.[0-9]+)')


def oneplot(host, times):
    print(f"{host} {len(times)} files Mean:{np.mean(times):.2f} max:{np.max(times):.2f} "
          f"min: {np.min(times):.2f} std:{np.std(times):.2f}, var:{np.var(times):.2f} seconds")
    bins = np.arange(3, 20.0, 1)
    plt.hist(times, bins=bins)
    plt.title(f"{host} histogram")
    plt.savefig(f"plots/{host}.png")
    pass


def plot(results):
    alltimes = []
    for host, timesall in results.items():
         times = [float(t[2]) for t in timesall]
         alltimes.append(times)
         oneplot(host, times)
    oneplot("all", alltimes)


def load(host: str, fin: TextIO, results: Dict) -> Dict:
    times = []
    for line in fin:
        if 'Starting' in line:
            continue
        fields = FIELDRE.match(line)
        if not fields:
            print (f"Could not parse {line} for {host}", sys.stderr)
            continue
        time = [fields.group(1), fields.group(2), fields.group(3)]
        times.append(time)
    results[host] = times
    return results

def process(files: list) -> Dict:
    results = {}
    for f in files:
        name = re.compile(r'.*/(lsstcam-dc[0,1][0-9])-.*')
        match = name.match(f)
        if not match:
            print (f"Could not get host from {f}", sys.stderr)
            exit
        host = match.groups()[0]
        print (host)
        with open(f,'r') as fin:
            load(host, fin, results)

    return results

if __name__ == '__main__':
    files = sys.argv[1:]
    results = process(files)
    plot(results)