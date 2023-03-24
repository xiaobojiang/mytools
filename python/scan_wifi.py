import subprocess
from tabulate import tabulate
import re
import sys, getopt

'''
This is a tool can be used in macos(only).
It can help you scan all your nearby ssids, and show their RSSI and channels
'''


def get_wifi_info(ssid_filter=None):
    cmd = ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s']
    output = subprocess.run(cmd,check=True, capture_output=True).stdout.decode('utf-8').split('\n')
    ssid_list = []
    for line in output:
        if 'SSID' not in line:
            line = line.lstrip()
            #split based on two or more spaces
            items = re.split(r'\s{2,}',line)
            if len(items) > 4:
                ssid = items[0]
                rssi = items[1]
                channel = items[2]
                if not ssid_filter:
                    ssid_list.append([ssid, '{}'.format(channel), rssi])
                else:
                    if ssid_filter.lower() in ssid.lower():
                        ssid_list.append([ssid, '{}'.format(channel), rssi])
    return ssid_list


def main(argv):
    opts, args = getopt.getopt(argv,"hf:",["filter="])
    ssid_filter = None
    for opt, arg in opts:
        if opt == '-h':
            print ('scan_wifi.py -f <ssid filter key word>')
            sys.exit()
        elif opt in ("-f", "--filter"):
            ssid_filter = arg


    print(tabulate((get_wifi_info(ssid_filter)), headers=['ssid','channels', 'rssi']))


if __name__ == '__main__':
    main(sys.argv[1:])

