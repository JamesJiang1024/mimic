class FakeObject():
    pass


class FakeDBAPI():
    def create_lookup_value(self, value):
        return None

    def get_lookup_key(self, name, value):
        return [20]

    def find_lookup_value_by_match(self, match):
        test = FakeObject()
        test.value = "20"
        return [test]

    def find_lookup_value_by_id_match(self, id, match):
        test = FakeObject()
        test.value = "20"
        test.id = 50
        return [test]

    def update_lookup_value(self, key, value):
        return True


def get_fake_hosts():
    return [
            {
            "host": {
                "name": "master"
            }
            },
            {
            "host": {
                "name": "compute"
            }
            }
           ]
