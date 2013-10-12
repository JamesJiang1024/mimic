#!/usr/bin/python
import json

po = file("/root/workspace/mimic/etc/mimic/policy.json")
policys = json.load(po)
result = ""
for key in policys:
    result = result + "'" + key + "'" + ","

print "update lookup_keys set override=1 where lookup_keys.key in (%s)" % result[:-1]
