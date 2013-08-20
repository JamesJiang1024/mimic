from oslo.config import cfg
from mimic.engine import foreman_helper


rule_begin = cfg.CONF.rule_begin
rule_increase = cfg.CONF.rule_increase


def judge_hostgroup():
    hosts_nu = len(foreman_helper.hosts())
    hosts_nu += 1
    (upper, sequence) = _upper_bound(hosts_nu)
    while len(sequence) != 0:
        node = sequence.pop(0)
        if upper[node] == "max":
            return foreman_helper.host_groups()[node]
        if hosts_nu - upper[node] > 0:
            hosts_nu -= upper[node]
        else:
            return foreman_helper.host_groups()[node]


def _upper_bound(num):
    upper = {}
    sequence = []

    rules_b = rule_begin.split(";")
    rules_i = rule_increase.split(";")

    count_begin = int(rules_b[0].split("=")[1])
    count_increase = int(rules_i[0].split("=")[1])

    rules_b = rules_b[1:]
    rules_i = rules_i[1:]

    for rule in rules_b:
        sequence.append(rule.split("=")[0])
        if rule.split("=")[1] != "max":
            upper[rule.split("=")[0]] = int(rule.split("=")[1])
        else:
            upper[rule.split("=")[0]] = rule.split("=")[1]

    if num - count_begin > 0:
        if (num - count_begin) % count_increase != 0:
            n = (num - count_begin) / count_increase + 1
        else:
            n = (num - count_begin) / count_increase

        for rule in rules_i:
            if upper[rule.split("=")[0]] != "max":
                upper[rule.split("=")[0]] += n * int(rule.split("=")[1])
    return (upper, sequence)
