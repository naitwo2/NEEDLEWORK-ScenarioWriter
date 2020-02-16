from absorbdict import start
import protocol
import srcfw
import srcip
import srcnatip
import srcport
import srcvlan
import dstfw
import dstip
import dstnatip
import dstnatport
import dstport
import dstvlan
import expect
import description

from datetime import datetime
import pandas as pd
import time

csv_title = 'SSG_convert_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.csv'


def generate_csv():
    # 生成した各リストをデータフレームに代入する
    df_icmp = pd.DataFrame({
        'exclude-list': '',
        '': '',
        'protocol': protocol.protocol_icmp,
        'src-fw': srcfw.src_fw,
        'src-vlan(option)': srcvlan.src_vlan,
        'src-ip': srcip.src_ip,
        'src-port(option)': srcport.src_port,
        'src-nat-ip(option)': srcnatip.src_nat_ip,
        'dst-fw': dstfw.dst_fw,
        'dst-vlan(option)': dstvlan.dst_vlan,
        'dst-nat-ip(option)': dstnatip.dst_nat_ip,
        'dst-nat-port (option)': dstnatport.dst_nat_port,
        'dst-ip': dstip.dst_ip,
        'dst-port': dstport.dst_port_icmp,
        'url/domain(option)': '',
        'anti-virus(option)': '',
        'timeout(option)': '',
        'try(option)': '',
        'expect': expect.expect_icmp,
        'description': description.description
    }).replace({'NaN': pd.np.nan, 'nan': pd.np.nan})

    df_tcp = pd.DataFrame({
        'exclude-list': '',
        '': '',
        'protocol': protocol.protocol_tcp,
        'src-fw': srcfw.src_fw,
        'src-vlan(option)': srcvlan.src_vlan,
        'src-ip': srcip.src_ip,
        'src-port(option)': srcport.src_port,
        'src-nat-ip(option)': srcnatip.src_nat_ip,
        'dst-fw': dstfw.dst_fw,
        'dst-vlan(option)': dstvlan.dst_vlan,
        'dst-nat-ip(option)': dstnatip.dst_nat_ip,
        'dst-nat-port (option)': dstnatport.dst_nat_port,
        'dst-ip': dstip.dst_ip,
        'dst-port': dstport.dst_port_tcp,
        'url/domain(option)': '',
        'anti-virus(option)': '',
        'timeout(option)': '',
        'try(option)': '',
        'expect': expect.expect,
        'description': description.description
    }).replace({'NaN': pd.np.nan, 'nan': pd.np.nan})

    df_udp = pd.DataFrame({
        'exclude-list': '',
        '': '',
        'protocol': protocol.protocol_udp,
        'src-fw': srcfw.src_fw,
        'src-vlan(option)': srcvlan.src_vlan,
        'src-ip': srcip.src_ip,
        'src-port(option)': srcport.src_port,
        'src-nat-ip(option)': srcnatip.src_nat_ip,
        'dst-fw': dstfw.dst_fw,
        'dst-vlan(option)': dstvlan.dst_vlan,
        'dst-nat-ip(option)': dstnatip.dst_nat_ip,
        'dst-nat-port (option)': dstnatport.dst_nat_port,
        'dst-ip': dstip.dst_ip,
        'dst-port': dstport.dst_port_udp,
        'url/domain(option)': '',
        'anti-virus(option)': '',
        'timeout(option)': '',
        'try(option)': '',
        'expect': expect.expect,
        'description': description.description
    }).replace({'NaN': pd.np.nan, 'nan': pd.np.nan})
    # データフレームを元にcsvを生成する
    print('icmpのポリシーを生成しています')
    df_icmp.query("protocol != ''").dropna(
        how='any').to_csv(csv_title, index=False)
    print('icmpのポリシーが生成されました')
    print('tcpのポリシーを生成しています')
    df_tcp.query("protocol != ''").dropna(how='any').to_csv(
        csv_title, index=False, mode='a', header=False)
    print('tcpのポリシーが生成されました')
    print('udpのポリシーを生成しています')
    df_udp.query("protocol != ''").dropna(how='any').to_csv(
        csv_title, index=False, mode='a', header=False)
    print('udpのポリシーが生成されました')
    print('csvが生成されました')
    elapsed_time = time.time() - start
    print("ツールを使用した時間は{0}".format(elapsed_time) + "秒です")


generate_csv()
