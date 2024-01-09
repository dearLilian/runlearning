from bs4 import BeautifulSoup
import pandas as pd
import requests
from urllib.parse import quote, unquote





# url = f"https://search.douban.com/movie/subject_search?search_text={quoted_search_text}&cat=1002"

def get_uq_link(search_text):
    quoted_search_text = quote(search_text)

    url = f"https://www.douban.com/search?cat=1002&q={quoted_search_text}"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Ch-Ua": '''"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"''',
        "Referer": "https://movie.douban.com/",
        "Sec-Fetch-Dest": "document",
        "cookie": """bid=WKVIFxu-_BI; ll="108169"; _ga=GA1.1.191779183.1701751376; _cc_id=23b54b9d3ef3a33a34eac66eed7b4a6a; panoramaId_expiry=1702776749037; panoramaId=f1310b00fced7a55f575e1c2e5e316d539385cb9e22ad6923b1d93788d069ada; panoramaIdType=panoIndiv; cto_bundle=BXoJSV91eU5RTFdCSmcxTFh6ZzJ4M3VUSFVkalFicWVrSGZKNkF0SEJKamlRc0lnY0huQzBRTEdRbmVkTm9sdVFIVThqMTVoanNrJTJCYzlRUUhLZEtSbFZNWVNSV1lJV3NHME9JUzVzQjJhWHhubldVbTQlMkJHcVVZeEluaHB1eFJSU2FXYWs1JTJGcWJWT0NNNjJnMTZCVVVXYmg3bERDOE5mVEN5MzN6ZTVEckt0N3Y1WGRQUmQ2JTJGa2xWMGU0b1V3ZDNzbHZ5OEpEQXpTVXZpaWJ5RThiMXZuQ1MybFElM0QlM0Q; _ga_YD7QXHZJ4Y=GS1.1.1702171947.1.1.1702172062.0.0.0; _ga_Y4GN1R87RG=GS1.1.1702171948.3.1.1702172062.0.0.0; _pk_id.100001.2939=23fb1116456f2945.1702181127.; __yadk_uid=IG3yWBrT25a5voDknmjWyvbI8e2gWUf3; __utmz=30149280.1702188613.6.3.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/celebrity/1352362/; _pk_ref.100001.2939=%5B%22%22%2C%22%22%2C1702379326%2C%22https%3A%2F%2Fmovie.douban.com%2Fcelebrity%2F1352362%2F%22%5D; _pk_ses.100001.2939=1; ap_v=0,6.0; __utma=30149280.191779183.1701751376.1702188613.1702379330.7; __utmc=30149280; dbcl2="65813696:ATM4RixqcdE"; ck=Bp8_; push_noty_num=0; push_doumail_num=0; __utmt=1; __utmv=30149280.6581; __gads=ID=a9b321e888688167:T=1702171894:RT=1702380648:S=ALNI_MbJAOSJsVQBSYsoHKK1YgOhrt4-vg; __gpi=UID=00000ca895d8a964:T=1702171894:RT=1702380648:S=ALNI_MY587WTpStdnaM_AGYG1dCqa678-w; __utmb=30149280.9.10.1702379330""",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    # 发送请求
    r = requests.get(url, headers=headers)
    status = r.status_code
    if status == 200:
        soup = BeautifulSoup(r.content.decode('utf-8'),"html.parser",from_encoding="utf-8")

        # a = soup.find('div', class_='item-root')
        a = soup.find('div', class_='result-list')
        if a is None:
            print(f"fail soup find for {search_text}")
            return None
        num = len(a)
        if num == 0:
            print('request succ, but null result')
        else:
            href = a.find('a', href=True)
            # print(item)
            # link = item.find_all('a', href=True, text=True)
            link = href['href'].split('?url=')[-1].split('%2F&query=')[0]
            uq_link = unquote(link)
            return uq_link
    else:
        print(f"Request failed, code:{status}")
    return None



input_fp = open("norm_三大奖获奖电视剧列表.csv", 'r')
output_fp = open("三大奖获奖电视剧豆瓣链接.csv", 'w')

out_map = {}
i = 1
for text in input_fp.readlines():
    text = text.strip()
    link = get_uq_link(text)
    if link is not None:
        if link not in out_map:
            idx = len(out_map) + 1
            out_map[text] = link
            vid = link.split('/')[-1]
            output_fp.write(f'{vid},{text},{link}\n')
            print(f'{idx},{vid},{text},{link}\n')

input_fp.close()
output_fp.close()
