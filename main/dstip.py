import ipaddress

from main import absorbdict
from main import multiple

dst_ip = []

# dst-ipのリストの生成


# 条件によってappendするdata数が異なるため注意
def select_dst_ip_from_scope_ip(policy, scope_ip):
    global dst_ip
    service_name = policy['protocol']
    judge_service_name(service_name)
    if policy['src_ip'] == '"Any"' and policy['src_zone'] != '"Untrust"':
        dst_ip += [str(scope_ip[1]), str(scope_ip[-2]),
                   str(scope_ip[-2]), str(scope_ip[1])] * service_element_num
    elif "VIP" in policy['src_ip'] and policy['protocol'] == '"ANY"':
        for vip_c in absorbdict.vip_dict:
            if policy['src_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
                dst_ip += [str(scope_ip[1]), str(scope_ip[-2])
                           ] * service_element_num
            elif policy['src_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
                dst_ip += [str(scope_ip[1]), str(scope_ip[-2])
                           ] * service_element_num
    else:
        src_address_name = policy['src_ip']
        judge_src_address_name(src_address_name)
        dst_ip += [str(scope_ip[1]), str(scope_ip[-2])] * \
            service_element_num * src_address_element_num


# 該当するIFで定義している中で最も広いnetworkアドレスを返す
def dst_if_network_range(dst_if):
    global route_network
    for if_ip_c in absorbdict.if_ip_dict:
        route_network = ipaddress.ip_network("2.3.4.5/32")
        if dst_if.replace('"', '') == if_ip_c['if_name'] and if_ip_c['ip_address'] is not None:
            if ipaddress.IPv4Network(if_ip_c['ip_address'], strict=False).num_addresses > ipaddress.IPv4Network(route_network, strict=False).num_addresses:
                route_network = ipaddress.ip_network(
                    if_ip_c['ip_address'], strict=False)
            return route_network


# routingされている中で最も広いnetworkアドレスを返す
def dst_if_route_network_range(policy, dst_zone):
    global route_network
    confirm_dst_if(policy, dst_zone)
    route_network = ipaddress.ip_network("1.2.3.4/32")
    for route_c in absorbdict.route_dict:
        if dst_if.replace('"', '') == route_c['if_name'].replace('"', ''):
            if route_c['network_address'] == "0.0.0.0/0":
                continue
            elif ipaddress.IPv4Network(route_c['network_address']).num_addresses > ipaddress.IPv4Network(route_network).num_addresses:
                route_network = ipaddress.ip_network(
                    route_c['network_address'])
                return route_network
            else:
                continue
            break
    else:
        # IFにIPが振られているか確認
        for if_ip_c in absorbdict.if_ip_dict:
            if dst_if.replace('"', '') == if_ip_c['if_name'] and if_ip_c.get('ip_address') is not None:
                dst_if_network_range(dst_if)
                break
            else:
                continue


def convert_network_address_to_scope_ip(network_address_list):
    global scope_ip
    scope_ip = ipaddress.ip_network("2.2.2.2/32")
    for item in network_address_list:
        if ipaddress.IPv4Network(item).num_addresses > ipaddress.IPv4Network(scope_ip).num_addresses:
            scope_ip = item
    return scope_ip


def define_scope_ip(policy, network_address_list):
    convert_network_address_to_scope_ip(network_address_list)
    select_dst_ip_from_scope_ip(policy, scope_ip)


def get_used_fw_ip():
    global fw_ip
    fw_ip = []
    for if_ip_c in absorbdict.if_ip_dict:
        fw_ip += [ipaddress.ip_network(if_ip_c['ip_address'].split('/')[0])]
    return fw_ip


def exclude_fw_ip_from_scope_ip(scope_ip):
    global network_address_list
    network_address_list = []
    get_used_fw_ip()
    for fw_ip_c in fw_ip:
        if fw_ip_c.subnet_of(scope_ip):
            after_scope_ip = scope_ip.address_exclude(fw_ip_c)
            network_address_list += after_scope_ip
    else:
        if network_address_list == []:
            network_address_list += [scope_ip]
        else:
            pass
    return network_address_list


def add_dst_ip_list_to_subnet_mask(dst_ip_list):
    global exclude_ip_range_list
    exclude_ip_range_list = []
    for dst_ip_list_c in dst_ip_list:
        for address_c in absorbdict.address_dict:
            if dst_ip_list_c == address_c['address_name'] and address_c.get('subnet_mask') is not None:
                exclude_ip_range = ipaddress.ip_network(
                    address_c['ip_address'] + '/' + address_c['subnet_mask'])
                exclude_ip_range_list += [exclude_ip_range]
                break
            elif "MIP" in dst_ip_list_c:
                for mip_c in absorbdict.mip_dict:
                    if dst_ip_list_c.strip(')"').split('(')[1] == mip_c['private_ip']:
                        exclude_ip_range = ipaddress.ip_network(
                            mip_c['global_ip'] + '/' + mip_c['subnet_mask'])
                        exclude_ip_range_list += [exclude_ip_range]
                break
            elif dst_ip_list_c == '"Any"':
                continue
            else:
                continue
    return exclude_ip_range_list


def exclude_dst_ip_list_from_route_network(dst_ip_list, route_network):
    global network_address_list
    network_address_list = []
    add_dst_ip_list_to_subnet_mask(dst_ip_list)
    for exclude_ip_range in exclude_ip_range_list:
        if exclude_ip_range.subnet_of(route_network) is True:
            # route_networkと同一の場合は空が追加されてしまうため注意
            after_exclude_network = route_network.address_exclude(
                exclude_ip_range)
            network_address_list += after_exclude_network
        else:
            after_exclude_network = ipaddress.ip_network(route_network)
            network_address_list += [after_exclude_network]
    convert_network_address_to_scope_ip(network_address_list)
    exclude_fw_ip_from_scope_ip(scope_ip)


# Any Any ANY の前のポリシーで使われているIPをAnyのピックアップから除外するためのリストを作る
def handle_implicit_any_ip(policy):
    global network_address_list
    dst_ip_list = []
    for pre_policy in absorbdict.policy_dict:
        if policy['src_zone'] == pre_policy['src_zone'] and policy['dst_zone'] == pre_policy['dst_zone']:
            if len(absorbdict.group_address_dict) >= 2:
                flag = False
                for group_address_c in absorbdict.group_address_dict:
                    if pre_policy['dst_ip'] == group_address_c['group_name']:
                        flag = True
                        dst_ip_list += [group_address_c['address_name']]
                        continue
                else:
                    if not flag:
                        dst_ip_list += [pre_policy['dst_ip']]
            elif pre_policy['dst_ip'] == '"Any"':
                continue
            else:
                dst_ip_list += [pre_policy['dst_ip']]
            continue
        elif policy['policy_id'] == pre_policy['policy_id']:
            pass
    else:
        dst_zone = policy['dst_zone']
        # dst_zoneがif_zoneで使用されていないことも想定する
        # TODO:スキップしないようにする
        dst_if_route_network_range(policy, dst_zone)
        if dst_ip_list != []:
            exclude_dst_ip_list_from_route_network(dst_ip_list, route_network)
            define_scope_ip(policy, network_address_list)
        else:
            append_list = dst_ip
            data = str("NaN")
            print('%sから%sへのポリシーはpolicy_id = %sより前に存在しません' %
                  (policy['src_zone'], policy['dst_zone'], policy['policy_id']))
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)


def src_ip_element(policy, data, service_element_num):
    global dst_ip
    if policy['src_ip'] == '"Any"' and policy['src_zone'] != '"Untrust"':
        dst_ip += [data] * service_element_num * 2
    elif "VIP" in policy['src_ip'] and policy['protocol'] == '"ANY"':
        for vip_c in absorbdict.vip_dict:
            if policy['src_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
                dst_ip += [data] * service_element_num
            elif policy['src_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
                dst_ip += [data] * service_element_num
    else:
        src_address_name = policy['src_ip']
        judge_src_address_name(src_address_name)
        dst_ip += [data] * service_element_num * src_address_element_num


def handle_dst_ip_is_vip(policy, service_element_num):
    for vip_c in absorbdict.vip_dict:
        if policy['dst_ip'].strip(')"').split('(')[1] == vip_c['if_name']:
            if vip_c['global_ip'] == "interface-ip" and policy['protocol'] == '"ANY"':
                data = str(vip_c['private_ip'])
                src_ip_element(policy, data, service_element_num)
            else:
                handle_vip_dst_port(policy)
                break
        elif policy['dst_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
            if policy['protocol'] == '"ANY"':
                data = str(vip_c['private_ip'])
                src_ip_element(policy, data, service_element_num)
            else:
                handle_vip_dst_port(policy)
                break


def handle_vip_dst_port(policy):
    global dst_ip
    for service_c in absorbdict.service_dict:
        if policy.get('dst_nat_port') is not None:
            vip_dst_port = policy['dst_nat_port']
        elif policy['protocol'] == '"FTP"':
            vip_dst_port = '21'
        elif policy['protocol'] == '"HTTP"':
            vip_dst_port = '80'
        elif policy['protocol'] == '"NTP"':
            vip_dst_port = '123'
        elif policy['protocol'] == '"DNS"':
            vip_dst_port = '53'
        elif service_c['service_name'] == policy['protocol']:
            vip_dst_port = service_c['dst_port_num'].split('-')[0]
        else:
            continue
    else:
        decide_dst_vip_ip(policy, vip_dst_port)


def decide_dst_vip_ip(policy, vip_dst_port):
    for vip_c in absorbdict.vip_dict:
        if vip_dst_port == vip_c['port_num'] and policy['dst_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
            data = str(vip_c['private_ip'])
            src_ip_element(policy, data, service_element_num)
            break
        elif vip_dst_port == vip_c['port_num'] and policy['dst_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
            data = str(vip_c['private_ip'])
            src_ip_element(policy, data, service_element_num)
            break
    else:
        data = str("NaN")
        print('vipの設定をされたポートは現在対応していません')
        # print('詳しくはREADMEでご確認ください')
        print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
        src_ip_element(policy, data, service_element_num)


# groupで定義されたものか判定する関数
def judge_service_name(service_name):
    global service_element_num
    for group_service_c in absorbdict.group_service_dict:
        if group_service_c['group_service_name'] == service_name:
            group_service_name = group_service_c['group_service_name']
            multiple.count_group_service_element(group_service_name)
            service_element_num = multiple.service_element_num
            break
        else:
            service_element_num = 1
            continue
    else:
        return service_element_num


# groupで定義されたものか判定する関数
def judge_src_address_name(src_address_name):
    global src_address_element_num
    for group_address_c in absorbdict.group_address_dict:
        if group_address_c['group_name'] == src_address_name:
            group_name = group_address_c['group_name']
            multiple.count_src_group_address_element(group_name)
            src_address_element_num = multiple.src_address_element_num
            break
        else:
            src_address_element_num = 1
            continue
    else:
        return src_address_element_num


def handle_dst_ip_is_any(policy, dst_zone):
    confirm_dst_if(policy, dst_zone)
    scope_ip = ipaddress.ip_network("4.4.4.4/32")
    for route_c in absorbdict.route_dict:
        if dst_if.replace('"', '') == route_c['if_name'].replace('"', ''):
            if route_c['network_address'] == "0.0.0.0/0":
                continue
            elif ipaddress.IPv4Network(route_c['network_address']).num_addresses > ipaddress.IPv4Network(scope_ip).num_addresses:
                scope_ip = ipaddress.ip_network(
                    route_c['network_address'])
                continue
            else:
                continue
            exclude_fw_ip_from_scope_ip(scope_ip)
            define_scope_ip(policy, network_address_list)
            break
    else:
        for if_ip_c in absorbdict.if_ip_dict:
            if dst_if.replace('"', '') == if_ip_c['if_name'] and if_ip_c['ip_address'] is not None:
                if ipaddress.IPv4Network(if_ip_c['ip_address'], strict=False).num_addresses > ipaddress.IPv4Network(scope_ip).num_addresses:
                    scope_ip = ipaddress.ip_network(
                        if_ip_c['ip_address'], strict=False)
                    break
            else:
                continue
            exclude_fw_ip_from_scope_ip(scope_ip)
            define_scope_ip(policy, network_address_list)


def confirm_dst_if(policy, dst_zone):
    global dst_if
    for if_zone in absorbdict.if_zone_dict:
        if dst_zone == if_zone['zone_name']:
            dst_if = if_zone['if_name']
    return dst_if


def judge_dst_ip_is_group_address(policy, service_element_num):
    if len(absorbdict.group_address_dict) >= 2:
        for group_address_c in absorbdict.group_address_dict:
            if policy['dst_ip'] == group_address_c['group_name']:
                dst_address_name = group_address_c['address_name']
                for address_c in absorbdict.address_dict:
                    if dst_address_name == address_c['address_name']:
                        data = str(address_c['ip_address'])
                        src_ip_element(policy, data, service_element_num)
        else:
            address_dst_ip(policy, service_element_num)
    else:
        address_dst_ip(policy, service_element_num)


def address_dst_ip(policy, service_element_num):
    for address_c in absorbdict.address_dict:
        if policy['dst_ip'] == address_c['address_name']:
            try:
                ipaddress.ip_address(address_c['ip_address'])
            except ValueError:
                data = str("NaN")
                print('policy id = %sは宛先IPがIPではないため出力されませんでした' %
                      policy['policy_id'])
                src_ip_element(policy, data, service_element_num)
            else:
                data = str(address_c['ip_address'])
                src_ip_element(policy, data, service_element_num)
            break


def handle_mip_ip(policy, service_element_num):
    for mip_c in absorbdict.mip_dict:
        if policy['dst_ip'].strip(')"').split('(')[1] == mip_c['private_ip']:
            data = str(mip_c['global_ip'])
            src_ip_element(policy, data, service_element_num)
            break


def handle_dst_ip(policy, service_element_num):
    global dst_ip
    if policy.get('dst_nat_ip') is not None:
        data = str(policy['dst_nat_ip'])
        src_ip_element(policy, data, service_element_num)
    elif policy['dst_ip'] == '"Any"' and policy['dst_zone'] == '"Untrust"':
        data = str("8.8.8.8")
        src_ip_element(policy, data, service_element_num)
    elif policy['src_ip'] == '"Any"' and policy['dst_ip'] == '"Any"' and policy['protocol'] == '"ANY"':
        handle_implicit_any_ip(policy)
    elif policy['dst_ip'] == '"Any"':
        dst_zone = policy['dst_zone']
        handle_dst_ip_is_any(policy, dst_zone)
    elif "MIP" in policy['dst_ip']:
        handle_mip_ip(policy, service_element_num)
    elif "VIP" in policy['dst_ip']:
        handle_dst_ip_is_vip(policy, service_element_num)
    else:
        judge_dst_ip_is_group_address(policy, service_element_num)


def handle_multiple_element():
    global service_element_num
    global src_address_element_num
    for policy in absorbdict.policy_dict:
        # group_address & group_serviceが両方とも使用されている場合
        if len(absorbdict.group_address_dict) >= 2 and len(absorbdict.group_service_dict) >= 2:
            service_name = policy['protocol']
            src_address_name = policy['src_ip']
            judge_service_name(service_name)
            judge_src_address_name(src_address_name)
        # group_addressが使用されている場合
        elif len(absorbdict.group_address_dict) >= 2:
            service_element_num = 1
            src_address_name = policy['src_ip']
            judge_src_address_name(src_address_name)
        # group_serviceが使用されている場合
        elif len(absorbdict.group_service_dict) >= 2:
            service_name = policy['protocol']
            src_address_element_num = 1
            judge_service_name(service_name)
        # Group_dictがない場合
        else:
            service_element_num = src_address_element_num = 1
        handle_dst_ip(policy, service_element_num)


handle_multiple_element()
