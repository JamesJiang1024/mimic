import pprint
import threading

from oslo.config import cfg
import pecan

from mimic.api import config
from mimic.api import hooks
from mimic.api import middleware
from mimic.openstack.common import log as logger
from mimic.openstack.common import memorycache


CONF = cfg.CONF
LOG = logger.getLogger(__name__)


AUTH_OPTIONS = [
    cfg.StrOpt('auth_host',
               default='localhost',
               help='Username to use for openstack service access'),
    cfg.StrOpt('auth_port',
               default='35357',
               help='Username to use for openstack service access'),
    cfg.StrOpt('auth_protocol',
               default='http',
               help='Username to use for openstack service access'),
    cfg.StrOpt('auth_api_version',
               default='v3',
               help='Username to use for openstack service access'),
    cfg.StrOpt('admin_user_domain_name',
               default='',
               help='Username to use for openstack service access'),
    cfg.StrOpt('admin_username',
               default='',
               help='Username to use for openstack service access'),
    cfg.StrOpt('admin_password',
               default='',
               help='Username to use for openstack service access'),
    cfg.StrOpt('admin_project_name',
               default='service',
               help='Username to use for openstack service access'),
    cfg.StrOpt('admin_project_domain_name',
               default='Default',
               help='Username to use for openstack service access'),
]
opt_group = cfg.OptGroup(name='AUTH',
                         title='Options for keystone service')
CONF.register_group(opt_group)
CONF.register_opts(AUTH_OPTIONS, opt_group)


def get_service_url(service_type, interface, project_id=None):
    endpoints = load_endpoints()
    endpoint = endpoints[service_type][interface]
    if project_id:
        endpoint = (endpoint.replace('$', '%') %
                    {'tenant_id': project_id, 'project_id': project_id})
    return endpoint


def force_v3_api(url):
    if url is None:
        return url
    if url.endswith('/v2.0'):
        return url.replace('/v2.0', '/v3')
    return url


_cache = memorycache.get_client(CONF.memcached_servers)


def load_endpoints():

    from keystoneclient.v3 import client

    ENDPOINT_CACHE_KEY = "minic:endpoints"
    _cache_endpoints = _cache.get(ENDPOINT_CACHE_KEY)
    if _cache_endpoints:
        return _cache_endpoints

    with threading.Lock():
        user_domain = CONF.AUTH.admin_user_domain_name
        user = CONF.AUTH.admin_username
        password = CONF.AUTH.admin_password
        project = CONF.AUTH.admin_project_name
        project_domain = CONF.AUTH.admin_project_domain_name
        auth_url = "%s://%s:%s/%s" % (CONF.AUTH.auth_protocol,
                                      CONF.AUTH.auth_host,
                                      CONF.AUTH.auth_port,
                                      CONF.AUTH.auth_api_version)

        c = client.Client(user_domain_name=user_domain,
                          username=user,
                          password=password,
                          project_domain_name=project_domain,
                          project_name=project,
                          auth_url=auth_url)

        # force use v3 endpoint
        c.management_url = force_v3_api(c.management_url)

        try:
            service_list = c.services.list()
            endpoint_list = c.endpoints.list()
        except Exception as e:
            LOG.exception('failed to load endpoints from kesytone:%s' % e)
            service_list = []
            endpoint_list = []

        _service_id_map = {}
        ENDPOINTS = {}
        for service in service_list:
            ENDPOINTS[service.type] = {}
            _service_id_map[service.id] = service.type

        for endpoint in endpoint_list:
            service_type = _service_id_map[endpoint.service_id]
            if service_type == 'identity':
                url = force_v3_api(endpoint.url)
            else:
                url = endpoint.url
            ENDPOINTS[service_type][endpoint.interface] = url

        LOG.debug('endpoints: %s' % pprint.pprint(ENDPOINTS))
        _cache.set(ENDPOINT_CACHE_KEY, ENDPOINTS)
    return ENDPOINTS


def get_pecan_config():
    # Set up the pecan configuration
    filename = config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def setup_app(config, extra_hooks=None):

    app_hooks = [hooks.DBHook()]

    if extra_hooks:
        app_hooks.extend(extra_hooks)

    if not config:
        config = get_pecan_config()

    app = pecan.make_app(
        config.app.root,
        static_root=config.app.static_root,
        template_path=config.app.template_path,
        debug=CONF.debug,
        force_canonical=getattr(config.app, 'force_canonical', True),
        hooks=app_hooks,
        wrap_app=middleware.FaultWrapperMiddleware,
    )
    pecan.conf.update({'wsme': {'debug': CONF.debug}})

    return app


class VersionSelectorApplication(object):
    def __init__(self):
        load_endpoints()
        pc = get_pecan_config()
        self.v1 = setup_app(config=pc)

    def __call__(self, environ, start_response):
        return self.v1(environ, start_response)
