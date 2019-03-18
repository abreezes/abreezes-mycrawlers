# -*- coding: utf-8 -*-
__author__ = 'admin'
__date__ = '2019/1/27 21:10'

import json

def response(flow):
    if 'aweme/v1/user/follower/list' in flow.request.url:
        res=json.loads(flow.response.text)
        with open('uid.txt', 'a+') as f:
            for l in res["followers"]:
                f.write('uid:'+str(l['uid'])+'\n')



if __name__ == '__main__':
    url='https://api.amemv.com/aweme/v1/user/follower/list/?user_id=84990209480&max_time=1548772015&count=20&offset=0&source_type=1&retry_type=no_retry&mcc_mnc=46007&iid=60041729766&device_id=62775678820&ac=wifi&channel=aweGW&aid=1128&app_name=aweme&version_code=430&version_name=4.3.0&device_platform=android&ssmix=a&device_type=HUAWEI+MLA-AL10&device_brand=HUAWEI&language=zh&os_api=22&os_version=5.1.1&uuid=863064011241066&openudid=1240a64f8e9a8400&manifest_version_code=430&resolution=720*1280&dpi=240&update_version_code=4302&_rticket=1548772016664&ts=1548771999&js_sdk_version=1.6.4&as=a10586e56f599cd2204411&cp=6f94ce5ffb065029e1KcSg&mas=01225b9bfacab0b5bc07ac52f605ff74948c8c2c2c0c4c4c26c69c'
    headers={"authority":"api.amemv.com",
                "accept-encoding":"gzip",
                "sdk-version":"1",
                "x-ss-tc":"0",
                "user-agent":"com.ss.android.ugc.aweme/430 (Linux; U; Android 5.1.1; zh_CN; HUAWEI MLA-AL10; Build/HUAWEIMLA-AL10; Cronet/58.0.2991.0)",
                "x-gorgon":"030000004500f340d62dd5c35d32d783735d3fa66e8371563d8a",
                "x-khronos":"1548772016",
                "x-pods":"",
                "cookie":"install_id=60041729766; ttreq=1$d7dd4509133d1114981b2d79102bc12639fe3ca2; odin_tt=ca6cb7e7b55de2e4dd9295ad89839311750cff75aa709bf7a4706cd416ed34799eadec1ff9bae483bd83ad72cd4b73932c54ea49a82c2fe3c8c7e84ec00849c0",}

    import requests
    res=requests.get(url,headers=headers).json()
    for l in res['followers']:
        print(l['uid'])
        # print(res['followers'])

