# import time
# 爬取演员列表
def get_douban_drama_detail(id):
    
    # url = "https://movie.querydata.org/api"
    url = "https://movie.douban.com/j/subject_abstract"
    params = {
        "subject_id": id
    }
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(url, params = params, headers = headers)
    if response.status_code != 200:
        print("request failed")
        return {}
    drama = response.json().get("subject", {})
    return drama


tvid2actors = {}
tvid2detail = {}
actor_fout = open('电视剧演员名单.csv', 'w')
for tag in tag_list:
    dramas_list = result[tag]
    for drama in dramas_list:
        # time.sleep(1)
        tv_id = drama[1]
        drama_detail = get_douban_drama_detail(tv_id)
        tvid2detail[tv_id] = drama_detail
        actors = drama_detail.get('actor', [])
        for name in actors:
            actor_fout.write(f'{tv_id},{name}')
        tvid2actors[tv_id] = actors
actor_fout.close()   
