# encoding: utf-8
import json
import requests
import sys
from lxml.etree import HTML

province = sys.argv[1]

def get_response_xml(url):
    res = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    })
    xml = HTML(res.text)
    return xml, res.status_code


def run():
    data_list = []
    f = open(province+'.json', 'w')
    for i in range(360375, 376401):
        url = f'http://wsjkw.hebei.gov.cn/syyctplj/{i}.jhtml'
        try:
            xml, status_code = get_response_xml(url)
            if status_code == 500:
                continue
            if status_code != 200:
                print(f'url请求失败: {url}')
                continue
            title = xml.xpath('//h1[@class="title"]/text()')[0]
            if '轨迹' not in title:
                continue
            publish_time = xml.xpath('//span[@class="fbsj2"]/text()')[0].replace('发布时间：', "")
            main_text = xml.xpath('//div[@id="zoom"]//text()')
            main_text = '\n'.join(main_text)

            source = province
            data_list.append({
                'title': title.strip(),
                'publish_time': publish_time.strip(),
                'main_text': main_text.strip(),
                'source': source,
            })
        except:
            print(f'url请求解析失败: {url}')
            continue
    json.dump({province: data_list}, f, ensure_ascii=False, indent=2)
    f.close()


if __name__ == '__main__':
    run()
