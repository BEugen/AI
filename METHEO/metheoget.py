from lxml import html
import requests
import pandas as pd

proxies = {
    "http": "127.0.0.1:3128",
    "https": "127.0.0.1:3128",
}


page = requests.get('https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B_%D0%B2_%D0%9D'
                    '%D0%B8%D0%BA%D0%B5%D0%BB%D0%B5', proxies=proxies)
tree = html.fromstring(page.content)
table = html.tostring(tree.xpath('//table[@id="archiveTable"]')[0])
print(table)
dth = pd.read_html(table, header=0, index_col=0)
dth[0].to_csv('metheo.csv', sep=';')
