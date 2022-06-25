import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re


if __name__ == '__main__':

    headers = Headers(browser="chrome", os="win").generate()
    base_url = "https://habr.com"
    res_url = base_url + "/ru/all/"
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']

    response = requests.get(res_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    list_articles = soup.findAll(class_="tm-articles-list__item")
    result = []
    for articl in list_articles:
        title = articl.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").find("span").text
        date = articl.find(class_="tm-article-snippet__datetime-published").time.attrs.get("title")
        link = articl.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").a.attrs.get("href")

        full_link = base_url + link
        res_articl = requests.get(full_link, headers=headers)
        soup_articl = BeautifulSoup(res_articl.text, 'html.parser')
        post = soup_articl.find(id="post-content-body").find(xmlns="http://www.w3.org/1999/xhtml").text
        words_post = set(re.findall("\w+", post, re.I))
        intersection = words_post.intersection(KEYWORDS)
        if intersection:
            print(f"{date} - {title} - {full_link}")
            info_articl = {"дата": date, "заголовок": title, "ссылка": full_link}
            result.append(info_articl)

    with open("result.txt", "w", encoding="utf-8") as file:
        for articl in result:
            line = f"{articl['дата']} - {articl['заголовок']} - {articl['ссылка']}\n"
            file.writelines(line)
