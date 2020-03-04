import sys

# TODO:マルチセルポリシーに対応する

option = sys.argv

ifinfo = []

value_name_key = ['set', 'policy', 'id', 'policy_id', 'name', 'value_name', 'from', 'src_zone', 'to',
                  'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'dst', 'ip', 'dst_nat_ip', 'expect', 'log']
value_name_keyex = ['set', 'policy', 'id', 'policy_id', 'name', 'value_name',
                    'from', 'src_zone', 'to',  'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'expect']

value_noname_key = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone',
                    'to',  'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'expect', 'log']
value_noname_key1 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone',
                     'to',  'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'expect', 'log']
value_noname_key2 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',  'dst_zone',
                     'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'dip_id', 'dip_num', 'expect', 'log']
value_noname_key3 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',
                     'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'ip', 'src_nat_ip', 'expect', 'log']
value_noname_key4 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',
                     'dst_zone', 'src_ip', 'dst_ip', 'protocol', 'nat', 'dst', 'ip', 'dst_nat_ip', 'expect', 'log']
value_noname_key5 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',  'dst_zone',
                     'src_ip', 'dst_ip', 'protocol', 'nat', 'src', 'dst', 'ip', 'dst_nat_ip', 'expect', 'log']
value_noname_key6 = ['set', 'policy', 'id', 'policy_id', 'from', 'src_zone', 'to',  'dst_zone', 'src_ip',
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
           'dip', 'dip_num', 'start_ip', 'fish_ip']
dip_ext_key = ['set', 'interface', 'if_name', 'ext', 'ip', 'global_ip',
               'subnet_mask', 'dip', 'dip_num', 'start_ip', 'fish_ip']
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


def append_noname_to_policy_dict(value):
    dictionary = policy_dict
    if len(value) == 13 and "log" in value or len(value) == 12 and "log" not in value:
        key = value_noname_key
        convert_list_to_dict(key, value, dictionary)
    elif len(value) == 15 and "log" in value or len(value) == 14 and "log" not in value:
        key = value_noname_key1
        convert_list_to_dict(key, value, dictionary)
    elif len(value) == 17 and "src" in value and "dip-id" in value and "log" in value or len(value) == 16 and "src" in value and "dip-id" in value and "log" not in value:
        key = value_noname_key2
        convert_list_to_dict(key, value, dictionary)
    elif len(value) == 17 and "src" in value and "log" in value or len(value) == 16 and "src" in value and "log" not in value:
        key = value_noname_key3
        convert_list_to_dict(key, value, dictionary)
    elif len(value) == 17 and "dst" in value and "log" in value or len(value) == 16 and "dst" in value and "log" not in value:
        key = value_noname_key4
        convert_list_to_dict(key, value, dictionary)
    elif len(value) == 18 and "log" in value or len(value) == 17 and "log" not in value:
        key = value_noname_key5
        convert_list_to_dict(key, value, dictionary)
    elif len(value) == 19 and "log" in value or len(value) == 18 and "log" not in value:
        key = value_noname_key6
        convert_list_to_dict(key, value, dictionary)


def append_if_zone_to_zone_dict(value):
    if_zone = value
    if '"bri0/0"' in if_zone:
        pass
    elif "tag" in if_zone:
        d = {k: v for k, v in zip(if_zonev_key, if_zone)}
        if_zone_dict.append(d)
    else:
        d = {k: v for k, v in zip(if_zone_key, if_zone)}
        if_zone_dict.append(d)


def create_ifinfo():
    global ifinfo
    for if_zone_c in if_zone_dict:
        flag = False
        for if_ip_c in if_ip_dict:
            if if_zone_c['if_name'].replace('"', '') in if_ip_c['if_name']:
                flag = True
                d = {'IF_Name': if_zone_c['if_name'].replace('"', ''), 'Zone': if_zone_c['zone_name'], 'IP': if_ip_c.get('ip_address')}
                ifinfo.append(d)
        else:
            if not flag:
                d = {'IF_Name': if_zone_c['if_name'], 'Zone': if_zone_c['zone_name'], 'IP': 'None'}
                ifinfo.append(d)
    print(ifinfo)


def absorb_config():
    with open(file_name) as f:
        for line in f:
            value = line.strip().split()
            if "manage" in line or "bypass" in line or "proxy-arp-entry" in line or "mtu" in line or "unset" in line or "sharable" in line:
                continue
            if "set policy id" in line and "name" in line and "from" in line:
                dictionary = policy_dict
                if len(value) == 20 and "log" in value or len(value) == 19 and "log" not in value:
                    key = value_name_key
                    convert_list_to_dict(key, value, dictionary)
                elif len(value) == 15 and "log" in value or len(value) == 14 and "log" not in value:
                    key = value_name_keyex
                    convert_list_to_dict(key, value, dictionary)
            elif "set policy id" in line and not "name" in line and "from" in line:
                append_noname_to_policy_dict(value)
            elif "set group service" in line:
                group_service = value
                dictionary = group_service_dict
                if len(group_service) == 6:
                    key = group_service_key
                    convert_list_to_dict(key, value, dictionary)
            elif "set service" in line:
                service = value
                if len(service) >= 9:
                    d = {k: v for k, v in zip(service_key, service)}
                    service_dict.append(d)
            elif "set route" in line and "interface" in line:
                route = value
                d = {k: v for k, v in zip(route_key, route)}
                route_dict.append(d)
            elif "set group address" in line:
                group_address = value
                if len(group_address) == 7:
                    d = {k: v for k, v in zip(
                        group_address_key, group_address)}
                    group_address_dict.append(d)
            elif "set address" in line:
                address = value
                d = {k: v for k, v in zip(address_key, address)}
                address_dict.append(d)
            elif "set interface" in line and "vip" in line:
                vip = value
                if "+" in vip:
                    d = {k: v for k, v in zip(vip_keys, vip)}
                    vip_dict.append(d)
                else:
                    d = {k: v for k, v in zip(vip_key, vip)}
                    vip_dict.append(d)
            elif "set interface" in line and "dip" in line:
                dip = value
                if "ext" in dip:
                    d = {k: v for k, v in zip(dip_ext_key, dip)}
                    dip_dict.append(d)
                else:
                    d = {k: v for k, v in zip(dip_key, dip)}
                    dip_dict.append(d)
            elif "set interface" in line and "mip" in line:
                mip = value
                d = {k: v for k, v in zip(mip_key, mip)}
                mip_dict.append(d)
            elif "set interface" in line and "ip" in line:
                if_ip = value
                d = {k: v for k, v in zip(if_ip_key, if_ip)}
                if_ip_dict.append(d)
            elif "set interface" in line and "nat" in line:
                if_nat = value
                d = {k: v for k, v in zip(if_nat_key, if_nat)}
                if_nat_dict.append(d)
            elif "set interface" in line and "zone" in line:
                append_if_zone_to_zone_dict(value)
            elif "set zone" in line and "block" in line:
                dictionary = zone_block_dict
                key = zone_block_key
                convert_list_to_dict(key, value, dictionary)
            elif "disable" in line:
                dictionary = disable_policy_dict
                key = disable_policy_key
                convert_list_to_dict(key, value, dictionary)
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
        print('有効化していないポリシーも出力します')
        absorb_config()
    elif disable_policy_output == 'n':
        print('有効化していないポリシーは出力しません')
        absorb_config()
        exclude_disable_policy()
    else:
        print('第２引数を入力する場合はyかnを入力してください')
        exit()


def confirm_file():
    global file_name
    try:
        file_name = option[1]
    except IndexError:
        print('コンフィグファイル名を入力してください')
        exit()
    

def confirm_disable_policy_output():
    global disable_policy_output
    if len(option) == 2:
        print('有効化していないポリシーの出力オプションが入力されていません')
        disable_policy_output = 'n'
    else:
        disable_policy_output = option[2]
    handle_disable_policy_output()


confirm_file()
confirm_disable_policy_output()
create_ifinfo()