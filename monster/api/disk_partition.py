from monster.openstack.common import wsgi


LOG = logging.getLogger(__name__)


class Partition(object):

    def __init__(self, devices, raidcard=False):
        if dicts['raid_card'] == 'no' and dicts['disks'].__len__() > 1:
            self.doraid = True
        else:
            self.doraid = False

        self.parts = ""
        self.devices = devices
        self.raidcard = raidcard
        self.devices_number = devices.__len__()

    def partition(self, parts, device_num, bootdevice, pvdevice):
        if device_num % 2 == 0:
            if device_num / 2 > 1:
                level = 10
            else:
                level = 1
            parts+="raid /boot --fstype='ext4' --level=%s --device=%s \n\r" % (level, bootdevice)
            parts+="raid pv.1 --size=1 --grow --level=%s --device=%s \n\r" % (level, pvdevice)
            return parts

    def do_rules(self):
            (bootdevice, pvdevice) = self._do_raid()
        else:


    def partition_no_raid(parts, device):
        parts+="part /boot --fstype=ext4 --size=500\n\r"
        parts+="part pv.1 --size=1 --grow\n\r"
        return parts


    def volgroup_build(parts):
        parts+="volgroup VolGroup00 --pesize=32768 pv.1 \n\r"
        parts+="logvol swap --fstype swap --name=LogVol00 --vgname=VolGroup00 --size=512 --grow --maxsize=10240 \n\r"
        parts+="logvol / --fstype ext4 --name=LogVol01 --vgname=VolGroup00 --size=4096 --grow --maxsize=51200 \n\r"
        parts+="logvol /home --fstype ext4 --name=LogVol02 --vgname=VolGroup00 --size=1048 --grow --maxsize=51200 \n\r"
        parts+="logvol /data0 --fstype ext4 --name=LogVol03 --vgname=VolGroup00 --size=512 --grow --maxsize=51200 \n\r"
        parts+="logvol /data1 --fstype ext4 --name=LogVol04 --vgname=VolGroup00 --size=512 --grow --maxsize=51200 \n\r"
        return parts

    def _do_raid():
        bootdevice = []
        pvdevice = []
        for device in self.devices:
            count += 1
            raid_num=str(count)
            if count < 10:
                raid_num = "0"+str(count)

            self.parts+="part raid.0%s --size=500 --ondisk=%s \n\r" % (raid_num, device)
            bootdevice.append("raid.0%s" % raid_num)
            self.parts+="part raid.1%s --size=1 --grow --ondisk=%s \n\r" % (raid_num, device)
            pvdevice.append("raid.1%s" % raid_num)

        return (bootdevice, pvdevice)

