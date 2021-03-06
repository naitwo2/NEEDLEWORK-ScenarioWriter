from main import absorbdict
import ipaddress

from main import multiple

src_nat_ip = []

# src-nat-ipのリストの生成


def handle_src_nat_ip():
    global src_nat_ip
    append_list = src_nat_ip
    for policy in absorbdict.policy_dict:
        if policy.get('src') is not None and policy.get('src_nat_ip') is not None:
            data = str(policy['src_nat_ip'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy.get('src') is not None and policy.get('dip_num') is not None:
            for dip_c in absorbdict.dip_dict:
                if policy.get('dip_num') == dip_c['dip_num']:
                    data = str(dip_c['start_ip'])
                    multiple.handle_multiple_ip(policy, append_list, data)
        elif policy.get('src') is not None:
            if policy.get('dst') is not None:
                address = str(policy['dst_nat_ip'])
                ip_network = ipaddress.ip_network(
                    ipaddress.ip_address(address), strict=False)
                for route_c in absorbdict.route_dict:
                    routing_network = ipaddress.ip_network(
                        route_c['network_address'])
                    if ip_network.subnet_of(routing_network) is True:
                        after_dst_if = route_c['if_name']
                        for if_ip_c in absorbdict.if_ip_dict:
                            if after_dst_if.replace('"', '') == if_ip_c['if_name'].replace('"', '') and if_ip_c.get('ip_address') is not None:
                                dst_fw = if_ip_c['ip_address'].split('/')[0]
                                data = str(dst_fw)
                                multiple.handle_multiple_ip(
                                    policy, append_list, data)
            else:
                flag = False
                for if_zone in absorbdict.if_zone_dict:
                    if policy['dst_zone'] == if_zone['zone_name']:
                        dst_if = if_zone['if_name']
                        for if_ip_c in absorbdict.if_ip_dict:
                            if dst_if.replace('"', '') == if_ip_c['if_name'].replace('"', '') and if_ip_c.get('ip_address') is not None:
                                flag = True
                                dst_fw = if_ip_c['ip_address'].split('/')[0]
                                data = str(dst_fw)
                                multiple.handle_multiple_ip(
                                    policy, append_list, data)
        else:
            flag = False
            for if_zone in absorbdict.if_zone_dict:
                if policy['src_zone'] == if_zone['zone_name']:
                    src_if = if_zone['if_name']
                    for if_nat_c in absorbdict.if_nat_dict:
                        if src_if.replace('"', '') == if_nat_c['if_name'].replace('"', ''):
                            flag = True
                            for if_zone in absorbdict.if_zone_dict:
                                if policy['dst_zone'] == if_zone['zone_name']:
                                    dst_if = if_zone['if_name']
                                    for if_ip_c in absorbdict.if_ip_dict:
                                        if dst_if.replace('"', '') == if_ip_c['if_name'].replace('"', ''):
                                            dst_fw = if_ip_c['ip_address'].split(
                                                '/')[0]
                                            data = str(dst_fw)
                                            multiple.handle_multiple_ip(
                                                policy, append_list, data)
                    else:
                        # TODO:要修正
                        if policy['protocol'] == '"NTP"' or policy['protocol'] == '"HTTP"':
                            for address_c in absorbdict.address_dict:
                                if policy['src_ip'].replace('"', '') == address_c['address_name'].replace('"', ''):
                                    ip_address = address_c['ip_address']
                                    for mip_c in absorbdict.mip_dict:
                                        if ip_address == mip_c['global_ip']:
                                            flag = True
                                            data = str(mip_c['private_ip'])
                                            multiple.handle_multiple_ip(
                                                policy, append_list, data)
            else:
                if not flag:
                    data = str("")
                    multiple.handle_multiple_ip(policy, append_list, data)


handle_src_nat_ip()
