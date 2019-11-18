import ipaddress

from main import absorbdict
from main import multiple

src_fw = []

# src-fwのリストの生成


def handle_src_fw():
    global src_fw
    append_list = src_fw
    for policy in absorbdict.policy_dict:
        for if_zone in absorbdict.if_zone_dict:
            if "VIP" in policy['src_ip']:
                for vip_c in absorbdict.vip_dict:
                    if policy['src_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
                        longest_match = {}
                        for if_ip_c in absorbdict.route_dict:
                            if ipaddress.ip_address(vip_c['private_ip']) in ipaddress.ip_network(if_ip_c['network_address'], strict=False):
                                a = {
                                    if_ip_c['if_name']: if_ip_c['network_address'].split('/')[1]}
                                longest_match.update(a)
                            else:
                                continue
                        max_keys = max(longest_match, key=longest_match.get)
                        src_if = []
                        src_if += [max_keys]
                        for src_if_c in src_if:
                            for if_ip_c in absorbdict.if_ip_dict:
                                if src_if_c.replace('"', '') == if_ip_c['if_name'].replace('"', ''):
                                    data = str(
                                        if_ip_c['ip_address'].split('/')[0])
                                    multiple.handle_multiple_ip(
                                        policy, append_list, data)
                                    break
                    elif policy['src_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
                        src_if = []
                        src_if += [policy['src_ip'].strip(')"').split('(')[1]]
                        for src_if_c in src_if:
                            for if_ip_c in absorbdict.if_ip_dict:
                                if src_if_c.replace('"', '') == if_ip_c['if_name'].replace('"', ''):
                                    data = str(
                                        if_ip_c['ip_address'].split('/')[0])
                                    multiple.handle_multiple_ip(
                                        policy, append_list, data)
                                    break
                        break
                break
            elif policy['src_zone'] == if_zone['zone_name']:
                src_if = []
                src_if += [if_zone['if_name']]
                for src_if_c in src_if:
                    for if_ip_c in absorbdict.if_ip_dict:
                        if src_if_c.replace('"', '') == if_ip_c['if_name'].replace('"', ''):
                            data = str(if_ip_c['ip_address'].split('/')[0])
                            multiple.handle_multiple_ip(
                                policy, append_list, data)
                            break
                        else:
                            flag = False
                            for if_zone in absorbdict.if_zone_dict:
                                if policy['src_zone'] == if_zone['zone_name']:
                                    flag = True
                                    break
                                else:
                                    continue
            else:
                flag = False
                for if_zone in absorbdict.if_zone_dict:
                    if policy['src_zone'] == if_zone['zone_name']:
                        flag = True
                        break
                    else:
                        continue
        else:
            if not flag:
                data = str("NaN")
                print('送信元ゾーンの' + policy['dst_zone'] +
                      'が割り当てられたIF,またはそのIFにIPがありません')
                print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
                multiple.handle_multiple_ip(policy, append_list, data)


handle_src_fw()
