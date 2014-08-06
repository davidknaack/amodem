from amodem import stream
import subprocess as sp

script = r"""
import sys
import time
import os

while True:
    time.sleep(0.1)
    sys.stdout.write(b'\x00' * 6400)
    sys.stderr.write('.')
"""


def test_read():
    p = sp.Popen(args=['python', '-'], stdin=sp.PIPE, stdout=sp.PIPE)
    p.stdin.write(script)
    p.stdin.close()
    f = stream.Reader(p.stdout)

    result = zip(range(10), f)
    p.kill()

    j = 0
    for i, buf in result:
        assert i == j
        assert len(buf) == f.SAMPLES
        j += 1

    try:
        for buf in f:
            pass
    except IOError as e:
        assert str(e) == 'timeout'