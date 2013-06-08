from mimic.openstack.common import log as logging


LOG = logging.getLogger(__name__)


class Partition(object):

    def __init__(self, devices, raidcard="no"):
        if raidcard == "no" and len(devices) > 1:
            self.doraid = True
        else:
            self.doraid = False

        self.parts = ""
        self.devices = devices
        self.devices_number = len(devices)
        self._do_rules()

    def _raid_partition(self, bootdevice, pvdevice):
        if self.devices_number % 2 == 0:
            if self.devices_number / 2 > 1:
                level = 10
            else:
                level = 1
            self.parts += "raid /boot --fstype='ext4' --level=%s \
                    --device=%s \n\r" % (level, bootdevice)
            self.parts += "raid pv.1 --size=1 --grow --level=%s \
                    --device=%s \n\r" % (level, pvdevice)

    def _do_rules(self):
        if self.doraid:
            (bootdevice, pvdevice) = self._do_raid()
            self._raid_partition(bootdevice, pvdevice)
        else:
            self._no_raid_partition()
        self._volgroup_build()

    def _no_raid_partition(self):
        self.parts += "part /boot --fstype=ext4 --size=500\n\r"
        self.parts += "part pv.1 --size=1 --grow\n\r"

    def _volgroup_build(self):
        self.parts += "volgroup VolGroup00 --pesize=32768 pv.1 \n\r"
        self.parts += "logvol swap --fstype swap --name=LogVol00 \
                --vgname=VolGroup00 --size=512 --grow --maxsize=10240 \n\r"
        self.parts += "logvol / --fstype ext4 --name=LogVol01 \
                --vgname=VolGroup00 --size=4096 --grow --maxsize=51200 \n\r"
        self.parts += "logvol /home --fstype ext4 --name=LogVol02 \
                --vgname=VolGroup00 --size=1048 --grow --maxsize=51200 \n\r"
        self.parts += "logvol /data0 --fstype ext4 --name=LogVol03 \
                --vgname=VolGroup00 --size=512 --grow --maxsize=51200 \n\r"
        self.parts += "logvol /data1 --fstype ext4 --name=LogVol04 \
                --vgname=VolGroup00 --size=512 --grow --maxsize=51200 \n\r"

    def _do_raid(self):
        bootdevice = []
        pvdevice = []
        count = 0
        for device in self.devices:
            count += 1
            raid_num = str(count)
            if count < 10:
                raid_num = "0"+str(count)

            self.parts += "part raid.0%s --size=500 \
                    --ondisk=%s \n\r" % (raid_num, device)
            bootdevice.append("raid.0%s" % raid_num)
            self.parts += "part raid.1%s --size=1 \
                    --grow --ondisk=%s \n\r" % (raid_num, device)
            pvdevice.append("raid.1%s" % raid_num)

        return (bootdevice, pvdevice)
