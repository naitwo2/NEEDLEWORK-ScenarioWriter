# NEEDLEWORK-ScenarioWriter
本ツールはファイアウォールのコンフィグファイルからNEEDLEWORKで使用できるcsvを生成するツールです。<br>現在対応しているファイアウォールは以下の通りです。

* Juniper SSG5 <br>
  ※動作確認バージョン：6.3.0r17.0

# ツールの仕様

## protocol
  * icmp
  * tcp
  * udp

## IP
* ポリシーのIPがAnyの場合、csvに出力されるIPは下記の通りです。
  * Untrustゾーン：8.8.8.8
  * その他のゾーン：設定されているルーティングのネットワークアドレスからFW IPを除いた後のアドレス空間が最も広いネットワークの開始および終了IP（ネットワークアドレスとブロードキャストアドレスを除く）<br>
  例：下記のように設定がされている場合、以下の処理が行われます。
  ```
  set route 10.0.0.0/24 interface ethernet0/0 gateway 10.0.0.1
  set route 10.0.0.0/16 interface ethernet0/0 gateway 10.0.0.2
  set interface ethernet0/0 ip 10.0.0.254/24
  set interface bgroup0 ip 172.16.0.254/24
  ```
  `10.0.0.0/16`からFW IPを除いた後のネットワークアドレス
  ```
   [IPv4Network('10.0.128.0/17'), 
   IPv4Network('10.0.64.0/18'),
   IPv4Network('10.0.32.0/19'), 
   IPv4Network('10.0.16.0/20'), 
   IPv4Network('10.0.8.0/21'), 
   IPv4Network('10.0.4.0/22'), 
   IPv4Network('10.0.2.0/23'), 
   IPv4Network('10.0.1.0/24'), 
   IPv4Network('10.0.0.0/25'), 
   IPv4Network('10.0.0.128/26'), 
   IPv4Network('10.0.0.192/27'), 
   IPv4Network('10.0.0.224/28'), 
   IPv4Network('10.0.0.240/29'), 
   IPv4Network('10.0.0.248/30'), 
   IPv4Network('10.0.0.252/31'), 
   IPv4Network('10.0.0.255/32')]
   ```
   `IPv4Network('10.0.128.0/17')`の開始および終了IPである<br>
   `10.0.128.1`, `10.0.255.254`がcsvに出力されます。

## DIP
* dipを範囲で指定した場合、開始IPのみをcsvに出力します。

## VIP
* VIP対応サービス（ポート）は以下の通りです。
  * FTP（21)
  * DNS(53)
  * HTTP(80)
  * NTP(123)
* ポリシーのIPがVIPかつServiceがANYの場合、VIPに設定した全てのIPを出力します。<br>
例：下記のように設定がされている場合、`192.168.10.1`, `192.168.30.3`, `192.168.80.8`がcsvに出力されます。
```
set interface ethernet0/0 vip interface-ip 21 "FTP" 192.168.10.1
set interface ethernet0/0 vip interface-ip 53 "DNS" 192.168.30.3
set interface ethernet0/0 vip interface-ip 123 "NTP" 192.168.80.8
set policy id 98 name "vip" from "Trust" to "Untrust" "Any" "VIP(ethernet0/0)" "ANY" permit
```

## Service
* 設定したserviceをポリシーで使用した場合、送信元ポートは開始ポートのみをcsvに出力します。
* 設定したserviceをポリシーで使用した場合、宛先ポートは終了ポートのみをcsvに出力します。
* デフォルトで登録されている下記サービスの宛先ポートは以下の通りです。
  * FTP（udp 21)
  * SMTP(tcp 25)
  * MAIL(tcp 25)
  * DNS(tcp,udp 53)
  * HTTP(tcp 80)   
  * NTP(tcp,udp 123)
  * NBDS(udp 138)
  * SNMP(tcp,udp 161)
  * HTTPS(tcp 443)
  * SYSLOG(udp 514)
* ポリシーのServiceがANYの場合、csvに出力される宛先ポート番号は下記の通りです。
  * icmp:なし
  * tcp,udp:65535
* group-serviceにgroup-serviceを追加したserviceをポリシーで使用している場合、group-serviceに含まれる最初のserviceで使用されているポート番号のみを出力します。 <br>
例：下記のように設定がされている場合、`tcp 1010`がcsvに出力されます。
```
 group-service
 　-  group-service（tcp 1010 , tcp 2020 , udp 100 , udp 200）
 　-  service（tcp 8080）
 　-  service（tcp 8081）
```

## その他
* インターフェースに割り当てられていないゾーンがポリシーで使用されている場合、正常にcsvが出力されない恐れがありますのでご注意ください。
* マルチセルポリシーには対応していません。
* csvに非出力のポリシーは理由がメッセージとして出力されます。

# 環境

* OS : Windows 10
* python : 3.7.4
* git : 2.20.1 (Apple Git-117)
* pip : 19.1.1
 

# pythonのインストール

1. pythonを[公式サイト](https://www.python.org/downloads/windows/)からインストールします。 
   * [参考URL](https://www.python.jp/install/windows/install_py3.html)
2. 環境変数を設定します。
   * 詳しくは[ツールの使用方法の項番5](#ツールの使用方法)へ


# gitのインストール

1.  [https://git-for-windows.github.io/](https://git-for-windows.github.io/)よりgitをインストールします。
    * [参考URL](https://prog-8.com/docs/git-env-win)


# ツールの使用方法

0. CLIを起動します。
1. 作業用ディレクトリを作成します。
    * `mkdir ディレクトリ名`
2. 作成したディレクトリに移動します。
    * `cd ディレクトリ名`
3. 作成したディレクトリに本リポジトリをcloneします。
    * `git clone https://github.com/ap-communications/NEEDLEWORK-ScenarioWriter.git`
4. 作成されたディレクトリに移動します。
    * `cd NEEDLEWORK-ScenarioWriter`
5. 環境変数に設定するパス（カレントディレクトリの絶対パス）を表示します。
    * `cd`
6. 5.で表示したパスを環境変数に設定します。
    * `setx PYTHONPATH 5.で表示したパス`
7. PCを再起動します。
8. ツールに使用する外部ライブラリをインストールします。
    * `pip install pandas==0.25.0`
9. 4.で作成されたディレクトリに移動します。
    * `cd 4.で作成されたディレクトリ`
10.  CLIにてツールを使用します。
    * `python main¥gencsv.py file_name disable_policy_output`   
      * file_name:ファイアウォールのコンフィグファイルを相対パスまたは絶対パスで入力、またはドラッグ&ドロップします。
      * disable_policy_output:コンフィグファイルで有効化していないポリシーをcsvに出力するかを決定します。
        * `y` : 出力する
        * `n` : 出力しない

# お問い合わせ
* 改善・要望等ございましたらpull requestをお願いします。

