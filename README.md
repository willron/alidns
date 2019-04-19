# 云厂商DNS解析命令行操作工具
阿里云DNS解析命令行操作工具

```
Usage: alidns.py [options] arg

Options:
  -h, --help            show this help message and exit
  -I RECORDID, --record-id=RECORDID
                        the record id
  -S STATUS, --record-status=STATUS
                        record status : [ enable | disable ]
  -W WEBSITE, --web-site=WEBSITE
                        the web site address
  -V VALUE, --value=VALUE
                        the value to record
  -T TYPE, --type=TYPE  record type. default is A. all type : [ A | CNAME | MX
                        | NS | TXT | AAAA | SRV ]
  -M TTL, --ttl=TTL     TTL. default 600
  -L LINE, --line=LINE  line for record. default is "default" line. all line: 
                        [default|unicom|telecom|mobile|edu|oversea|baidu|biyin
                        g|google|youdao|yahoo]
  -o OPERATION, --operation=OPERATION
                        all operation: [ check | add | update | setstatus ]
  -s, --simple-search   simple search mode, find all record include host, like
                        %host% in mysql
  -e, --exact-search    exact search mode, just find the record match host.
                        default search mode
  -t, --table-output    format output to table
  -j, --json-output     format output to json
  ```

腾讯云DNS解析命令行操作工具

```
Usage: qcloud_dns.py [options] [ ListRecord | AddRecord | ModifyRecord | SetStatus ]

Options:
  -h, --help            show this help message and exit
  -I RECORDID, --record-id=RECORDID
                        the record id
  -S SUB_DOMAIN, --sub-domain=SUB_DOMAIN
                        sub domain, like www
  -A STATUS, --record-status=STATUS
                        record status : [ enable | disable ]
  -D DOMAIN, --domain=DOMAIN
                        the target domain, default: ksgame.com
  -V VALUE, --value=VALUE
                        the value to record
  -T TYPE, --type=TYPE  record type. default is A. all type : [ A | CNAME | MX
                        | NS | TXT | AAAA ]
  -M TTL, --ttl=TTL     TTL. default 600
  -L LINE, --line=LINE  line for record. default is "默认" line. all line:
                        [默认|境内|境外|电信|联通|移动]
  -o OFFSET, --offset=OFFSET
                        set offset
  -l LENGTH, --length=LENGTH
                        set length
  -t, --table-output    format output to table
  -j, --json-output     format output to json
```
