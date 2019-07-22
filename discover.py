from pyHS100 import Discover

for dev in Discover.discover().values():
    print(dev)
    print("host:" + dev.host)
