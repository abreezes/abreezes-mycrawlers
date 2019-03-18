import demjson
import requests

# user_info_url='https://api.weibo.com/2/users/show.json'
# user_info_url='https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid=230283{}'
user_info_url='https://m.weibo.cn/api/container/getIndex?containerid=2302831826792401_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid=2302831826792401'
win='https://event.weibo.com/yae/aj/event/mlottery/result?id=2110000&pageid='
home='https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid=100505{}'
key='1711685942'
token='2.00efEGREmhDqrB48defe3c52Ot3QOC'
# cookies={'_T_WM': 'e0e2d6a3a8290136f328546c66fd3b83', 'ALF': '1546668983', 'M_WEIBOCN_PARAMS': 'luicode%3D10000011%26lfid%3D2302835723535900%26fid%3D2302835723535900_-_INFO%26uicode%3D10000011', 'MLOGIN': '1', 'SCF': 'AtvqNjJ-OZuRPXdlcA6x5ZbbRLHfPqSwM_ySwbxGJExWXHepCsLGps-yNwHXa2X_dvJZZhyByZMOU_rjVUxf2Bo.', 'SSOLoginState': '1544076983', 'SUB': '_2A25xAaW7DeRhGeBI7FcW-CvPzzmIHXVSDcvzrDV6PUJbkdAKLU7skW1NRmH6km1q3hDNeK8O79EdHdkPI9_HKkul', 'SUHB': '0h1Z6bjuLoA8ye', 'WEIBOCN_FROM': '1110006030'}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# cookies={'_s_tentry': 'www.google.com', 'ALF': '1546668983', 'Apache': '5148580838035.799.1544076940520', 'SINAGLOBAL': '3178230129927.7793.1543887699277', 'SSOLoginState': '1544076983', 'SUB': '_2A25xAaW7DeRhGeBI7FcW-CvPzzmIHXVSDcvzrDV6PUJbkdAKLU7skW1NRmH6km1q3hDNeK8O79EdHdkPI9_HKkul', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWCA4.0bXvQ48u1CfWJSIMo5JpX5KzhUgL.Foe4eKMpS0q4Soq2dJLoI7n_CJLydJM_xBtt', 'SUHB': '0h1Z6bjuLoA8ye', 'ULV': '1544076940527:3:3:3:5148580838035.799.1544076940520:1543995855879', 'UOR': ',,www.google.com', 'wvr': '6', 'Ugrow-G0': '5b31332af1361e117ff29bb32e4d8439', 'wb_view_log_3917176966': '1920*10801', 'YF-Page-G0': 'bf52586d49155798180a63302f873b5e', 'YF-V5-G0': '82f55bdb504a04aef59e3e99f6aad4ca', '_T_WM': 'e0e2d6a3a8290136f328546c66fd3b83', 'M_WEIBOCN_PARAMS': 'luicode%3D10000011%26lfid%3D2302835723535900%26fid%3D2302835723535900_-_INFO%26uicode%3D10000011', 'MLOGIN': '1', 'SCF': 'AtvqNjJ-OZuRPXdlcA6x5ZbbRLHfPqSwM_ySwbxGJExWXHepCsLGps-yNwHXa2X_dvJZZhyByZMOU_rjVUxf2Bo.', 'WEIBOCN_FROM': '1110006030'}
# cookies={
#   "ECARD-G0": "17be1f05a3b451108a01af5b858319ca",
#    "SSOLoginState":  "1544146818",
#    "ALF":  "1546738797",
#    "login_sid_t":  "daa290c0039cf66b56de03dd44b8e248",
#    "SUHB":  "0IIFLrd4cmQiIb",
#    "SUBP":  "0033WrSXqPxfM725Ws9jqgMF55529P9D9WW2IOAXA06p2MHZ6mlCa.Cz5JpX5K-hUgL.Foqc1hzXeK2fSK-2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSonESh2pSK-f",
#    "cross_origin_proto":  "SSL",
#    "_s_tentry":  "passport.weibo.com",
#    "SINAGLOBAL":  "619744659932.2709.1544146769534",
#    "Apache":  "619744659932.2709.1544146769534",
#    "ULV":  "1544146769541:1:1:1:619744659932.2709.1544146769534:",
#    "SCF":  "Alhr-wrFp_Pr0G9xPnwjgcRknroih6Lyj1GNaTKgTBka3h6rnXSVRZ6PRE0h9Zih8fhERzOi1n_lHsXAT8RHQfs.",
#    "SUB":  "_2A25xDb_SDeRhGeBI41AV8S_JzjmIHXVS8cGarDV6PUJbktAKLW7MkW1NRnogxHKvGuDfPB2DVS_m7EyQ4ttUzjn3",
#    "un":  "zsvxry167639@game.weibo.com",
#    "WBStorage":  "bfb29263adc46711|undefined",
#    "Ugrow-G0":  "8751d9166f7676afdce9885c6d31cd61",
#    "YF-V5-G0":  "5468b83cd1a503b6427769425908497c",
#    "YF-Page-G0":  "324e50a7d7f9947b6aaff9cb1680413f",
#    "wb_view_log":  "1920*10801",
#    "WEIBOCN_FROM":  "1110006030",
#    "_T_WM":  "c1cfcc1d7f3e99753735cb164c81a37f",
#    "MLOGIN":  "1",
#    "M_WEIBOCN_PARAMS":  "luicode%3D10000011%26lfid%3D2302835723535900%26fid%3D2302835723535900_-_INFO%26uicode%3D10000011"
# }
# 最后基本信息cookes
cookies={
  "ECARD-G0": "3b12e468e76dbfb55a0adb3de1390008",
   "SSOLoginState":  "1544149027",
   "ALF":  "1546741006",
   "login_sid_t":  "0424ae3e5b6b689500f73823c6ded349",
   "SUHB":  "079z_FvyM6x0Un",
   "SUBP":  "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5EmW-xb484LZNzFWlTVsBV5JpX5K-hUgL.Foqc1hzXeK2N1h.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSonESh2pS0n4",
   "cross_origin_proto":  "SSL",
   "_s_tentry":  "passport.weibo.com",
   "SINAGLOBAL":  "2141366855924.8132.1544148978206",
   "Apache":  "2141366855924.8132.1544148978206",
   "ULV":  "1544148978217:1:1:1:2141366855924.8132.1544148978206:",
   "SCF":  "AsmVPL5h2aDJZhyiafciNNkA2W7oXjwIaAYinb9bgHXknH-WnwOqokEYUkFowh2rCz_U6nHs342EULd1dypKeDA.",
   "SUB":  "_2A25xDahyDeRhGeBI41AV8S_LwzWIHXVS8cg6rDV6PUJbktAKLWjzkW1NRnog72QznmBatiJZr87ipmah-9QDw8NW",
   "un":  "ztutnh667774@game.weibo.com",
   "WBStorage":  "bfb29263adc46711|undefined",
   "Ugrow-G0":  "9642b0b34b4c0d569ed7a372f8823a8e",
   "YF-V5-G0":  "a9b587b1791ab233f24db4e09dad383c",
   "YF-Page-G0":  "8ec35b246bb5b68c13549804abd380dc",
   "wb_view_log":  "1920*10801",
   "WEIBOCN_FROM":  "1110006030",
   "_T_WM":  "43b359553edc0409900c9f70b21c3d2b",
   "MLOGIN":  "1",
   "M_WEIBOCN_PARAMS":  "luicode%3D10000011%26lfid%3D2302831826792401%26fid%3D2302831826792401_-_INFO%26uicode%3D10000011"
}

# 没带基本信息cookies
cookies1 = {
    'wvr': '6',
    'SINAGLOBAL': '3178230129927.7793.1543887699277',
    'UOR': ',,www.google.com',
    'ECARD-G0': '3b12e468e76dbfb55a0adb3de1390008',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWCA4.0bXvQ48u1CfWJSIMo5JpX5KMhUgL.Foe4eKMpS0q4Soq2dJLoI7n_CJLydJM_xBtt',
    'ALF': '1575684368',
    'SSOLoginState': '1544148370',
    'SCF': 'Al4Zay_WM1tyBFNvd8JpaPYwmg39CNa7rrf5Vs5T7ng7Vj49w8myzQYxzwCdOUfL6_jC-h5BF4WtlAHcDvnT480.',
    'SUB': '_2A25xDaXFDeRhGeVH6lUQ9yjFzTqIHXVSepANrDV8PUNbmtBeLXnykW9NT390cZuGMuvD0p5KrKZFIE7YptXV4Smv',
    'SUHB': '0WGc556byULXdF',
    '_s_tentry': '-',
    'Apache': '8684387155611.1544148697789',
    'ULV': '1544148697828:4:4:4:8684387155611.1544148697789:1544076940527',
}
# params={'access_token':token,
#         'uid':'5723535900'}
cookies2={"wb_view_log": "1366*7681", "WBStorage": "bfb29263adc46711|undefined", "Ugrow-G0": "169004153682ef91866609488943c77f", "login_sid_t": "5db4733bb20dbba4555d2eeac50f1fe1", "cross_origin_proto": "SSL", "YF-V5-G0": "9717632f62066ddd544bf04f733ad50a", "YF-Page-G0": "340a8661f2b409bf3ea4c8981c138854", "_s_tentry": "passport.weibo.com", "SINAGLOBAL": "6848884282402.412.1544276258384", "Apache": "6848884282402.412.1544276258384", "ULV": "1544276258396:1:1:1:6848884282402.412.1544276258384:", "SUHB": "0cS3uy5b6v_pqU", "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WFl_ipogalE5YXHaekYFn0G5JpX5K-hUgL.Foqc1hzXeK2XS022dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSonESh2pShMp", "ALF": "1546868273", "SSOLoginState": "1544276304", "SCF": "AulsiYVsFYRGEic55GyLxkMFZxmaP2yB2jB0Unuyfd3DU4SKVv5Rd2jMFUD9uNwKU4pUarIj54TMui3eOuYMQmM.", "SUB": "_2A25xD7kADeRhGeBI41AV8S_IzD2IHXVS88dIrDV6PUJbktANLVL-kW1NRnogzGuq4B-e2hhUh4S7OYYjdKcSTpFB", "un": "fvrlek618043@game.weibo.com", "WEIBOCN_FROM": "1110006030", "_T_WM": "d2d834288422c7ffadefdc0a0e2f3918", "MLOGIN": "1", "M_WEIBOCN_PARAMS": "luicode%3D10000011%26lfid%3D2302835723535900%26fid%3D2302835723535900_-_INFO%26uicode%3D10000011"}
cookies3={
  "M_WEIBOCN_PARAMS": "uicode%3D20000174",
   "MLOGIN":  "1",
   "SUB":  "_2A25xFNpnDeRhGeBI41AV8S_JyzqIHXVS9uYvrDV6PUJbkdAKLUPHkW1NRnogyZQBBxIj1Bk6ohD2pvsbANyqehEy",
   "SCF":  "AgO8jWLVX780P4O8_lzwcpa_JL-EDKYZ9zu2FfMtrx1tM3CvxEpvdmBrF6vpJXDf212uysYO72w-vNa7Rz4Z4Bk.",
   "SUHB":  "05iqIBnOs8VCEP",
   "SSOLoginState":  "1544596023",
   "WEIBOCN_FROM":  "1110006030",
   "_T_WM":  "44e9c11bd3689a874bb154e6afd4788d"
}
cookies4={
  "M_WEIBOCN_PARAMS": "uicode%3D20000174",
   "MLOGIN":  "1",
   "SUB":  "_2A25xFMC6DeRhGeBI41AV8S_LwzWIHXVS9uDyrDV8PUJbkNBeLXf8kW1NRnog70Gs1nhALSt55OrQurVX-MEqsQmT",
   "SCF":  "AuhVOCPqXyvyN014mFtKs6eZM22tX7Jm4vunCH6KrVWuZWvT-XYL205ZiuN0m0XwKwCT4VK13m-dACHf-LB-z1E.",
   "SUHB":  "00x55bHEPoJ4Wp",
   "SSOLoginState":  "1544597738",
   "WEIBOCN_FROM":  "1110006030",
   "_T_WM":  "3e7bc1c4e7ad032ab4465a8abc63c1ef",
   "ECARD-G0":  "3b12e468e76dbfb55a0adb3de1390008",
   "ALF":  "1547189739",
   "SUBP":  "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5EmW-xb484LZNzFWlTVsBV5JpX5oz75NHD95QcSonESh2pS0n4Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSoqReoBpeKMR1Btt"
}
res=requests.get(user_info_url,headers=headers,cookies=cookies4)
homeres=requests.get(home.format('6208238296','6208238296'),cookies=cookies4).json()

comp=requests.get('https://m.weibo.cn/api/container/getIndex?containerid=2302832954769872_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid=2302832954769872',cookies=cookies2).text
# print(comp['data']['cards'])

winres=requests.get(win,cookies=cookies4,headers=headers)

pc='https://event.weibo.com/yae/aj/event/lottery/result?pageid=100140E3131412&id=2110002&page=1&prizeLevel=1&_t=0'
winres_pc=requests.get(pc,cookies=cookies4,headers=headers)

print(demjson.decode(res.text)['data']['cards'][1]['card_group'][0]['desc'])
if demjson.decode(res.text)['data']['cards'][1]['card_group'][0]['desc'] == '个人信息':
    print('1111111111')

print(winres_pc.json())
print('-'*30)
print(res)
print('-'*30)
print(winres.json())
print('-'*30)
print(homeres)
