# @Time    : 2019/10/15 0015 下午 21:03
# @Author  : h.user
# @Email   : h.user.com
# @File    : __init__.py.py
# @Software: PyCharm

import json
import execjs

import requests


class GoogleTranslate(object):
    """
    针对google翻译进行封装
    """
    XO = "436428.3201187685"
    JS_CODE = """function vo(a){return function(){return a}};function wo(a,b){for(var c=0;c<b.length-2;c+=3){var d=b.charAt(c+2);d="a"<=d?d.charCodeAt(0)-87:Number(d);d="+"==b.charAt(c+1)?a>>>d:a<<d;a="+"==b.charAt(c)?a+d&4294967295:a^d}return a}function tk(a,b){var d=vo(String.fromCharCode(116));c=vo(String.fromCharCode(107));d=[d(),d()];d[1]=c();c="";d=b.split(".");b=Number(d[0])||0;for(var e=[],f=0,g=0;g<a.length;g++){var k=a.charCodeAt(g);128>k?e[f++]=k:(2048>k?e[f++]=k>>6|192:(55296==(k&64512)&&g+1<a.length&&56320==(a.charCodeAt(g+1)&64512)?(k=65536+((k&1023)<<10)+(a.charCodeAt(++g)&1023),e[f++]=k>>18|240,e[f++]=k>>12&63|128):e[f++]=k>>12|224,e[f++]=k>>6&63|128),e[f++]=k&63|128)}a=b;for(f=0;f<e.length;f++)a+=e[f],a=wo(a,"+-a^+6");a=wo(a,"+-3^+b+-f");a^=Number(d[1])||0;0>a&&(a=(a&2147483647)+2147483648);a%=1E6;return c+(a.toString()+"."+(a^b))}"""
    HEADERS = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'referer': 'https://translate.google.cn/?hl=zh-CN&tab=TT',
        'authority': 'translate.google.cn',
    }
    PARAMS = {
        "client": "webapp", "sl": "auto", "tl": "zh-CN", "hl": "zh-CN",
        "dt": "at", "dt": "bd", "dt": "ex", "dt": "ld",
        "dt": "md", "dt": "qca", "dt": "rw", "dt": "rm",
        "dt": "ss", "dt": "t", "otf": "1", "ssel": "0",
        "tsel": "0", "kc": "3", "tk": "795424.691180", "q": "you",
    }

    def get_tk(self, content):
        ctx = execjs.compile(self.JS_CODE)
        result = ctx.call("tk", content, self.XO)
        return result

    def start_translate(self, content, proxies={}, timeout=10):
        """
        默认代理为空,响应超时10秒
        :param content:
        :param proxies:
        :param timeout:
        :return:
        """
        if content is None or content == "":
            return ""
        tk = self.get_tk(content)
        params = self.PARAMS
        params["q"] = content
        params["tk"] = tk
        try:
            response = requests.get(
                url='https://translate.google.cn/translate_a/single',
                headers=self.HEADERS,
                params=params,
                proxies=proxies,
                timeout=timeout
            )
        except requests.exceptions.ReadTimeout:
            print("当前翻译出错,响应超时，请检查网络情况")
            return None
        try:
            response_json = json.loads(response.text)
            result = []
            for item in response_json[0]:
                result.append(item[0].replace("\n", ""))
            if len(result) == 1:
                return result[0]
            else:
                return result
        except json.decoder.JSONDecodeError:
            print("当前翻译出错,请优先检查代理")
            return None


Translate = GoogleTranslate()

if __name__ == '__main__':
    """
    测试代码
    """
    result = Translate.start_translate("hello")
    if result is not None:
        print(result)
    else:
        print(result)
