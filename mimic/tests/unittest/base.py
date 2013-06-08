import testtools
import mox


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.mox = mox.Mox()
