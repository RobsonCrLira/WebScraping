import requests
import pandas as pd
from bs4 import BeautifulSoup


def post_pesquisa(url_pesquisa):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/83.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "DNT": "1",
               "Connection": "close",
               "Upgrade-Insecure-Requests": "1"}

    r = requests.get(url_pesquisa, headers)
    content = r.content
    all_post = []
    if r.status_code == 200:
        soup = BeautifulSoup(content, 'html.parser')
        for post in soup.findAll('div', attrs={'class': "a-section a-spacing-medium"}):
            nome = ""
            valor = ""
            if post.find('span', attrs={'class': "a-size-base-plus a-color-base a-text-normal"}) is not None:
                nome = post.find('span', attrs={'class': "a-size-base-plus a-color-base a-text-normal"}).text
            else:
                nome = "Nome não encontrado"

            if post.find('span', attrs={'class': "a-offscreen"}) is not None:
                valor = post.find('span', attrs={'class': "a-offscreen"}).text
            else:
                valor = "0"
            all_post.append({'Descricao': nome, "Valor": valor})
    else:
        print(f'Problemas de conexao {r.status_code} - {r.text}')
    return all_post


if __name__ == "__main__":
    url_amazon = 'https://www.amazon.com.br/s?k=iphone&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss'
    posts = post_pesquisa(url_amazon)

    df = pd.DataFrame(data=posts, columns=['Descricao', 'Valor'])
    resp = df.set_index('Descricao')
    resp.to_excel("amazon.xlsx")
    resp.to_csv("amazon.csv", sep=";")
