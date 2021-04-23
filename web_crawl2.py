# encoding: utf-8
import json
import traceback
import requests
import sys
from urllib.parse import urljoin
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
    for page in range(1, 16):
        if page == 1:
            url = "http://wsjkw.hlj.gov.cn/searchs/5e12d28f6df5eb2c8cccfde4?keys=%E8%BD%A8%E8%BF%B9"
        else:
            url = f'http://wsjkw.hlj.gov.cn/searchs/5e12d28f6df5eb2c8cccfde4?keys=%E8%BD%A8%E8%BF%B9&page={page}'

        xml, status_code = get_response_xml(url)
        if status_code != 200:
            print(f'url请求失败: {url}')
            continue

        content_url_list = xml.xpath('//div[@class="list_content"]/ul/li/p/a/@href')
        for content_url in content_url_list:
            try:
                next_url = urljoin(url, content_url)

                next_xml, status_code = get_response_xml(next_url)
                if status_code != 200:
                    print(f'url请求失败: {url}')
                    continue

                title = next_xml.xpath('//div[@class="main"]/h4/text()|//div[@class="gknb_top"]/p/text()')[0]
                publish_time = next_xml.xpath('//div[@class="main"]/div[@class="time"]/b[contains(text(), "时间")]/text()|//div[@class="gknb_span"]/text()')[0]
                if "发布时间" in publish_time:
                    publish_time = publish_time.split()[0].replace('发布时间：', "")
                else:
                    publish_time = publish_time.replace('时间 : ', "")
                main_text = next_xml.xpath('//div[@class="main"]/p//text()')
                if not main_text:
                    main_text = next_xml.xpath('//div[@class="gknb_content"]/p//text()')
                main_text = '\n'.join(main_text)

                source = province
                data_list.append({
                    'title': title.strip(),
                    'publish_time': publish_time.strip(),
                    'main_text': main_text.strip(),
                    'source': source,
                })
            except:
                traceback.print_exc()
                print(f'url请求解析失败: {next_url}')
                continue
    json.dump({province: data_list}, f, ensure_ascii=False, indent=2)
    f.close()


if __name__ == '__main__':
    run()
