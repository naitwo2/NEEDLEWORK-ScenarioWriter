import ipaddress

from main import absorbdict
from main import multiple

src_ip = []

# src-ipのリストの生成

service_element_num = 1
dst_address_element_num = 1


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


def select_dst_ip_from_scope_ip(policy, scope_ip, service_element_num):
    global src_ip
    if policy['dst_ip'] == '"Any"' and policy['dst_zone'] != '"Untrust"':
        src_ip += [str(scope_ip[1]), str(scope_ip[-2]),
                   str(scope_ip[-2]), str(scope_ip[1])] * service_element_num
    elif "VIP" in policy['dst_ip'] and policy['protocol'] == '"ANY"':
        for vip_c in absorbdict.vip_dict:
            if policy['dst_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
                src_ip += [str(scope_ip[1]), str(scope_ip[-2])
                           ] * service_element_num
            elif policy['dst_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
                src_ip += [str(scope_ip[1]), str(scope_ip[-2])
                           ] * service_element_num
    else:
        dst_address_name = policy['dst_ip']
        judge_dst_address_name(dst_address_name)
        src_ip += [str(scope_ip[1]), str(scope_ip[-2])] * \
            service_element_num * dst_address_element_num


def handle_network_address_src(policy, scope_ip):
    global src_ip
    # group_serviceに対応する
    if len(absorbdict.group_service_dict) >= 2:
        for group_service_c in absorbdict.group_service_dict:
            if group_service_c['group_service_name'] == policy['protocol']:
                group_service_name = group_service_c['group_service_name']
                multiple.count_group_service_element(group_service_name)
                service_element_num = multiple.service_element_num
                select_dst_ip_from_scope_ip(
                    policy, scope_ip, service_element_num)
                break
        else:
            service_element_num = 1
            select_dst_ip_from_scope_ip(
                policy, scope_ip, service_element_num)
    else:
        # group_Serviceが使用されていない
        service_element_num = 1
        select_dst_ip_from_scope_ip(policy, scope_ip, service_element_num)


def src_if_if_network_range(src_if):
    global route_network
    for if_ip_c in absorbdict.if_ip_dict:
        route_network = ipaddress.ip_network("2.3.4.5/32")
        if src_if.replace('"', '') == if_ip_c['if_name'] and if_ip_c['ip_address'] is not None:
            if ipaddress.IPv4Network(if_ip_c['ip_address'], strict=False).num_addresses > ipaddress.IPv4Network(route_network, strict=False).num_addresses:
                route_network = ipaddress.ip_network(
                    if_ip_c['ip_address'], strict=False)
            return route_network


def src_if_route_network_range(src_zone):
    global route_network
    for if_zone in absorbdict.if_zone_dict:
        if src_zone == if_zone['zone_name']:
            src_if = if_zone['if_name']
            route_network = ipaddress.ip_network("1.2.3.4/32")
            for route_c in absorbdict.route_dict:
                if src_if.replace('"', '') == route_c['if_name'].replace('"', ''):
                    if ipaddress.IPv4Network(route_c['network_address']) == "0.0.0.0/0":
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
                    if src_if.replace('"', '') == if_ip_c['if_name'] and if_ip_c.get('ip_address') is not None:
                        src_if_if_network_range(src_if)
                        break
                    else:
                        continue
                continue
            break


def convert_network_address_to_scope_ip(network_address_list):
    global scope_ip
    scope_ip = ipaddress.ip_network("2.2.2.2/32")
    for item in network_address_list:
        if ipaddress.IPv4Network(item).num_addresses > ipaddress.IPv4Network(scope_ip).num_addresses:
            scope_ip = item
    return scope_ip


def define_scope_ip(policy, network_address_list):
    convert_network_address_to_scope_ip(network_address_list)
    handle_network_address_src(policy, scope_ip)


def confirm_fw_ip():
    global fw_ip
    fw_ip = []
    for if_ip_c in absorbdict.if_ip_dict:
        fw_ip += [ipaddress.ip_network(if_ip_c['ip_address'].split('/')[0])]
    return fw_ip


# TODO:これだと除外したとこ以外のレンジに含まれていたらアウト
def exclude_fw_ip_from_scope_ip(scope_ip):
    global network_address_list
    network_address_list = []
    confirm_fw_ip()
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


# TODO:network_address_listからfw_ipを外す
def exclude_network_range(src_ip_list, route_network):
    global network_address_list
    network_address_list = []
    # TODO:route_networkをhandle_dst_ip_is_anyを参考に持ってくる
    for src_ip_list_c in src_ip_list:
        for address_c in absorbdict.address_dict:
            if src_ip_list_c == address_c['address_name'] and address_c.get('subnet_mask') is not None:
                exclude_ip_range = ipaddress.ip_network(
                    address_c['ip_address'] + '/' + address_c['subnet_mask'])
                if exclude_ip_range.subnet_of(route_network) is True:
                    # route_networkと同一の場合は空になってしまうため注意
                    after_exclude_network = route_network.address_exclude(
                        exclude_ip_range)
                    network_address_list += after_exclude_network
                else:
                    after_exclude_network = ipaddress.ip_network(route_network)
                    network_address_list += [after_exclude_network]
            elif "MIP" in src_ip_list_c:
                for mip_c in absorbdict.mip_dict:
                    if src_ip_list_c.strip(')"').split('(')[1] == mip_c['private_ip']:
                        exclude_ip_range = ipaddress.ip_network(
                            mip_c['global_ip'] + '/' + mip_c['subnet_mask'])
                        if exclude_ip_range.subnet_of(route_network) is True:
                            after_exclude_network = route_network.address_exclude(
                                exclude_ip_range)
                            network_address_list += after_exclude_network
                        else:
                            after_exclude_network = ipaddress.ip_network(
                                exclude_ip_range)
                            network_address_list += [after_exclude_network]
            elif src_ip_list_c == '"Any"':
                continue
            else:
                continue
            break
    convert_network_address_to_scope_ip(network_address_list)
    exclude_fw_ip_from_scope_ip(scope_ip)


def handle_implicit_any_ip(policy):
    global network_address_list
    src_ip_list = []
    for pre_policy in absorbdict.policy_dict:
        if policy['src_zone'] == pre_policy['src_zone'] and policy['dst_zone'] == pre_policy['dst_zone']:
            if len(absorbdict.group_address_dict) >= 2:
                flag = False
                for group_address_c in absorbdict.group_address_dict:
                    if pre_policy['src_ip'] == group_address_c['group_name']:
                        flag = True
                        src_ip_list += [group_address_c['address_name']]
                        continue
                else:
                    if not flag:
                        src_ip_list += [pre_policy['src_ip']]
            elif pre_policy['src_ip'] == '"Any"':
                continue
            else:
                src_ip_list += [pre_policy['src_ip']]
            continue
        elif policy['policy_id'] == pre_policy['policy_id']:
            pass
    else:
        src_zone = policy['src_zone']
        # src_zoneがif_zoneで使用されていないこと(route_networkが返ってこないこと)も想定する
        src_if_route_network_range(src_zone)
        if src_ip_list != []:
            exclude_network_range(src_ip_list, route_network)
            define_scope_ip(policy, network_address_list)
        else:
            append_list = src_ip
            data = str("NaN")
            print(policy['src_zone'] + 'から' + policy['dst_zone'] +
                  'へのポリシーは' + 'policy_id =' + policy['policy_id'] + 'より前に存在しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)


def dst_ip_element(policy, data, service_element_num):
    global src_ip
    if policy['dst_ip'] == '"Any"' and policy['dst_zone'] != '"Untrust"':
        src_ip += [data] * service_element_num * 2
    elif "VIP" in policy['dst_ip'] and policy['protocol'] == '"ANY"':
        for vip_c in absorbdict.vip_dict:
            if policy['dst_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
                src_ip += [data] * service_element_num
            elif policy['dst_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
                src_ip += [data] * service_element_num
    else:
        for group_address_c in absorbdict.group_address_dict:
            if policy['dst_ip'] == group_address_c['group_name']:
                group_name = group_address_c['group_name']
                multiple.count_dst_group_address_element(group_name)
                dst_address_element_num = multiple.dst_address_element_num
                src_ip += [data] * service_element_num * \
                    dst_address_element_num
                break
        else:
            src_ip += [data] * service_element_num


def multiple_dst_ip(policy, data):
    global service_element_num
    if len(absorbdict.group_service_dict) >= 2:
        service_name = policy['protocol']
        judge_service_name(service_name)
        global service_element_num
    else:
        service_element_num = 1
    dst_ip_element(policy, data, service_element_num)


def handle_vip_src_port(policy):
    global src_ip
    for service_c in absorbdict.service_dict:
        if policy['protocol'] == '"FTP"':
            vip_src_port = '21'
        elif policy['protocol'] == '"HTTP"':
            vip_src_port = '80'
        elif policy['protocol'] == '"NTP"':
            vip_src_port = '123'
        elif policy['protocol'] == '"DNS"':
            vip_src_port = '53'
        elif service_c['service_name'] == policy['protocol'] and service_c['protocol_name']:
            vip_src_port = service_c['src_port_num'].split('-')[0]
        else:
            continue
    else:
        decide_src_vip_ip(policy, vip_src_port)


def decide_src_vip_ip(policy, vip_src_port):
    for vip_c in absorbdict.vip_dict:
        if vip_src_port == vip_c['port_num'] and policy['src_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
            data = str(vip_c['private_ip'])
            multiple_dst_ip(policy, data)
            break
        elif vip_src_port == vip_c['port_num'] and policy['src_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
            data = str(vip_c['private_ip'])
            multiple_dst_ip(policy, data)
            break
    else:
        data = str("NaN")
        print('vipの設定をされたポートは現在対応していません')
        # print('詳しくはREAD.MEでご確認ください')
        print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
        multiple_dst_ip(policy, data)


def judge_dst_address_name(dst_address_name):
    global dst_address_element_num
    for group_address_c in absorbdict.group_address_dict:
        if group_address_c['group_name'] == dst_address_name:
            group_name = group_address_c['group_name']
            multiple.count_dst_group_address_element(group_name)
            dst_address_element_num = multiple.dst_address_element_num
            break
        else:
            continue
    else:
        return dst_address_element_num


def handle_src_ip_is_any(policy, src_zone):
    for if_zone in absorbdict.if_zone_dict:
        if src_zone == if_zone['zone_name']:
            src_if = if_zone['if_name']
            scope_ip = ipaddress.ip_network("4.4.4.4/32")
            for route_c in absorbdict.route_dict:
                if src_if.replace('"', '') == route_c['if_name'].replace('"', ''):
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
                    if src_if.replace('"', '') == if_ip_c['if_name'] and if_ip_c['ip_address'] is not None:
                        if ipaddress.IPv4Network(if_ip_c['ip_address'], strict=False).num_addresses > ipaddress.IPv4Network(scope_ip).num_addresses:
                            scope_ip = ipaddress.ip_network(
                                if_ip_c['ip_address'], strict=False)
                            break
                    else:
                        continue
                    exclude_fw_ip_from_scope_ip(scope_ip)
                    define_scope_ip(policy, network_address_list)
                continue
            break


def address_src_ip(policy, service_element_num):
    for address_c in absorbdict.address_dict:
        if policy['src_ip'] == address_c['address_name']:
            try:
                ipaddress.ip_address(address_c['ip_address'])
            except ValueError:
                data = str("NaN")
                print('policy id = ' +
                      policy['policy_id'] + 'は送信元IPがIPではないため出力されませんでした')
                multiple_dst_ip(policy, data)
            else:
                data = str(address_c['ip_address'])
                multiple_dst_ip(policy, data)
            break


def handle_src_ip_is_vip(policy, service_element_num):
    for vip_c in absorbdict.vip_dict:
        if policy['src_ip'].strip(')"').split('(')[1] == vip_c['if_name']:
            if vip_c['global_ip'] == "interface-ip" and policy['protocol'] == '"ANY"':
                data = str(vip_c['private_ip'])
                multiple_dst_ip(policy, data)
            else:
                handle_vip_src_port(policy)
                break
        elif policy['src_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
            if policy['protocol'] == '"ANY"':
                data = str(vip_c['private_ip'])
                multiple_dst_ip(policy, data)
            else:
                handle_vip_src_port(policy)
                break


def judge_src_ip_is_group_address(policy, service_element_num):
    if len(absorbdict.group_address_dict) >= 2:
        for group_address_c in absorbdict.group_address_dict:
            if policy['src_ip'] == group_address_c['group_name']:
                src_address_name = group_address_c['address_name']
                for address_c in absorbdict.address_dict:
                    if src_address_name == address_c['address_name']:
                        data = str(address_c['ip_address'])
                        multiple_dst_ip(policy, data)
        else:
            address_src_ip(policy, service_element_num)
    else:
        address_src_ip(policy, service_element_num)


def handle_mip_ip(policy, service_element_num):
    for mip_c in absorbdict.mip_dict:
        if policy['dst_ip'].strip(')"').split('(')[1] == mip_c['private_ip']:
            data = str(mip_c['global_ip'])
            dst_ip_element(policy, data, service_element_num)
            break


def handle_src_ip(policy, service_element_num):
    global src_ip
    if policy.get('src_nat_ip') is not None:
        data = str(policy['src_nat_ip'])
        multiple_dst_ip(policy, data)
    elif policy['src_ip'] == '"Any"' and policy['src_zone'] == '"Untrust"':
        data = str("8.8.8.8")
        multiple_dst_ip(policy, data)
    elif policy['src_ip'] == policy['dst_ip'] == '"Any"' and policy['protocol'] == '"ANY"':
        handle_implicit_any_ip(policy)
    elif policy['src_ip'] == '"Any"':
        src_zone = policy['src_zone']
        handle_src_ip_is_any(policy, src_zone)
    elif "MIP" in policy['src_ip']:
        handle_mip_ip(policy, service_element_num)
    elif "VIP" in policy['src_ip']:
        handle_src_ip_is_vip(policy, service_element_num)
    else:
        judge_src_ip_is_group_address(policy, service_element_num)


def handle_multiple_element():
    global service_element_num
    global dst_address_element_num
    for policy in absorbdict.policy_dict:
        # group_address & group_serviceが両方とも使用されている場合
        if len(absorbdict.group_address_dict) >= 2 and len(absorbdict.group_service_dict) >= 2:
            service_name = policy['protocol']
            dst_address_name = policy['dst_ip']
            judge_service_name(service_name)
            judge_dst_address_name(dst_address_name)
        # group_addressが使用されている場合
        elif len(absorbdict.group_address_dict) >= 2:
            service_element_num = 1
            dst_address_name = policy['dst_ip']
            judge_dst_address_name(dst_address_name)
        # group_serviceが使用されている場合
        elif len(absorbdict.group_service_dict) >= 2:
            service_name = policy['protocol']
            dst_address_element_num = 1
            judge_service_name(service_name)
        # Group_dictがない場合
        else:
            service_element_num = dst_address_element_num = 1
        handle_src_ip(policy, service_element_num)


handle_multiple_element()

print(len(src_ip))
print(src_ip)
