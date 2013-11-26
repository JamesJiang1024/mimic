def get_machine(uuid, mac):
    machine = {
        "uuid": uuid,
        "discovered_mac": mac,
        "cpu": "2GHZ",
        "memory": "2G",
        "harddisk": "500G"
    }
    return machine
