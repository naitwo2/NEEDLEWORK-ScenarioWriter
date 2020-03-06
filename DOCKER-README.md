# Docker版のREADME
## 目次
- コンテナのビルド
- 実行
- 実行例

## コンテナのビルド
```
git clone https://github.com/apc-susumu-tanaka/NEEDLEWORK-ScenarioWriter.git
cd NEEDLEWORK-ScenarioWriter
make
```

## 実行
※この例では、コンフィグファイルを、"/sample/ssg_config.txt"とします。
※**コンフィグファイルは/scenario.txtにバインドしてください**
```
docker run -v /sample/ssg_config.txt:/scenario.txt \
-e DISABLE_POLICY_OUTPUT=n \
needlework-scenariowriter:latest
```


## 実行例
```
dummyuser@linux :~/develop/NEEDLEWORK-ScenarioWriter$ docker run -v /sample/sample_cfg.txt:/scenario.txt -e DISABLE_POLICY_OUTPUT=n needlework-scenariowriter:latest
icmpのポリシーを生成しています
icmpのポリシーが生成されました
tcpのポリシーを生成しています
tcpのポリシーが生成されました
udpのポリシーを生成しています
udpのポリシーが生成されました
csvが生成されました
=======CSVを出力します=======
exclude-list,,protocol,src-fw,src-vlan(option),src-ip,src-port(option),src-nat-ip(option),dst-fw,dst-vlan(option),dst-nat-ip(option),dst-nat-port (option),dst-ip,dst-port,url/domain(option),anti-virus(option),timeout(option),try(option),expect,description
,,icmp,172.16.0.254,,192.168.128.1,,,10.0.0.254,,172.16.0.254,,200.200.200.203,,,,,,drop,policy id =77
~中略~
,,udp,172.16.0.254,,192.168.128.1,,,172.16.30.254,30,,,172.30.2.126,65535,,,,,pass,policy id =95
```