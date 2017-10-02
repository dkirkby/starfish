import time
import argparse
import subprocess


def scan(iface, timeout):
    try:
        proc = subprocess.run(
            ['/sbin/iwlist', iface, 'scan'], stdout=subprocess.PIPE,
            timeout=timeout)
    except subprocess.TimeoutExpired as e:
        print(str(e))
        return
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
                print('{0} {1}'.format(quality, essid))
                quality = essid = None
    else:
        print('returncode =', proc.returncode)
    return


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--ival', type=float, default=60,
        help='scan interval in seconds')
    parser.add_argument(
        '--save', type=str, default='scan.dat',
        help='name of file where scan results are saved')
    args = parser.parse_args()
    out = open(args.save, 'a')
    try:
        while True:
            timestamp = time.time()
            print('===>', timestamp)
            scan('wlan0', 0.4 * args.ival)
            #print(output)
            #print(output, file=out)
            #out.flush()
            delay = args.ival - time.time() + timestamp
            if delay > 0:
                time.sleep(delay)
    except KeyboardInterrupt:
        print('bye')
    out.close()

if __name__ == '__main__':
    main()
