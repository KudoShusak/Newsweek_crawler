import re
import requests
import time
import os
from datetime import datetime
import json
from bs4 import BeautifulSoup

# クローリングを開始するURL
start_url = "https://www.newsweekjapan.jp/"

prefix = '{:%Y%m%d_%H%M%S}_'.format(datetime.now())

# クローリング結果保存ファイル
result_file = f"{prefix}newsweekjapan_cwlLog.jsonl"

# テキストデータ保存ファイル
text_file = f"{prefix}newsweekjapan.jsonl"

# 取得したhtmlのリストを保存するファイル
logfile = f"{prefix}newsweekjapan_html_list.jsonl"

# htmlファイルの名前
sub_filename = "_newsweekjapan_article.html"

# htmlファイルを保存するディレクトリ（フォルダ）
directory = f'{prefix}html'
os.mkdir(directory)

# エラーログファイル
errorlog = f'{prefix}error.log'

# データ取得前に待つ時間
sleeptime = 3

# ループ回数
loop = 8

#### テキスト抽出 ####
# News week 記事 ＆ コラム

## 各ページの本文を抽出
def sub_gettext(soup):

    bodyhtmllist = []
    bodytxtlist = []
    body = soup.find('div', class_='entryDetailBodyCopy')
    # 【関連記事】があれば削除
    relatedlink = body.find('div', class_='related-link-elm')
    if relatedlink != None :
        relatedlink.decompose()
    else :
        relatedlink = body.find('div', class_='related-link-elm-lastpage')
        if relatedlink != None :
            relatedlink.decompose()
    # 新刊雑誌の広告文を削除
    magazineinfo = body.find('div', id='magazine-info')
    if magazineinfo != None :
        magazineinfo.decompose()
    # 記事下段の記事以外の部分を削除
    entryPagenate = body.find('div', class_='entryPagenate')
    if entryPagenate != None :
        entryPagenate.decompose()

    for bodyhtml in body.find_all(['p','h2','h3','h4']) :
        # 写真のキャプションを削除
        if '<img ' in str(bodyhtml) :
            continue
        bodyhtmllist.append(bodyhtml)
        bodytxtlist.append(bodyhtml.text)

    return [bodyhtmllist, bodytxtlist]

## 一つの記事が複数のページに渡っているので、順番に記事を抽出する
def gettext(soup,url,count):

    txthtmllist = []
    txtlist = []

    sub_url_list = []

    # この記事が何ページあるか調べる
    index = soup.find('ul', class_='indexNavi clearfix')

    if index != None :
        index_num = index.find_all('li', class_="indexNum")
        if len(index_num) == 0 :
            # コラムの場合ページ数取り直し
            index_num = index.find_all('li')
        for num in index_num :
            page_a = num.find('a')
            if page_a != None :
                if not "Next" in page_a.text:
                    page = str(int(page_a.text))
                    sub_url = url.replace('.php','') + f'_{page}.php'
                    sub_url_list.append(sub_url)

    # タイトル取得
    title = soup.find('h1')
    txtlist.append(title.text)

    bodytxtlist = sub_gettext(soup)

    num = 2
    for sub_url in sub_url_list :
        time.sleep(sleeptime) # データ取得前に少し待つ
        headers = {'User-Agent':'Mozilla/5.0'}
        html = requests.get(sub_url, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")

        sub_bodytxtlist = sub_gettext(soup)

        bodytxtlist[0].extend(sub_bodytxtlist[0])
        bodytxtlist[1].extend(sub_bodytxtlist[1])

        # ファイルに保存
        filename = str(count+1).zfill(5) + '-%s'%str(num) + sub_filename
        num += 1
        filepath = os.path.join(directory,filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(html.text))
        f.close()

        # ファイル名とurlのセットを記録しておく
        logdata = {'filename': filename, 'url': sub_url}
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(json.dumps(logdata)+'\n')
        f.close()


    txthtmllist = bodytxtlist[0]
    txtlist.extend([s for s in bodytxtlist[1] if s != ''])

    return [txthtmllist,txtlist]

#### テキスト抽出 ####
# worldvoiceは、少しだけフォーマットが違う

## 各ページの本文を抽出
def sub_getworldtext(soup):

    bodyhtmllist = []
    bodytxtlist = []
    body = soup.find('div', class_='wv-entry-body')
    # 【関連記事】があれば削除
    relatedlink = body.find('div', class_='related-link-elm')
    if relatedlink != None :
        relatedlink.decompose()
    else :
        relatedlink = body.find('div', class_='related-link-elm-lastpage')
        if relatedlink != None :
            relatedlink.decompose()
    # 新刊雑誌の広告文を削除
    magazineinfo = body.find('div', id='magazine-info')
    if magazineinfo != None :
        magazineinfo.decompose()
    # 記事下段の記事以外の部分を削除
    entryPagenate = body.find('div', class_='entryPagenate')
    if entryPagenate != None :
        entryPagenate.decompose()

    for bodyhtml in body.find_all(['p','h2','h3','h4']) :
        # 写真のキャプションを削除
        if '<img ' in str(bodyhtml) :
            continue
        bodyhtmllist.append(bodyhtml)
        # <br/>を'\n'に置換
        for br in bodyhtml.find_all('br') :
            br.replace_with('\n')
        # 空行は削除
        textline = re.sub('\n[\n]+','\n', bodyhtml.text)
        textline = re.sub('^\n[\n]*','', textline)
        bodytxtlist.append(textline)

    return [bodyhtmllist, bodytxtlist]

## 複数のページに渡る記事を、順番に抽出する
def getworldtext(soup,url,count):

    txthtmllist = []
    txtlist = []

    sub_url_list = []

    # この記事が何ページあるか調べる
    index = soup.find('div', class_='wv-pager list-pager')

    if index != None :
        index_num = index.find_all('li', class_="indexNum")
        for num in index_num :
            page_a = num.find('a')
            if page_a != None :
                page = str(int(page_a.text))
                sub_url = url.replace('.php','') + f'_{page}.php'
                sub_url_list.append(sub_url)

    # タイトル取得
    title = soup.find('h3')
    txtlist.append(title.text)

    bodytxtlist = sub_getworldtext(soup)

    num = 2
    for sub_url in sub_url_list :
        time.sleep(sleeptime) # データ取得前に少し待つ
        headers = {'User-Agent':'Mozilla/5.0'}
        html = requests.get(sub_url, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")

        sub_bodytxtlist = sub_getworldtext(soup)

        bodytxtlist[0].extend(sub_bodytxtlist[0])
        bodytxtlist[1].extend(sub_bodytxtlist[1])

        # ファイルに保存
        filename = str(count+1).zfill(5) + '-%s'%str(num) + sub_filename
        num += 1
        filepath = os.path.join(directory,filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(html.text))
        f.close()

        # ファイル名とurlのセットを記録しておく
        logdata = {'filename': filename, 'url': sub_url}
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(json.dumps(logdata)+'\n')
        f.close()


    txthtmllist = bodytxtlist[0]
    txtlist.extend([s for s in bodytxtlist[1] if s != ''])

    return [txthtmllist,txtlist]

#### テキスト抽出 ####
# アスティオンも、少しだけフォーマットが違う（worldvoiceと、一つの関数にまとめられそう）
def sub_getasteiontext(soup):

    bodyhtmllist = []
    bodytxtlist = []
    body = soup.find('div', class_='entryDetailBodyBlock')
    # 【関連記事】があれば削除
    relatedlink = body.find('div', class_='related-link-elm')
    if relatedlink != None :
        relatedlink.decompose()
    else :
        relatedlink = body.find('div', class_='related-link-elm-lastpage')
        if relatedlink != None :
            relatedlink.decompose()
    # 新刊雑誌の広告文を削除
    magazineinfo = body.find('div', id='magazine-info')
    if magazineinfo != None :
        magazineinfo.decompose()
    # 記事下段の記事以外の部分を削除
    entryPagenate = body.find('div', class_='entryPagenate')
    if entryPagenate != None :
        entryPagenate.decompose()

    for bodyhtml in body.find_all(['p','h2','h3','h4']) :
        # 写真のキャプションを削除
        if '<img ' in str(bodyhtml) :
            continue
        bodyhtmllist.append(bodyhtml)
        # <br/>を'\n'に置換
        for br in bodyhtml.find_all('br') :
            br.replace_with('\n')
        # 空行は削除
        textline = re.sub('\n[\n]+','\n', bodyhtml.text)
        textline = re.sub('^\n[\n]*','', textline)
        bodytxtlist.append(textline)

    return [bodyhtmllist, bodytxtlist]

## 複数のページに渡る記事を、順番に抽出する
def getasteiontext(soup,url,count):

    txthtmllist = []
    txtlist = []

    sub_url_list = []

    # この記事が何ページあるか調べる
    index = soup.find('ul', class_='indexNavi clearfix')

    if index != None :
        index_num = index.find_all('li', class_="")
        for num in index_num :
            page_a = num.find('a')
            if page_a != None :
                page = str(int(page_a.text))
                sub_url = url.replace('.php','') + f'_{page}.php'
                sub_url_list.append(sub_url)

    # タイトル取得
    title = soup.find('h1')
    txtlist.append(title.text)

    bodytxtlist = sub_getasteiontext(soup)

    num = 2
    for sub_url in sub_url_list :
        time.sleep(sleeptime) # データ取得前に少し待つ
        headers = {'User-Agent':'Mozilla/5.0'}
        html = requests.get(sub_url, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")

        sub_bodytxtlist = sub_getasteiontext(soup)

        bodytxtlist[0].extend(sub_bodytxtlist[0])
        bodytxtlist[1].extend(sub_bodytxtlist[1])

        # ファイルに保存
        filename = str(count+1).zfill(5) + '-%s'%str(num) + sub_filename
        num += 1
        filepath = os.path.join(directory,filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(html.text))
        f.close()

        # ファイル名とurlのセットを記録しておく
        logdata = {'filename': filename, 'url': sub_url}
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(json.dumps(logdata)+'\n')
        f.close()


    txthtmllist = bodytxtlist[0]
    txtlist.extend([s for s in bodytxtlist[1] if s != ''])

    return [txthtmllist,txtlist]


#### JSONL形式で保存 ####

# save_dataをJSON形式でresult_fileに追記する。
def save_result(cont_txt, url="None", filename=result_file):

    save_data = {"url":url, "contents": [str(cont_txt[0]), cont_txt[1]]}
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(save_data, ensure_ascii=False) + '\n')
    f.close()

    return

# テキストデータのlistを指定の形式でtext_fileに追記する
def save_text(textlist, url="None", filename=text_file):

    jointxt = '\n'.join(textlist)
    save_data = {"url" : url, "text" : jointxt}

    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(save_data, ensure_ascii=False) + '\n')
    f.close()

    return

#### クローリング ####

# アクセスするURL(初期値はクローリングを開始するURL)
url = start_url
urllist = [url]

# クロール済みリスト
crawledlist = []

count = 0
for i in range(loop):
    print(f'{i + 1}階層目クローリング開始') # 動作確認用

    linklist = []
    # 対象ページのhtml取得
    for url in urllist:
        #　同じURLを何度もクロールしない
        if url in crawledlist:
            continue

        time.sleep(sleeptime) # データ取得前に少し待つ

        crawl_flg = False
        try:
            headers = {'User-Agent':'Mozilla/5.0'}
            html = requests.get(url, headers=headers)
            soup = BeautifulSoup(html.content, "html.parser")

            # 次のループで使うURLの候補として<a>タグのリストをため込む
            for tag_a in soup.find_all("a") :
                linklist.append(str(tag_a))

            ## テキスト抽出
            if '/stories/' in url and '.php' in url :
                # 通常の記事
                cont_txt = gettext(soup,url,count)
                crawl_flg = True
                print('記事　 : ', end='' )
            elif '/worldvoice/' in url and '.php' in url :
                # worldvoice
                cont_txt = getworldtext(soup,url,count)
                crawl_flg = True
                print('world　 : ', end='' )
            elif '/asteion/' in url and '.php' in url :
                # アスティオン
                cont_txt = getasteiontext(soup,url,count)
                crawl_flg = True
                print('asteion: ', end='' )
            else :
                article_url = re.search(r'.*?jp/[a-z]+?/[0-9]+?/[0-9]+?/post-.+?php', url)
                if article_url != None :
                    # コラム
                    cont_txt = gettext(soup,url,count)
                    crawl_flg = True
                    print('コラム : ', end='' )
            
            if crawl_flg == True :
                crawl_flg = False
                count += 1

                # テキスト抽出結果を保存
                save_result(cont_txt, url=url, filename = result_file)
                save_text(cont_txt[1], url=url, filename = text_file)
                print(count, cont_txt[1]) # 動作確認用

                # 取得したhtmlをファイルに保存
                filename = str(count).zfill(5) + '-1' + sub_filename
                filepath = os.path.join(directory,filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(html.text))
                f.close()

                # ファイル名とurlのセットを記録しておく
                logdata = {'filename': filename, 'url': url}
                with open(logfile, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(logdata)+'\n')
                f.close()

        except:
            # 何かエラーが出てもとりあえず続ける
            print(f'Error: {url}') # 動作確認用
            # エラーをログファイルに記録
            now = '{:%Y.%m.%d %H:%M:%S}'.format(datetime.now())
            with open(errorlog, 'a', encoding='utf-8') as f:
                f.write(f'"time" :"{now}", "Error": "{url}"\n')
            f.close()
            continue

# 使い終わったurllistをクロール済みリストに追加
    crawledlist.extend(urllist)
    crawledlist = list(set(crawledlist)) # 重複削除

    # 次のループのためのurllistを作る

    urllist = []
    for link in linklist:
        for url in re.findall('<a.+?href="(.+?)".*?>', str(link)):
            # 同じ記事を何度もクロールしないように'?'と'#'の後の文字列を削除
            url = re.sub('[?#].+','',url)
            # 記事の2ページ以降のリンクはトップへ
            url = re.sub('_[0-9]+.php','.php',url)
            # 先頭が'/'の場合は、'https://www.newsweekjapan.jp'を追加
            if len(url) != 0:
                if url[0] == '/' :
                    url = f'https://www.newsweekjapan.jp{url}'
            # NewsWeek for womanのURLには、'..'が使われることが多い
            # 重複回避のため、修正する
            url = url.replace('/woman/..', '')
            # URLに混入する'\'を削除
            url = url.replace('\\', '')
            
            if 'https://www.newsweekjapan.jp' in url :
                if not '/category_admin/' in url :
                    urllist.append(url)

    # 新着記事が載るページを追加
    fixedlist = ['https://www.newsweekjapan.jp/stories/','https://www.newsweekjapan.jp/column/','https://www.newsweekjapan.jp/worldvoice/','https://www.newsweekjapan.jp/asteion/']
    urllist.extend(fixedlist)
    urllist = list(set(urllist)) # 重複削除

    # クロール済みリストから、新着記事が載るページを削除
    for fixed in fixedlist:
        crawledlist= [s for s in crawledlist if s != fixed]
