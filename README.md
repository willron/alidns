# alidns
阿里云DNS命令行操作工具

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
