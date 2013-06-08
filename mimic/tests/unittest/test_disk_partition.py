from mimic.tests.unittest import base
from mimic.api import disk_partition


class PartitionTestCase(base.TestCase):
    def fake_part(self):
        fake_parts = "part raid.001 --size=500 --ondisk=sda\n\r"
        fake_parts += "part raid.101 --size=1 --grow --ondisk=sda\n\r"
        fake_parts += "part raid.002 --size=500 --ondisk=sdb\n\r"
        fake_parts += "part raid.102 --size=1 --grow --ondisk=sdb\n\r"
        fake_parts += "raid /boot --fstype='ext4' --level=1 --device=['raid.001', 'raid.002']\n\r"
        fake_parts += "raid pv.1 --size=1 --grow --level=1 --device=['raid.101', 'raid.102']\n\r"
        fake_parts += "volgroup VolGroup00 --pesize=32768 pv.1\n\r"
        fake_parts += "logvol swap --fstype swap --name=LogVol00 --vgname=VolGroup00 --size=512 --grow --maxsize=10240\n\r"
        fake_parts += "logvol / --fstype ext4 --name=LogVol01 --vgname=VolGroup00 --size=4096 --grow --maxsize=51200\n\r"
        fake_parts += "logvol /home --fstype ext4 --name=LogVol02 --vgname=VolGroup00 --size=1048 --grow --maxsize=51200\n\r"
        fake_parts += "logvol /data0 --fstype ext4 --name=LogVol03 --vgname=VolGroup00 --size=512 --grow --maxsize=51200\n\r"
        fake_parts += "logvol /data1 --fstype ext4 --name=LogVol04 --vgname=VolGroup00 --size=512 --grow --maxsize=51200\n\r"
        return fake_parts

    def test_raid_partition_notalone_noraidcard(self):
        partition = disk_partition.Partition(['sda', 'sdb'])
        self.assertTrue(partition.devices == ['sda', 'sdb'])
        self.assertTrue(partition.doraid == True)
        self.assertTrue(partition.devices_number == 2)
        self.assertTrue(partition.parts, self.fake_part())


