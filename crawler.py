import requests
from lxml import etree


class Crawler(object):

    def __init__(self):
        self.start_url = "https://www.xicidaili.com/nn/{}"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            "Host": "www.xicidaili.com",
            # "Pragma": "no-cache",
            # "Sec-Fetch-Mode": "navigate",
            # "Sec-Fetch-Site": "none",
            # "Sec - Fetch - User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "zh-CN,zh;q = 0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }

    def get_url_list(self):
        return [self.start_url.format(i) for i in range(1, 3)]

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        # print(response.status_code)
        return response.content

    def get_ip(self, html_str):
        # //tbody/tr/td[6]
        html = etree.HTML(html_str)
        tr_list = html.xpath("//table[@id='ip_list']/tr")
        # print(tr_list)
        ip_list = []
        for tr in tr_list:
            ip = tr.xpath("//td[2]/text()")[0]
            port = tr.xpath("//td[3]/text()")[0]
            type = tr.xpath("//td[6]/text()")[0]
            ip_list.append(type.lower() + "://" + ":".join([ip, port]))
        return ip_list

    def run(self):
        # 1. url_list
        url_list = self.get_url_list()
        ips_list = []
        # 2. 发送请求  获取响应
        for url in url_list:
            # print(url)
            html_str = self.parse_url(url)
            # 3. 提取数据
            ip_list = self.get_ip(html_str)
            ips_list.extend(ip_list)
        return ips_list


if __name__ == '__main__':
    crawler = Crawler()
    for ip in crawler.run():
        print(ip)
