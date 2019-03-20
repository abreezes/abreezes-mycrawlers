def get_type(value):
    if '工' in value or '工程' in value or '技术员' in value or '技术' in value or '师傅' in value \
            or '技师' in value or '学徒' in value or '维修' in value or '修理' in value or '维护' in value:
        return '工程类'
    elif '总经理' in value or '项目经理' in value or '储备' in value or '运营' in value or '课长' \
            in value or '总监' in value or '主管' in value:
        return '管理类'
    elif '销售' in value or '渠道' in value or '销售工程师' in value or '业务' in value or '市场' \
            in value or '客户经理' in value or '专员' in value:
        return '销售类'
    elif '设计' in value or '开发' in value or '研发' in value or '编程' in value:
        return '设计类'
    else:
        return '其它'

def get_addr(url):
    if '110300' in url or '682' in url:
        return '厦门'
    elif '110400' in url or '685' in url:
        return '泉州'
    elif '110200' in url or '681' in url:
        return '福州'
    elif '110600' in url or '684' in url:
        return '莆田'

if __name__ == '__main__':
    print(get_type('空调维修师傅'))