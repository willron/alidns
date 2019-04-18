#!/usr/bin/env python2
# coding:utf-8
'''
by:willron
'''
__author__ = 'zxp'


import json
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import CheckDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordInfoRequest
from aliyunsdkalidns.request.v20150109 import SetDomainRecordStatusRequest


def domainname_split(host):
    host_split = host.strip().split('.')
    if host.endswith('com.cn') or host.endswith('net.cn'):
        host_split[-1] = host_split[-2] + '.' + host_split.pop()

    domainname = '.'.join(host_split[-2:])
    if len(host_split) < 3:
        return []
    if len(host_split) == 3:
        rr = host_split[0]
    if len(host_split) > 3:
        rr = '.'.join(host_split[0:-2])
    return [rr, domainname]


def send_request(request):
    request.set_accept_format('json')
    ali_auth = client.AcsClient('xxxxxxxxxxx', 'xxxxxxxxxxxxxx', 'cn-shenzhen')
    result = ali_auth.do_action(request)
    return json.loads(result)


def get_record_from_id(recordid):
    request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    request.set_RecordId(recordid)
    result = send_request(request)
    return result


def simple_search(website, pagesize=50):
    rr_domainname = domainname_split(website)
    if rr_domainname:
        rr = rr_domainname[0]
        domainname = rr_domainname[1]
        simplesearch_list = []
        pagenumber = 1
        while True:
            request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
            request.set_DomainName(domainname)
            request.set_RRKeyWord(rr)
            request.set_PageSize(pagesize)
            request.set_PageNumber(pagenumber)
            result = send_request(request)
            simplesearch_list.extend(result['DomainRecords']['Record'])
            totalcount = result['TotalCount']
            max_page_number = totalcount / pagesize + 1
            if pagenumber == max_page_number:
                break
            pagenumber += 1
        return simplesearch_list
    return False


def exact_search(website):
    simplefound_list = simple_search(website)
    if simplefound_list is False or simplefound_list == []:
        return simplefound_list
    exactsearch_list = []
    for each in simplefound_list:
        if each['RR'] == domainname_split(website)[0]:
            exactsearch_list.append(each)
    return exactsearch_list


def add_record(website, value, type='A', line='default', ttl=600):

    rr_domainname = domainname_split(website)
    if rr_domainname:
        rr = rr_domainname[0]
        domainname = rr_domainname[1]
        request = AddDomainRecordRequest.AddDomainRecordRequest()
        request.set_RR(rr)
        request.set_DomainName(domainname)
        request.set_Type(type)
        request.set_Value(value)
        request.set_Line(line)
        request.set_TTL(ttl)
        result = send_request(request)
        return result
    return False


def safe_add_record(website, value, type='A', line='default', ttl=600):
    exactresult = exact_search(website)
    rr_domainname = domainname_split(website)
    if rr_domainname:
        rr = rr_domainname[0]
        domainname = rr_domainname[1]

        if exactresult:

            for i in exactresult:
                if i['RR'] == rr and i['DomainName'] == domainname and i['Value'] == value and i['Type'] == type and i['Line'] == line:
                    i['Opeartion'] = False
                    return [i]

        result = add_record(website, value, type, line, ttl)
        if 'RecordId' in result:
            exactresult = exact_search(website)
            return exactresult

    return False


def modify_record(recordid, website, value, type='A', line='default', ttl=600):
    rr_domainname = domainname_split(website)
    if rr_domainname:
        rr = rr_domainname[0]
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_RecordId(recordid)
        request.set_RR(rr)
        request.set_Type(type)
        request.set_Value(value)
        request.set_Line(line)
        request.set_TTL(ttl)
        result = send_request(request)
        if 'RecordId' in result:
            checkresule = get_record_from_id(recordid)
            return [checkresule]
    return False


def set_record_status(recordid, status):
    request = SetDomainRecordStatusRequest.SetDomainRecordStatusRequest()
    request.set_RecordId(recordid)
    request.set_Status(status)
    result = send_request(request)
    if 'RecordId' in result:
        checkresult = get_record_from_id(recordid)
        return [checkresult]
    return False


if __name__ == '__main__':

    from optparse import OptionParser

    usage = 'usage: %prog [options] arg'
    parser = OptionParser(usage)

    # 与API参数有关的参数，大写
    parser.add_option('-I', '--record-id', dest='recordid', type='int', help='the record id')

    parser.add_option('-S', '--record-status', dest='status', help='record status : [ enable | disable ]')

    parser.add_option('-W', '--web-site', dest='website', help='the web site address')

    # parser.add_option('-R', '--resource-record', dest='rr', help='Resource Record. host in fact')

    parser.add_option('-V', '--value', dest='value', help='the value to record')

    parser.add_option('-T', '--type', dest='type',
                      help='record type. default is A. all type : [ A | CNAME | MX | NS | TXT | AAAA | SRV ]')

    parser.add_option('-M', '--ttl', dest='ttl', type='int', help='TTL. default 600')

    parser.add_option('-L', '--line', dest='line',
                      help='line for record. default is "default" line. '
                           'all line: [default|unicom|telecom|mobile|edu|oversea|baidu|biying|google|youdao|yahoo]')

    # parser.add_option('-E', '--remark', dest='remark', help='remark to the record')


    # 脚本相关参数，小写
    parser.add_option('-o', '--operation', dest='operation', help='all operation: [ check | add | update | setstatus ]')

    parser.add_option('-s', '--simple-search', action='store_true', dest='searchmode',
                      help='simple search mode, find all record include host, like %host% in mysql')

    parser.add_option('-e', '--exact-search', action='store_false', dest='searchmode',
                      help='exact search mode, just find the record match host. default search mode')

    parser.add_option('-t', '--table-output', action='store_true', dest='tableoutput', help='format output to table')

    parser.add_option('-j', '--json-output', action='store_true', dest='jsonoutput', help='format output to json')

    # 设置参数默认值
    parser.set_defaults(searchmode=False, type='A', line='default', ttl=600)

    (options, args) = parser.parse_args()

    if options.tableoutput and options.jsonoutput:
        parser.error('do not put json-output and table-output together!')

    # if not options.operation or options.operation.lower() not in ['add', 'check', 'update', 'setstatus']:
    #     parser.error('the operation option (-o) is not define or missing!')

    # if not options.website:
    #     parser.error('need a website!')

    if options.operation == 'check':    # 查询记录
        if not options.website:
            parser.error('need the website!')
        if options.searchmode is True:
            result = simple_search(options.website)
        else:
            result = exact_search(options.website)

    elif options.operation == 'add':    # 添加记录
        if options.website and options.value:
            if options.type not in ['A', 'CNAME', 'MX', 'NS', 'TXT', 'AAAA', 'SRV']:
                parser.error('wrong type (-T)')
            if options.line not in ['default', 'unicom', 'telecom', 'mobile', 'edu', 'oversea',
                                    'baidu', 'biying', 'google', 'youdao', 'yahoo']:
                parser.error('wrong line (-L)')
            result = safe_add_record(website=options.website, value=options.value,
                                        type=options.type, line=options.line, ttl=options.ttl)
        else:
            parser.error('add record need a website and a value at least!')

    elif options.operation == 'update':     # 修改记录
        if options.website and options.value and options.type and options.recordid:
            if options.type not in ['A', 'CNAME', 'MX', 'NS', 'TXT', 'AAAA', 'SRV']:
                parser.error('wrong type (-T)')
            if options.line not in ['default', 'unicom', 'telecom', 'mobile', 'edu', 'oversea',
                                    'baidu', 'biying', 'google', 'youdao', 'yahoo']:
                parser.error('wrong line (-L)')
            result = modify_record(recordid=options.recordid, website=options.website, value=options.value,
                                   type=options.type, line=options.line, ttl=options.ttl)
        else:
            parser.error('update record need the website, value, type and recordid!')

    elif options.operation == 'setstatus':      # 设置记录状态
        if options.recordid and options.status:
            if options.status.lower() not in ['enable', 'disable']:
                parser.error('record status must enable or disable!')
            result = set_record_status(recordid=options.recordid, status=options.status)
        else:
            parser.error('set record status need recordid and status!')

    else:
        parser.error('the operation option (-o) is not define or missing!')


    if result is not False:
        # 输出格式化
        if options.jsonoutput:
            print json.dumps(result, ensure_ascii=False, indent=4)
        elif options.tableoutput:
            from prettytable import PrettyTable
            t = PrettyTable(['RecordID', 'SiteAddress', 'Type', 'Value', 'Line', 'Status', 'Opeartion'])
            t.align['SiteAddress'] = 'l'
            t.padding_width = 1
            for i in result:
                row = [i['RecordId'], i['RR'] + '.' + i['DomainName'], i['Type'], i['Value'], i['Line'], i['Status']]
                if 'Opeartion' in i:
                    row.append(str(i['Opeartion']))
                else:
                    row.append('')
                t.add_row(row)
            print t
        else:
            # print result
            for i in result:
                print i['RecordId'], i['RR'] + '.' + i['DomainName'], i['Type'], i['Value'], i['Line'], i['Status']
    else:
        print 'There is return False!'

