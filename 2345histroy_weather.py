#coding:utf-8

import requests
import config
from lxml import etree
import csv
import time
import re
from concurrent.futures import ThreadPoolExecutor   # 线程池


# 历史天气url
# http://tianqi.2345.com/Pc/GetHistory?areaInfo[areaId]=1009412&areaInfo[areaType]=1&date[year]=2022&date[month]=5
# http://tianqi.2345.com/Pc/GetHistory?areaInfo[areaId]=59287&areaInfo[areaType]=2&date[year]=2022&date[month]=4
# [areaId]=59287 地区id
# [areaType]=1/2    国内为2 国际为1
# [year]=2022   年份
# [month]=5 月份

now_year = int(time.strftime("%Y", time.localtime(time.time())))
now_month = int(time.strftime("%m", time.localtime(time.time())))
count = 0

def dowload_info(areaId_list, areaType, year_list, month_list, province):
    '''获取天气并写入csv'''

    with open(province +'.csv', 'a', encoding='utf-8', newline='') as f_csv:
        csv_header = csv.DictWriter(f_csv, fieldnames=['日期', '最高温', '最低温', '天气', '风力风向', '城市'])
        csv_header.writeheader()

    for areaId in areaId_list:
        city = list(config.map[province].keys())[list(config.map[province].values()).index(areaId)]
        fcsv = open(province +'.csv', 'a', encoding='utf-8', newline='')
        csv_write = csv.writer(fcsv)
        for year in year_list:
            # print(year_list)
            print(year)
            if year == now_year:
                month_list = list(range(1, now_month + 1))
            for month in month_list:
                print('现在是: {}年\t {}月\t {}'.format( str(year) , str(month) , str(province)))
                params = {
                    'areaInfo[areaId]': areaId,
                    'areaInfo[areaType]' : areaType,
                    'date[year]': year,
                    'date[month]': month
                }

                resp = requests.get(config.histroy_weather_url, params=params,headers=config.headers)
                if resp.status_code != 200:
                    count+=1
                resp.encoding = 'unicode_escape'
                resp_html = resp.text.replace('\\', '').replace('°', '')
                clear_html = re.sub(r'周.', '', resp_html)   # re 去除星期几
                html = etree.HTML(clear_html)
                table1 = html.xpath('/html/body/table/tr[position() > 1]')
                for i in table1:
                    txt = i.xpath('./td/text()')
                    # print(txt)
                    txt.append(city)
                    csv_write.writerow(txt)
    fcsv.close()


def get_city_code():
    '''从配置文件中获取每个省的城市的code, 并返回字典 格式： 省份：[code1, code2, ...]'''

    city_code_list = []
    for c in list(config.map.values()):
        city_code_list.append(list(c.values()))
    province = dict(zip(list(config.map.keys()), city_code_list))
    return province

def get_weather():
    ''' 配置参数， 并使用多线程启动'''
    
    csv_name = list(get_city_code().keys())
    year_list = list(range(now_year-11, now_year+1))
    month_list = list(range(1, 13))
    areaType = config.areaType  # 地区（国内与国外）

    with ThreadPoolExecutor(len(csv_name)) as t:
        for province in csv_name:
            areaId_list = get_city_code()[province]
            t.submit(dowload_info, areaId_list, areaType, year_list, month_list, province)

    print('提取完成')
    print('失败次数{}'.format(count))
    


if __name__ == '__main__':

    get_weather()
