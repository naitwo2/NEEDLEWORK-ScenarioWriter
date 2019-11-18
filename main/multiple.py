from main import absorbdict

# 送信元または宛先IPがAnyかつそのゾーンがUntrust以外の場合そのポリシーはリストに（Any*2）個追加する
# 送信元または宛先IPがVIPかつプロトコルがANYの場合そのポリシーはリストに（該当するVIP）個追加する
# TODO:group_addressのaddress_nameにgroup_address,group_service_nameのservice_nameにgroup_service_nameは別途対応する


service_element_num = src_address_element_num = dst_address_element_num = 1


# group_serviceをgroupで束ねていた場合はgroup_service以下の要素数までは確認しない
def count_group_service_element(group_service_name):
    global service_element_num
    service_element_num = 0
    for group_service_c in absorbdict.group_service_dict:
        if group_service_name == group_service_c['group_service_name']:
            service_element_name = group_service_c['service_name']
            flag = False
            for group_service2_c in absorbdict.group_service_dict:
                if service_element_name == group_service2_c['group_service_name']:
                    flag = True
            else:
                if flag:
                    service_element_num = 1
                else:
                    flag = False
                    for service_c in absorbdict.service_dict:
                        if service_element_name == service_c['service_name']:
                            d = service_c
                            service_element_num += 1
                            flag = True
                    else:
                        if not flag:
                            d = group_service_c
                            service_element_num += list(d.values()
                                                        ).count(group_service_name)
    else:
        return service_element_num


def count_src_group_address_element(group_name):
    global src_address_element_num
    src_address_element_num = 0
    for group_address_c in absorbdict.group_address_dict:
        if group_name == group_address_c['group_name']:
            address_element_name = group_address_c['address_name']
            flag = False
            for group_address2_c in absorbdict.group_address_dict:
                if address_element_name == group_address2_c['group_name']:
                    flag = True
            else:
                if flag:
                    src_address_element_num = 1
                else:
                    flag = False
                    for address_c in absorbdict.address_dict:
                        if address_element_name == address_c['address_name']:
                            d = address_c
                            src_address_element_num += 1
                            flag = True
                    else:
                        if not flag:
                            d = group_address_c
                            src_address_element_num += list(
                                d.values()).count(group_name)
    else:
        return src_address_element_num


def count_dst_group_address_element(group_name):
    global dst_address_element_num
    dst_address_element_num = 0
    for group_address_c in absorbdict.group_address_dict:
        if group_name == group_address_c['group_name']:
            address_element_name = group_address_c['address_name']
            flag = False
            for group_address2_c in absorbdict.group_address_dict:
                if address_element_name == group_address2_c['group_name']:
                    flag = True
            else:
                if flag:
                    dst_address_element_num = 1
                else:
                    flag = False
                    for address_c in absorbdict.address_dict:
                        if address_element_name == address_c['address_name']:
                            d = address_c
                            dst_address_element_num += 1
                            flag = True
                    else:
                        if not flag:
                            d = group_address_c
                            dst_address_element_num += list(
                                d.values()).count(group_name)
    else:
        return dst_address_element_num


def judge_service_name(service_name):
    global service_element_num
    for group_service_c in absorbdict.group_service_dict:
        if group_service_c['group_service_name'] == service_name:
            group_service_name = group_service_c['group_service_name']
            count_group_service_element(group_service_name)
            break
        else:
            service_element_num = 1
            continue
    else:
        return service_element_num


def judge_src_address_name(address_name):
    global src_address_element_num
    for group_address_c in absorbdict.group_address_dict:
        if group_address_c['group_name'] == address_name:
            group_name = group_address_c['group_name']
            count_src_group_address_element(group_name)
            break
        else:
            src_address_element_num = 1
            continue
    else:
        return src_address_element_num


def judge_dst_address_name(address_name):
    global dst_address_element_num
    for group_address_c in absorbdict.group_address_dict:
        if group_address_c['group_name'] == address_name:
            group_name = group_address_c['group_name']
            count_dst_group_address_element(group_name)
            break
        else:
            dst_address_element_num = 1
            continue
    else:
        return dst_address_element_num


def handle_multiple_only_dst_ip(policy, append_list, data):
    if policy['dst_ip'] == '"Any"' and policy['dst_zone'] != '"Untrust"':
        append_list += [data] * service_element_num * 2
    elif "VIP" in policy['dst_ip'] and policy['protocol'] == '"ANY"':
        for vip_c in absorbdict.vip_dict:
            if policy['dst_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
                append_list += [data] * service_element_num
            elif policy['dst_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
                append_list += [data] * service_element_num
    else:
        for group_address_c in absorbdict.group_address_dict:
            if policy['dst_ip'] == group_address_c['group_name']:
                group_name = group_address_c['group_name']
                count_dst_group_address_element(group_name)
                append_list += [data] * service_element_num * \
                    dst_address_element_num
                break
        else:
            append_list += [data] * service_element_num


def handle_multiple_element(policy, append_list, data):
    if policy['src_ip'] == '"Any"' and policy['src_zone'] != '"Untrust"':
        handle_multiple_only_dst_ip(policy, append_list, data)
        handle_multiple_only_dst_ip(policy, append_list, data)
    elif "VIP" in policy['src_ip'] and policy['protocol'] == '"ANY"':
        for vip_c in absorbdict.vip_dict:
            if policy['src_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
                handle_multiple_only_dst_ip(policy, append_list, data)
            elif policy['src_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
                handle_multiple_only_dst_ip(policy, append_list, data)
    else:
        handle_multiple_only_dst_ip(policy, append_list, data)


def handle_multiple_group_ip(policy, append_list, data):
    if policy['src_ip'] == '"Any"' and policy['src_zone'] != '"Untrust"':
        handle_multiple_only_dst_ip(policy, append_list, data)
        handle_multiple_only_dst_ip(policy, append_list, data)
    elif "VIP" in policy['src_ip'] and policy['protocol'] == '"ANY"':
        for vip_c in absorbdict.vip_dict:
            if policy['src_ip'].strip(')"').split('(')[1] == vip_c['if_name'] and vip_c['global_ip'] == "interface-ip":
                handle_multiple_only_dst_ip(policy, append_list, data)
            elif policy['src_ip'].strip(')"').split('(')[1] == vip_c['global_ip']:
                handle_multiple_only_dst_ip(policy, append_list, data)
    else:
        flag = False
        for group_address_c in absorbdict.group_address_dict:
            if policy['src_ip'] == group_address_c['group_name']:
                flag = True
                flags = False
                for group_address2_c in absorbdict.group_address_dict:
                    if policy['dst_ip'] == group_address2_c['group_name']:
                        flags = True
                        append_list += [data] * service_element_num
                else:
                    if not flags:
                        handle_multiple_only_dst_ip(policy, append_list, data)
            else:
                continue
        else:
            if not flag:
                handle_multiple_only_dst_ip(policy, append_list, data)


def handle_multiple_ip(policy, append_list, data):
    # group_address & group_serviceが両方とも使用されている場合
    global service_element_num
    global src_address_element_num, dst_address_element_num
    if len(absorbdict.group_address_dict) >= 2 and len(absorbdict.group_service_dict) >= 2:
        service_name = policy['protocol']
        # src_address = policy['src_ip']
        # dst_address = policy['dst_ip']
        judge_service_name(service_name)
        # judge_src_address_name(src_address), judge_dst_address_name(dst_address)
        handle_multiple_group_ip(policy, append_list, data)
    # group_addressが使用されている場合
    elif len(absorbdict.group_address_dict) >= 2:
        service_element_num = 1
        handle_multiple_group_ip(policy, append_list, data)
    # group_serviceが使用されている場合
    elif len(absorbdict.group_service_dict) >= 2:
        service_name = policy['protocol']
        judge_service_name(service_name)
        handle_multiple_element(policy, append_list, data)
    # Group_dictがない場合
    else:
        service_element_num = 1
        handle_multiple_element(policy, append_list, data)
