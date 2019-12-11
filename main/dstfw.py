import ipaddress

from main import absorbdict
from main import multiple

dst_fw = []

# dst-fwのリストの生成


def decide_dst_fw(policy, append_list, dst_if):
    for if_ip_c in absorbdict.if_ip_dict:
        if dst_if.replace('"', '') == if_ip_c['if_name'].replace('"', ''):
            data = str(
                if_ip_c['ip_address'].split('/')[0])
            multiple.handle_multiple_ip(
                policy, append_list, data)


def handle_dst_fw():
    global dst_fw
    append_list = dst_fw
    for policy in absorbdict.policy_dict:
        for if_zone_c in absorbdict.if_zone_dict:
            if policy.get('dst_nat_ip') is not None:
                longest_match = {}
                for if_ip_c in absorbdict.route_dict:
                    if ipaddress.ip_address(policy['dst_nat_ip']) in ipaddress.ip_network(if_ip_c['network_address'], strict=False):
                        a = {if_ip_c['if_name']: if_ip_c['network_address'].split('/')[1]}
                        longest_match.update(a)
                        max_keys = max(longest_match, key=longest_match.get)
                    else:
                        continue
                dst_if = max_keys
                decide_dst_fw(policy, append_list, dst_if)
                break
            elif "VIP" in policy['dst_ip']:
                for vip_c in absorbdict.vip_dict:
                    if policy['dst_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
                        longest_match = {}
                        for if_ip_c in absorbdict.route_dict:
                            if ipaddress.ip_address(vip_c['private_ip']) in ipaddress.ip_network(if_ip_c['network_address'], strict=False):
                                a = {
                                    if_ip_c['if_name']: if_ip_c['network_address'].split('/')[1]}
                                longest_match.update(a)
                            else:
                                continue
                        max_keys = max(longest_match, key=longest_match.get)
                        dst_if = max_keys
                        decide_dst_fw(policy, append_list, dst_if)
                        break
                    elif policy['dst_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
                        dst_if = policy['dst_ip'].strip(')"').split('(')[1]
                        decide_dst_fw(policy, append_list, dst_if)
                        break
                break
            elif policy['dst_zone'] == if_zone_c['zone_name']:
                dst_if = if_zone_c['if_name']
                decide_dst_fw(policy, append_list, dst_if)


handle_dst_fw()
