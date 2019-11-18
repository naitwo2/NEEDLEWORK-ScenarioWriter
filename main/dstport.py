from main import absorbdict

from main import multiple

dst_port_icmp = []
dst_port_tcp = []
dst_port_udp = []

# dst-portのリストの生成


def handle_dst_port_icmp():
    global dst_port_icmp
    append_list = dst_port_icmp
    for policy in absorbdict.policy_dict:
        if policy.get('dst_nat_port') is not None:
            data = str(policy['dst_nat_port'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"PING"':
            data = str("")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"SMTP"':
            data = str("NaN")
            print('"SMTP"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"SNMP"':
            data = str("NaN")
            print('"SNMP"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"NBDS"':
            data = str("NaN")
            print('"NBDS"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"FTP"':
            data = str("NaN")
            print('"FTP"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"HTTP"':
            data = str("NaN")
            print('"HTTP"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"HTTPS"':
            data = str("NaN")
            print('"HTTPS"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"NTP"':
            data = str("NaN")
            print('"NTP"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"SYSLOG"':
            data = str("NaN")
            print('"SYSLOG"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"DNS"':
            data = str("NaN")
            print('"DNS"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"MAIL"':
            data = str("NaN")
            print('"MAIL"はicmpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"ANY"':
            # icmpはdstportが存在しない
            data = str("")
            multiple.handle_multiple_ip(policy, append_list, data)
        else:
            for service_c in absorbdict.service_dict:
                if service_c['service_name'] == policy['protocol'] and service_c['protocol_name'] == "icmp":
                    data = str(service_c['dst_port_num'].split('-')[1])
                    multiple.handle_multiple_ip(policy, append_list, data)
                    break
                else:
                    continue
            else:
                if len(absorbdict.group_service_dict) >= 2:
                    service_name = []
                    for group_service_c in absorbdict.group_service_dict:
                        if group_service_c['group_service_name'] == policy['protocol']:
                            service_name += group_service_c['service_name']
                            for service_c in absorbdict.service_dict:
                                if service_c['service_name'] == service_name and service_c['protocol_name'] == "icmp":
                                    data = str(
                                        service_c['dst_port_num'].split('-')[1])
                                    multiple.handle_multiple_ip(
                                        policy, append_list, data)
                                    break
                            else:
                                # TODO:最初のservice_nameにICMPが使用されていなければデフォが入ってしまい次以降でデフォが使用されていると異なる挙動となる
                                data = str("")
                                multiple.handle_multiple_ip(
                                    policy, append_list, data)
                            break
                    else:
                        data = str("NaN")
                        print('service_nameでicmpが使用されていないため出力しませんでした')
                        print('policy_id = %sの出力をスキップしました' %
                              policy['policy_id'])
                        multiple.handle_multiple_ip(policy, append_list, data)
                else:
                    data = str("NaN")
                    print('service_nameでicmpが使用されていないため出力しませんでした')
                    print('policy_id = %sの出力をスキップしました' %
                            policy['policy_id'])
                    multiple.handle_multiple_ip(policy, append_list, data)


handle_dst_port_icmp()


def handle_dst_port_tcp():
    global dst_port_tcp
    append_list = dst_port_tcp
    for policy in absorbdict.policy_dict:
        if policy.get('dst_nat_port') is not None:
            data = str(policy['dst_nat_port'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"SMTP"':
            data = str("25")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"SNMP"':
            data = str("161")  # 162
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"NBDS"':
            data = str("NaN")
            print('"NBDS"はtcpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"FTP"':
            data = str("21")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"HTTP"':
            data = str("80")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"HTTPS"':
            data = str("443")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"NTP"':
            data = str("123")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"SYSLOG"':
            data = str("NaN")
            print('"SYSLOG"はtcpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"DNS"':
            data = str("53")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"MAIL"':
            data = str("25")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"PING"':
            data = str("NaN")
            print('"PING"はtcpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"ANY"':
            # TODO:Any Any ANYの時の処理を変更する
            if policy['src_ip'] == policy['dst_ip'] == '"Any"':
                # 要修正
                data = str("65535")
                multiple.handle_multiple_ip(policy, append_list, data)
            else:
                data = str("80")
                multiple.handle_multiple_ip(policy, append_list, data)
        else:
            for service_c in absorbdict.service_dict:
                if service_c['service_name'] == policy['protocol'] and service_c['protocol_name'] == 'tcp':
                    data = str(service_c['dst_port_num'].split('-')[1])
                    multiple.handle_multiple_ip(policy, append_list, data)
                    break
            else:
                if len(absorbdict.group_service_dict) >= 2:
                    for group_service_c in absorbdict.group_service_dict:
                        if group_service_c['group_service_name'] == policy['protocol']:
                            service_name = group_service_c['service_name']
                            for service_c in absorbdict.service_dict:
                                if service_c['service_name'] == service_name and service_c['protocol_name'] == "tcp":
                                    data = str(
                                        service_c['dst_port_num'].split('-')[1])
                                    multiple.handle_multiple_ip(
                                        policy, append_list, data)
                                    break
                            else:
                                # TODO:最初のservice_nameにTCPが使用されていなければデフォが入ってしまい次以降でデフォが使用されていると異なる挙動となる
                                data = str("80")
                                multiple.handle_multiple_ip(
                                    policy, append_list, data)
                            break
                    else:
                        data = str("NaN")
                        print('service_nameでtcpが使用されていないため出力しませんでした')
                        print('policy_id = %sの出力をスキップしました' %
                              policy['policy_id'])
                        multiple.handle_multiple_ip(policy, append_list, data)
                else:
                    data = str("NaN")
                    print('service_nameでtcpが使用されていないため出力しませんでした')
                    print('policy_id = %sの出力をスキップしました' %
                            policy['policy_id'])
                    multiple.handle_multiple_ip(policy, append_list, data)


handle_dst_port_tcp()


def handle_dst_port_udp():
    global dst_port_udp
    append_list = dst_port_udp
    for policy in absorbdict.policy_dict:
        if policy.get('dst_nat_port') is not None:
            data = str(policy['dst_nat_port'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"SMTP"':
            data = str("NaN")
            print('"SMTP"はudpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"SNMP"':
            data = str("161")  # 162
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"NBDS"':
            data = str("138")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"FTP"':
            data = str("21")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"HTTP"':
            data = str("NaN")
            print('"HTTP"はudpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"HTTPS"':
            data = str("NaN")
            print('"HTTPS"はudpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"NTP"':
            data = str("123")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"SYSLOG"':
            data = str("514")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"DNS"':
            data = str("53")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"MAIL"':
            data = str("NaN")
            print('"MAIL"はudpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"PING"':
            data = str("NaN")
            print('"PING"はudpを使用しません')
            print('policy_id = %sの出力をスキップしました' % policy['policy_id'])
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"ANY"':
            if policy['src_ip'] == '"Any"' and policy['dst_ip'] == '"Any"':
                # TODO:Any Any ANYの時の処理を変更する
                data = str("65535")
                multiple.handle_multiple_ip(policy, append_list, data)
            else:
                data = str("53")
                multiple.handle_multiple_ip(policy, append_list, data)
        else:
            for service_c in absorbdict.service_dict:
                if service_c['service_name'] == policy['protocol'] and service_c['protocol_name'] == "udp":
                    data = str(service_c['dst_port_num'].split('-')[1])
                    multiple.handle_multiple_ip(policy, append_list, data)
                    break
                else:
                    continue
            else:
                if len(absorbdict.group_service_dict) >= 2:
                    for group_service_c in absorbdict.group_service_dict:
                        if group_service_c['group_service_name'] == policy['protocol']:
                            service_name = group_service_c['service_name']
                            for service_c in absorbdict.service_dict:
                                if service_c['service_name'] == service_name and service_c['protocol_name'] == "udp":
                                    data = str(
                                        service_c['dst_port_num'].split('-')[1])
                                    multiple.handle_multiple_ip(
                                        policy, append_list, data)
                                    break
                                else:
                                    continue
                            else:
                                # TODO:最初のservice_nameにUDPが使用されていなければデフォが入ってしまい次以降でデフォが使用されていると異なる挙動となる
                                data = str("53")
                                multiple.handle_multiple_ip(
                                    policy, append_list, data)
                            break
                    else:
                        data = str("NaN")
                        print('service_nameでudpが使用されていないため出力しませんでした')
                        print('policy_id = %sの出力をスキップしました' %
                              policy['policy_id'])
                        multiple.handle_multiple_ip(policy, append_list, data)
                else:
                    data = str("NaN")
                    print('service_nameでudpが使用されていないため出力しませんでした')
                    print('policy_id = %sの出力をスキップしました' %
                            policy['policy_id'])
                    multiple.handle_multiple_ip(policy, append_list, data)


handle_dst_port_udp()
