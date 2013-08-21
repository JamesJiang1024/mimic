# vim: tabstop=4 shiftwidth=4 softtabstop=4

from oslo.config import cfg

ENGINE_SERVICE_OPTS = [
    cfg.StrOpt('foreman_address',
               default="http://127.0.0.1:3000",
               help='foreman_address'),
    cfg.StrOpt('foreman_proxy_address',
               default="http://127.0.0.1:8443",
               help='foreman_proxy_address'),
    cfg.StrOpt('rule_begin',
               default="count=20;master=2;compute=max",
               help='rule_begin'),
    cfg.StrOpt('rule_increase',
               default="count=10;master=1;compute=max",
               help='rule_increase')
]

CONF = cfg.CONF
CONF.register_opts(ENGINE_SERVICE_OPTS)
