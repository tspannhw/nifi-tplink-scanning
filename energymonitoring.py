from pyHS100 import Discover
import json
import datetime
import os
import os.path
import socket
import time
import uuid
from time import gmtime, strftime
import psutil
import requests

# Get MAC address of a local interfaces
def psutil_iface(iface):
    # type: (str) -> Optional[str]
    import psutil
    nics = psutil.net_if_addrs()
    if iface in nics:
        nic = nics[iface]
        for i in nic:
            if i.family == psutil.AF_LINK:
                return i.address

headers = {'content-type': 'application/json'}


for dev in Discover.discover().values():
        now = datetime.datetime.now()
        row = {}
        year = now.year
        month = now.month
        start = time.time()
        sysinfo = dev.get_sysinfo()
        uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S", gmtime()), uuid.uuid4())

        for k, v in dev.get_emeter_realtime().items():
            row["%s" % k] = v

        for k, v in sysinfo.items():
            row["%s" % k] = v

        emeterdaily = dev.get_emeter_daily(year=year, month=month)
        for k, v in emeterdaily.items():
            row["day%s" % k] = v

        hwinfo = dev.hw_info

        for k, v in hwinfo.items():
            row["%s" % k] = v

        timezone = dev.timezone

        for k, v in timezone.items():
            row["%s" % k] = v

        emetermonthly = dev.get_emeter_monthly(year=year)

        for k, v in emetermonthly.items():
            row["month%s" % k] = v

        row['host'] = dev.host
        row['current_consumption'] = dev.current_consumption()
        row['alias'] = dev.alias
        row['devicetime'] = dev.time.strftime('%m/%d/%Y %H:%M:%S')
        row['ledon'] = dev.led
        end = time.time()
        row['end'] = '{0}'.format(str(end))
        row['te'] = '{0}'.format(str(end - start))
        row['systemtime'] = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        row['cpu'] = psutil.cpu_percent(interval=1)
        row['memory'] = psutil.virtual_memory().percent
        usage = psutil.disk_usage("/")
        row['diskusage'] = "{:.1f}".format(float(usage.free) / 1024 / 1024)
        row['uuid'] = str(uuid2)
        row['macaddress'] = psutil_iface('en0')
        print(json.dumps(row))
        #r = requests.post(url="http://hw13125.local:7979/emeter", data=json.dumps(row), headers=headers)
