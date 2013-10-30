from mimic.api import app

from oslo.config import cfg

from designateclient.v1 import Client


CONF = cfg.CONF

designate_opts = [
    cfg.StrOpt('domain_name',
               default='ustack.in',
               help="the required domain saved in designate.")
]
opt_group = cfg.OptGroup(name='designate',
                         title='Options for dns service')
CONF.register_group(opt_group)
CONF.register_opts(designate_opts, opt_group)

_CLIENT = None
_REQUIRE_DOMAIN_ID = None


def designate_client():
    global _CLIENT

    if _CLIENT is None:
        endpoint = app.load_endpoints()['dns']['admin']
        # Currently designate is set to noauth
        _CLIENT = Client(endpoint=endpoint, token="fake_token")
    return _CLIENT


def get_domain_list():
    domain_manager = designate_client().domains
    return domain_manager.list()


def create_record(name, data, type="A"):
    global _REQUIRE_DOMAIN_ID

    record_manager = designate_client().records
    if _REQUIRE_DOMAIN_ID is None:
        domain_list = get_domain_list()
        for _d in domain_list:
            if _d.name.strip('.') == CONF.designate.domain_name.strip('.'):
                _REQUIRE_DOMAIN_ID = _d.id
                break

        if _REQUIRE_DOMAIN_ID is None:
            raise Exception("required domain `%s` is not found." %
                            CONF.designate.domain_name)

    name = name if name.endswith('.') else name + '.'
    return record_manager.create(_REQUIRE_DOMAIN_ID,
                                 {'name': name, 'type': type, 'data': data})
