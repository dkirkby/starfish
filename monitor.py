import time
import argparse
import subprocess


def scan(iface, out, timeout):
    try:
        when = time.time()
        proc = subprocess.run(
            ['/sbin/iwlist', iface, 'scan'], stdout=subprocess.PIPE,
            timeout=timeout)
    except subprocess.TimeoutExpired as e:
        print(str(e))
        return out
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
                if len(essid) > 0:
                    entry = out.get(essid, [])
                    entry.append((when, quality))
                    out[essid] = entry
                quality = essid = None
    else:
        print('returncode =', proc.returncode)
    return out


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--ival', type=float, default=15,
        help='scan interval in seconds')
    parser.add_argument(
        '--save', type=str, default='scan.dat',
        help='name of file where scan results are saved')
    args = parser.parse_args()
    wlan0, wlan1 = {}, {}
    nscan = 0
    try:
        while True:
            nscan += 1
            timestamp = time.time()
            print('[{}] {:.3f}'.format(nscan, timestamp))
            scan('wlan0', wlan0, 0.4 * args.ival)
            scan('wlan1', wlan1, 0.4 * args.ival)
            delay = args.ival - time.time() + timestamp
            if delay > 0:
                time.sleep(delay)
    except KeyboardInterrupt:
        print('saving')

    with open(args.save, 'w') as f:
        for iface, d in ('wlan0', wlan0) , ('wlan1', wlan1):
            for essid in d:
                print('# {} "{}"'.format(iface, essid), file=f)
                for t, q in d[essid]:
                    print('{:.3f} {}'.format(t, q), file=f)

if __name__ == '__main__':
    main()
