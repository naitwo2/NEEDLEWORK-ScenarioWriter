from main import absorbdict

from main import multiple

protocol_icmp = []
protocol_tcp = []
protocol_udp = []

# protocolのリストの生成


# その他設定で用いられるプロトコルがあれば別途実装する
def handle_protocol_icmp():
    global protocol_icmp
    append_list = protocol_icmp
    for policy in absorbdict.policy_dict:
        if policy['protocol'] == '"ANY"':
            data = str("icmp")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"PING"':
            data = str("icmp")
            multiple.handle_multiple_ip(policy, append_list, data)
        else:
            flag = False
            for service_c in absorbdict.service_dict:
                if policy['protocol'] == service_c['service_name'] and service_c['protocol_name'] == "icmp":
                    flag = True
                    data = str("icmp")
                    multiple.handle_multiple_ip(policy, append_list, data)
            else:
                if not flag:
                    data = str("")
                    multiple.handle_multiple_ip(policy, append_list, data)


handle_protocol_icmp()


def handle_protocol_tcp():
    global protocol_tcp
    append_list = protocol_tcp
    for policy in absorbdict.policy_dict:
        if policy['protocol'] == '"ANY"':
            data = str("tcp")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"PING"':
            data = str("")
            multiple.handle_multiple_ip(policy, append_list, data)
        else:
            flag = False
            for service_c in absorbdict.service_dict:
                if policy['protocol'] == service_c['service_name'] and service_c['protocol_name'] == "tcp":
                    flag = True
                    data = str("tcp")
                    multiple.handle_multiple_ip(policy, append_list, data)
            else:
                if not flag:
                    data = str("tcp")
                    multiple.handle_multiple_ip(policy, append_list, data)


handle_protocol_tcp()


def handle_protocol_udp():
    global protocol_udp
    append_list = protocol_udp
    for policy in absorbdict.policy_dict:
        if policy['protocol'] == '"ANY"':
            data = str("udp")
            multiple.handle_multiple_ip(policy, append_list, data)
        elif policy['protocol'] == '"PING"':
            data = str("")
            multiple.handle_multiple_ip(policy, append_list, data)
        else:
            flag = False
            for service_c in absorbdict.service_dict:
                if policy['protocol'] == service_c['service_name'] and service_c['protocol_name'] == "udp":
                    flag = True
                    data = str("udp")
                    multiple.handle_multiple_ip(policy, append_list, data)
            else:
                if not flag:
                    data = str("udp")
                    multiple.handle_multiple_ip(policy, append_list, data)


handle_protocol_udp()
