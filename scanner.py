import time
import argparse
import subprocess


def scan(iface, essids, timeout=5):
    qualities = [0] * len(essids)
    try:
        when = time.time()
        proc = subprocess.run(
            ['/sbin/iwlist', iface, 'scan'], stdout=subprocess.PIPE,
            timeout=timeout)
    except subprocess.TimeoutExpired as e:
        return qualities
    if proc.returncode == 0:
        lines = proc.stdout.decode().split('\n')
        quality = essid = None
        for line in lines:
            line = line.strip()
            if line.startswith('Cell'):
                quality = essid = None
            elif line.startswith('Quality='):
                delim = line.index('/')
                quality = int(line[8:delim])
            elif line.startswith('ESSID:"'):
                essid = line[7:-1]
            if quality is not None and essid is not None:
                # Process a (essid, quality) pair.
                try:
                    idx = essids.index(essid)
                    qualities[idx] = quality
                except ValueError:
                    pass
                quality = essid = None
    else:
        print('returncode =', proc.returncode)
    return qualities


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--iface', type=str, default='wlan1',
        help='wireless interface to scan')
    parser.add_argument(
        '--essid1', type=str, default='Carols Guest Network',
        help='first network to scan for')
    parser.add_argument(
        '--essid2', type=str, default='carols guest network',
        help='second network to scan for')
    args = parser.parse_args()

    essids = [args.essid1, args.essid2]
    try:
        while True:
            q1, q2 = scan(args.iface, essids)
            qmin = min(q1, q2)
            qmax = max(q1, q2)
            display = ' ' * qmin
            pad = ' ' * abs(q1 - q2)
            if q1 == q2:
                display += '*'
            elif q1 < q2:
                display += '1' + pad + '2'
            else:
                display += '2' + pad + '1'
            display += (' ' * (72 - len(display)))
            display += '<< {:02d} {:02d}'.format(qmin, qmax)
            print(display)
    except KeyboardInterrupt:
        print('bye')


if __name__ == '__main__':
    main()
