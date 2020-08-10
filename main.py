import requests, bs4, re

url = "https://www.books.com.tw/web/sys_newtopb/books/"
html = requests.get(url)
if html.status_code != 200:
    print('網址無效:', html.url)
    quit()

patten = re.compile('.{3}\-.{3}\>.{3}')  # 網頁標題:博客來-中文書>新書榜
title = patten.search(html.text)
print(title.group())

soup = bs4.BeautifulSoup(html.text, 'html.parser')
books = []
total = soup.select_one("div.mod_a.clearfix > ul.clearfix")  # 進到item上面的標籤
bang = total.find_all("li", {"class": "item"})  # 取得所有<li class:item>(包含item last)
for i in range(0, 100):
    top = bang[i].select_one("div.stitle").text
    title = bang[i].select_one("div.type02_bd-a > h4").text
    author = bang[i].select_one("div.type02_bd-a > ul > li")
    if author is None:  #判斷有沒有作者
        author_text = "不明"
    else:
        author_text = author.text
    price = bang[i].select_one("div.type02_bd-a > ul > li.price_a > strong:nth-of-type(2)")
    if price is None:  # 判斷是不是沒有第二個strong 代表沒有打折 所以改拿第一個strong 拿到沒有打折的售價
        price_text = bang[i].select_one("div.type02_bd-a > ul > li.price_a > strong:nth-of-type(1)").text
    else:
        price_text = price.text
    # top.strip因為標籤有p 有換行符號
    book = {"rank": top.strip(), "title": title, "author": author_text, "price": price_text}
    books.append(book)

for j in range(len(books)):
    print('{} {} {} 價格:{}'.format(books[j]["rank"], books[j]["title"], books[j]["author"], books[j]["price"]))
