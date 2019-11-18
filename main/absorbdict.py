import sys
import time

# TODO:file_nameが指定されていませんと出力の有無を指定していません的なメッセージを出す
# TODO:マルチセルポリシーに対応する
file_name = sys.argv[1]
disable_policy_output = sys.argv[2]

start = time.time()

policy_name_key = ['set', 'policy', 'id', 'policy_id', 'name', 'policy_name', 'from', 'src_zone', 'to',
                   'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'dst', 'ip', 'dst_nat_ip', 'expect', 'log']
policy_name_keyex = ['set', 'policy', 'id', 'policy_id', 'name', 'policy_name',
                     'from', 'src_zone', 'to',  'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'expect']

policy_noname_key = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone',
                     'to',  'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'expect', 'log']
policy_noname_key1 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone',
                      'to',  'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'expect', 'log']
policy_noname_key2 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',  'dst_zone',
                      'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'dip_id', 'dip_num', 'expect', 'log']
policy_noname_key3 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',
                      'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'ip', 'src_nat_ip', 'expect', 'log']
policy_noname_key4 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',
                      'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'nat', 'dst', 'ip', 'dst_nat_ip', 'expect', 'log']
policy_noname_key5 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',  'dst_zone',
                      'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'dst', 'ip', 'dst_nat_ip', 'expect', 'log']
policy_noname_key6 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',  'dst_zone', 'src_ip',
                      'dst_ip', 'protocol', 'nat', 'dst', 'ip', 'dst_nat_ip', 'port', 'dst_nat_port', 'expect', 'log']

service_key = ['set', 'service', 'service_name', 'protocol', 'protocol_name',
               'src-port', 'src_port_num', 'dst_port', 'dst_port_num', 'timeout', 'timeouttime']
route_key = ['set', 'route', 'network_address', 'interface',
             'if_name', 'gateway', 'gateway_ip', 'metric', 'metric_num']
address_key = ['set', 'address', 'zone_name',
               'address_name', 'ip_address', 'subnet_mask']
group_address_key = ['set', 'group', 'address',
                     'zone_name', 'group_name', 'add', 'address_name']
group_service_key = ['set', 'group', 'service',
                     'group_service_name', 'add', 'service_name']

vip_key = ['set', 'interface', 'if_name', 'vip',
           'global_ip', 'port_num', 'service_name', 'private_ip']
vip_keys = ['set', 'interface', 'if_name', 'vip', 'global_ip',
            '+', 'port_num', 'service_name', 'private_ip']
mip_key = ['set', 'interface', 'if_name', 'mip', 'private_ip',
           'host', 'global_ip', 'netmask', 'subnet_mask', 'vr', 'vr_name']
dip_key = ['set', 'interface', 'if_name',
           'dip', 'dip_num', 'start_ip', 'finish_ip']
dip_ext_key = ['set', 'interface', 'if_name', 'ext', 'ip', 'global_ip',
               'subnet_mask', 'dip', 'dip_num', 'start_ip', 'finish_ip']
if_ip_key = ['set', 'interface', 'if_name', 'ip', 'ip_address']
if_nat_key = ['set', 'interface', 'if_name', 'nat']
if_mip_key = ['set', 'interface', 'if_name', 'mip', 'ip_address',
              'host' 'global_ip' 'netmask' 'subnet_mask' 'vr', 'vr_name']
if_zone_key = ['set', 'interface', 'if_name', 'zone', 'zone_name']
if_zonev_key = ['set', 'interface', 'if_name',
                'tag', 'vlan_num', 'zone', 'zone_name']
zone_block_key = ['set', 'zone', 'zone_name', 'block']
disable_policy_key = ['set', 'policy', 'id', 'policy_id', 'disable']

policy_dict = []
service_dict = []
route_dict = []
address_dict = []
group_address_dict = []
group_service_dict = []
vip_dict = []
mip_dict = []
dip_dict = []
if_ip_dict = []
if_nat_dict = []
if_zone_dict = []
zone_block_dict = []
disable_policy_dict = []


def convert_list_to_dict(key, value, dictionary):
    d = {k: v for k, v in zip(
        key, value)}
    dictionary.append(d)


def append_noname_to_policy_dict(policy_noname):
    value = policy_noname
    dictionary = policy_dict
    if len(policy_noname) == 13 and "log" in policy_noname or len(policy_noname) == 12 and "log" not in policy_noname:
        key = policy_noname_key
        convert_list_to_dict(key, value, dictionary)
    elif len(policy_noname) == 15 and "log" in policy_noname or len(policy_noname) == 14 and "log" not in policy_noname:
        key = policy_noname_key1
        convert_list_to_dict(key, value, dictionary)
    elif len(policy_noname) == 17 and "src" in policy_noname and "dip-id" in policy_noname and "log" in policy_noname or len(policy_noname) == 16 and "src" in policy_noname and "dip-id" in policy_noname and "log" not in policy_noname:
        key = policy_noname_key2
        convert_list_to_dict(key, value, dictionary)
    elif len(policy_noname) == 17 and "src" in policy_noname and "log" in policy_noname or len(policy_noname) == 16 and "src" in policy_noname and "log" not in policy_noname:
        key = policy_noname_key3
        convert_list_to_dict(key, value, dictionary)
    elif len(policy_noname) == 17 and "dst" in policy_noname and "log" in policy_noname or len(policy_noname) == 16 and "dst" in policy_noname and "log" not in policy_noname:
        key = policy_noname_key4
        convert_list_to_dict(key, value, dictionary)
    elif len(policy_noname) == 18 and "log" in policy_noname or len(policy_noname) == 17 and "log" not in policy_noname:
        key = policy_noname_key5
        convert_list_to_dict(key, value, dictionary)
    elif len(policy_noname) == 19 and "log" in policy_noname or len(policy_noname) == 18 and "log" not in policy_noname:
        key = policy_noname_key6
        convert_list_to_dict(key, value, dictionary)


def absorb_config():
    with open(file_name) as fin:
        for line in fin:
            if "manage" in line or "bypass" in line or "proxy-arp-entry" in line or "mtu" in line or "unset" in line or "sharable" in line:
                continue
            if "set policy id" in line and "name" in line and "from" in line:
                policy_name = value = line.strip().split()
                dictionary = policy_dict
                if len(policy_name) == 20 and "log" in policy_name or len(policy_name) == 19 and "log" not in policy_name:
                    key = policy_name_key
                    convert_list_to_dict(key, value, dictionary)
                elif len(policy_name) == 15 and "log" in policy_name or len(policy_name) == 14 and "log" not in policy_name:
                    key = policy_name_keyex
                    convert_list_to_dict(key, value, dictionary)
            elif "set policy id" in line and not "name" in line and "from" in line:
                policy_noname = line.strip().split()
                append_noname_to_policy_dict(policy_noname)
            elif "set group service" in line:
                group_service = value = line.strip().split()
                dictionary = group_service_dict
                if len(group_service) == 6:
                    key = group_service_key
                    convert_list_to_dict(key, value, dictionary)
            elif "set service" in line:
                service = value = line.strip().split()
                if len(service) >= 9:
                    d = {k: v for k, v in zip(service_key, service)}
                    service_dict.append(d)
            elif "set route" in line and "interface" in line:
                route = value = line.strip().split()
                d = {k: v for k, v in zip(route_key, route)}
                route_dict.append(d)
            elif "set group address" in line:
                group_address = value = line.strip().split()
                if len(group_address) == 7:
                    d = {k: v for k, v in zip(
                        group_address_key, group_address)}
                    group_address_dict.append(d)
            elif "set address" in line:
                address = value = line.strip().split()
                d = {k: v for k, v in zip(address_key, address)}
                address_dict.append(d)
            elif "set interface" in line and "vip" in line:
                vip = value = line.strip().split()
                if "+" in vip:
                    d = {k: v for k, v in zip(vip_keys, vip)}
                    vip_dict.append(d)
                else:
                    d = {k: v for k, v in zip(vip_key, vip)}
                    vip_dict.append(d)
            elif "set interface" in line and "dip" in line:
                dip = value = line.strip().split()
                if "ext" in dip:
                    d = {k: v for k, v in zip(dip_ext_key, dip)}
                    dip_dict.append(d)
                else:
                    d = {k: v for k, v in zip(dip_key, dip)}
                    dip_dict.append(d)
            elif "set interface" in line and "mip" in line:
                mip = value = line.strip().split()
                d = {k: v for k, v in zip(mip_key, mip)}
                mip_dict.append(d)
            elif "set interface" in line and "ip" in line:
                if_ip = value = line.strip().split()
                d = {k: v for k, v in zip(if_ip_key, if_ip)}
                if_ip_dict.append(d)
            elif "set interface" in line and "nat" in line:
                if_nat = value = line.strip().split()
                d = {k: v for k, v in zip(if_nat_key, if_nat)}
                if_nat_dict.append(d)
            elif "set interface" in line and "zone" in line:
                if_zone = value = line.strip().split()
                if '"bri0/0"' in if_zone:
                    pass
                elif "tag" in if_zone:
                    d = {k: v for k, v in zip(if_zonev_key, if_zone)}
                    if_zone_dict.append(d)
                else:
                    d = {k: v for k, v in zip(if_zone_key, if_zone)}
                    if_zone_dict.append(d)
            elif "set zone" in line and "block" in line:
                zone_block = value = line.strip().split()
                d = {k: v for k, v in zip(zone_block_key, zone_block)}
                zone_block_dict.append(d)
            elif "disable" in line:
                disable_policy = value = line.strip().split()
                d = {k: v for k, v in zip(disable_policy_key, disable_policy)}
                disable_policy_dict.append(d)
            else:
                continue


def exclude_disable_policy():
    for policy in policy_dict:
        for disable_policy in disable_policy_dict:
            if policy['policy_id'] == disable_policy['policy_id']:
                policy_dict.remove(policy)
                break
        else:
            continue


def handle_disable_policy_output():
    if disable_policy_output == 'y':
        absorb_config()
    elif disable_policy_output == 'n':
        absorb_config()
        exclude_disable_policy()
    else:
        print('Error! Input again.')


handle_disable_policy_output()
