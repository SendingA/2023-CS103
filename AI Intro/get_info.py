import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tqdm import tqdm

requests.packages.urllib3.disable_warnings()
ua = UserAgent()
headers = {
            "User-Agent": ua.random,
            "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language" : "zh-CN,zh;q=0.9",
            "Accept-Encoding" : "gzip, deflate, br",
        }

def get_id_list(start=1, end=10):
    """按页获取id，可以输入获取页数的范围，返回id列表"""

    id_list = []
    for page in tqdm(range(start, end+1), desc="Getting id"):
        response = requests.get(f"https://www.sustech.edu.cn/zh/events-{page}.html", headers=headers, verify=False)
        soup = BeautifulSoup(response.text, features="html.parser")
        for a in soup.find_all(name="a", attrs={"class": ["boor-l", "fl"]}):
            id = a.attrs["href"].split("/")[-1].split(".")[0]
            id_list.append(int(id))
    print("Finish.")
    return id_list


def get_info(id):
    """根据详情页的网址中的id，获取infomation，将infomation构造成dict返回"""

    info = {"id": id}
    url = f"https://www.sustech.edu.cn/zh/events/{id}.html"
    info["url"] = url
    response = requests.get(url, headers=headers, verify=False)
    if response.text == "404":
        return None
    
    soup = BeautifulSoup(response.text, features="html.parser")

    # 获取标题
    info["title"] = soup.find("h1").text

    # 获取演讲人、时间、地点
    for i, j in zip(["presenter", "time", "location"], 
                    soup.find_all(name="i", attrs={'class': ["vc_icon_element-icon", "fa"]})):
        info[i] = j.parent.text.split("：")[1]
    
    # 获取图片
    for img in soup.find_all("img"):
        if img.parent.name == "p":
            img_url = "https://www.sustech.edu.cn" + img.attrs["src"]
            info["poster"] = img_url
    
    return info


def get_info_list(id_list, save=True):
    """批量获取info，可保存为json文件"""
    info_list = []
    for id in tqdm(id_list, desc="Getting info"):
        info_list.append(get_info(id))
    print("Finish.")
    
    # 保存为json格式
    if save:
        import json
        # encoding和ensure_ascii防止乱码
        with open("info_list.json", mode="w", encoding="utf-8") as f:
            json.dump(info_list, f, ensure_ascii=False, indent=4)

