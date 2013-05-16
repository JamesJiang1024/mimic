import json
import urllib
import httplib2



def inform_foreman(disks, mac):
    h = httplib2.Http(".cache")
    resp, content = h.request("http://192.168.1.2:3000/api/hosts", "GET")
    hosts = json.loads(content)
    origin_mac = mac
    change_id = 0
    for host in hosts:
        host_id = host['host']['id']
        resp, content = h.request("http://192.168.1.2:3000/api/hosts/%s" % host_id, "GET")
        host_detail = json.loads(content)
        new_mac = host_detail['host']['mac']
        for origin_macd in origin_mac:
            if new_mac.upper() == origin_macd.upper():
                change_id = host_id
                put_data = {
                "host":{
                    "build": True,
                    "disk": disks,
                    "operatingsystem_id": "4"
                }
               }
                resp, content = h.request("http://192.168.1.2:3000/api/hosts/%s" % \
                change_id, "PUT", body=json.dumps(put_data), \
                headers={'content-type': 'application/json'} )
                return True
    return False


