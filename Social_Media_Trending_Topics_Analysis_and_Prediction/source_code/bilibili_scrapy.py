from bs4 import BeautifulSoup           #网页解析，获取数据
import re                               #正则表达式，进行文字匹配
import urllib.request,urllib.error      #指定URL，获取网页数据
import xlwt                             #进行excel操作

def main():

#     1. 获取网页
    baseurl = "https://www.bilibili.com/v/popular/rank/all"
#     2. 获取和解析数据
    datalist = getData(baseurl)
#     3. 保存数据
    savepath = "./b站热门视频.xls"
    saveData(datalist,savepath)
    ssl._create_default_https_context = ssl._create_unverified_context
    context = ssl._create_unverified_context()

    urllib2.urlopen(context=context)
    try:
        r = requests.get(url, headers=headers, cookies=cookie)
    except requests.exceptions.SSLError as err:
        print(err)
        r = requests.get(url, headers=headers, cookies=cookie, verify=False)


findLink = re.compile(r'<a href="(.*?)" target="_blank">')
findName = re.compile(r'<a class="title" href=".*?" target="_blank">(.*)</a>')
findPlay = re.compile(r'<span class="data-box"><i class="b-icon play"></i>(.*?)</span>',re.S)
findView = re.compile(r'<span class="data-box"><i class="b-icon view"></i>(.*?)</span>',re.S)
findUP = re.compile(r'<span class="data-box up-name"><i class="b-icon author"></i>(.*?)</span>',re.S)
findGrades = re.compile(r'<div class="pts"><div>(.*?)</div>')



def getData(baseurl):
    datalist = []
    html = askURL(baseurl)
    # print(html)
    soup = BeautifulSoup(html, "html.parser")  # 形成树形结构对象
    for item in soup.find_all("div",class_="content"):
        # print(item)
        data = []
        item = str(item)
        # 视频链接
        link = re.findall(findLink,item)[0]
        data.append(link)
        # 视频名字
        name = re.findall(findName,item)[0]
        data.append(name)
        # 播放量
        play = re.findall(findPlay,item)[0]
        # print(play)
        data.append(play)
        # 评论数
        view = re.findall(findView,item)[0]
        # print(view)
        data.append(view)
        # UP个人空间链接
        uplink = re.findall(findLink,item)[1]
        # print(uplink)
        data.append(uplink)
        # UP主
        UP = re.findall(findUP,item)[0]
        # print(UP)
        data.append(UP)
        # 综合得分
        grades = re.findall(findGrades,item)[0]
        # print(grades)
        data.append(grades)
        datalist.append(data)

    return datalist



def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("B站热门",cell_overwrite_ok=True)
    col = ("排名","视频链接","视频名字","播放量","评论数","UP个人空间链接","UP主","综合得分")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,50):
        print("第%d条"%i)
        data = datalist[i]
        sheet.write(i+1,0,i+1)
        # print(data)
        for j in range(0,7):
            sheet.write(i+1,j+1,data[j])

    book.save(savepath)  # 保存数据表



def askURL(url):
    head = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "referer": "https: // www.bilibili.com /",
        "cookie": "_uuid=D3D1D709-07B0-0088-6B22-2DF2B38C600034103infoc; buvid3=D062BC64-9B52-4B58-9A58-E11498DB186313434infoc; sid=k806w948; blackside_state=1; rpdid=|(J~RYkluJ|)0J'uYklYlYu~l; PVID=1; CURRENT_QUALITY=116; fingerprint=5baec738e814efcfee02e2c27da99952; buvid_fp_plain=A777C3F8-7EC1-40FB-80A9-E89C46AEF71018557infoc; buvid4=4D94022B-3766-548C-1A52-47EF991AD56500954-022030717-s1JeiAveeisD+vB8L/P6RA%3D%3D; buvid_fp=09f6089b92beabb866538642ed7079e4; CURRENT_FNVAL=4048; innersign=0; b_lsid=71CCCE99_17F6DED82A4"
'''        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec - ch - ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        "sec - ch - ua - mobile": "?0",
        "sec - ch - ua - platform": '"macOS"',
        "sec - fetch - dest": "document",
        "sec - fetch - mode": "navigate",
        "sec - fetch - site": "none",
        "sec - fetch - user": "?1",
        "upgrade - insecure - requests": "1"'''
    }

    request = urllib.request.Request(url,headers = head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e,"code")
        if hasattr(e,"reason"):
            print(e,"reason")
    return html




if __name__ == "__main__":  #程序执行时
    #调用函数
    main()
    print("爬取完毕！")

