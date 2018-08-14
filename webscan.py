#!/usr/bin/env python

import time
import os
import subprocess
from pprint import pprint

from zapv2 import ZAPv2

print ('Starting ZAP ...')
subprocess.Popen(['C:/Windows/ZAP/zap.sh','-daemon'],stdout=open(os.devnull,'w'))
print ('Waiting for ZAP to load, 10 seconds ...')
time.sleep(10)

target = 'https://google-gruyere.appspot.com/495715196449258428882656550965763645231/'

zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

# do stuff
print ('Accessing target %s' % target)
# try have a unique enough session...
zap.urlopen(target)
# Give the sites tree a chance to get updated
time.sleep(2)

print ('Spidering target %s' % target)
zap.spider.scan(target)

# Give the Spider a chance to start
time.sleep(2)
while (int(zap.spider.status) < 100):
   print ('Spider progress %: ' + zap.spider.status)
time.sleep(5)

print ('Spider completed')
# Give the passive scanner a chance to finish
time.sleep(5)

print ('Scanning target %s' % target)
zap.ascan.scan(target)
while (int(zap.ascan.status) < 100):
   print ('Scan progress %: ' + zap.ascan.status)
time.sleep(5)

print ('Scan completed')

# Report the results

print ('Hosts: ' + ', '.join(zap.core.hosts))
print ('Alerts: ')
pprint (zap.core.alerts())

print ('Shutting down ZAP ...')
zap.core.shutdown
