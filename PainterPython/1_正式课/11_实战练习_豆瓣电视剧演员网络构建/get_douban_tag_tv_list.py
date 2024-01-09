# part1： 数据采集
# 采集1：小组偏爱的演员网络
# 数据源：豆瓣电视剧主演信息（中国内地及港澳台）
# >=200部分, 评分>=7分

# 家庭100/爱情100/悬疑100
import requests

def get_douban_tv_dramas(tag = "国产剧", num = 1):
    url = "https://movie.douban.com/j/search_subjects"
    params = {
        "type": "tv",
        "tag": tag,
        "page_limit": num,  # You can adjust the limit as needed
        "page_start": 0
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    response = requests.get(url, params=params, headers = headers)
    dramas = response.json().get('subjects', [])

    filtered_dramas = []
    for drama in dramas:
        title = drama["title"]
        url = drama["url"]
        rate = drama["rate"]
        if rate == '' or float(rate) < 7:
            continue
        did = drama["id"]
        filtered_dramas.append([tag, did, title, rate, url])
    with open(f'{tag}_{len(filtered_dramas)}_list.csv', 'w') as fout:
        for drama in filtered_dramas:
            fout.write(','.join(drama) + '\n')
    return filtered_dramas


tag_list = ["国产剧", "港剧"]

result = {}
for tag in tag_list:
    dramas_list = get_douban_tv_dramas(tag, 300)
    result[tag] = dramas_list


