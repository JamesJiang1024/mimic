import json
import urllib
import httplib2

from monster.openstack.common import cfg


rule_begin = cfg.CONF.rule_begin
rule_increase = cfg.CONF.rule_increase


def judge_roles():
    hosts_nu = hosts_num()
    pass


def get_upper(num):
    upper = {}
    rule_begin = "count=20;master=2;compute=max"
    rule_increase = "count=10;master=1;compute=max"
    rules_b = rule_begin.split(";")
    rules_i = rule_increase.split(";")
    count_begin = int(rules_b[0].split("=")[1])
    count_increase = int(rules_i[0].split("=")[1])

    rules_b = rules_b[1:]
    rules_i = rules_i[1:]

    for rule in rules_b:
        if rule.split("=")[1] != "max":
            upper[rule.split("=")[0]] = int(rule.split("=")[1])
        else:
            upper[rule.split("=")[0]] = rule.split("=")[1]

    if num - count_begin > 0:
        if (num - count_begin) % count_increase != 0:
            n = (num - count_begin)/count_increase + 1
        else:
            n = (num - count_begin)/count_increase

        for rule in rules_i:
            if upper[rule.split("=")[0]] != "max":
                upper[rule.split("=")[0]] += n * int(rule.split("=")[1])
    return upper


def hosts_num():
    return 10


if __name__ == "__main__":
    print get_upper(34)
