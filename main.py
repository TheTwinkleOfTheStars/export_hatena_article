#! /usr/bin/env python
from glob import glob
import datetime
import os
import pandas as pd
from bs4 import BeautifulSoup

DATA_DIR = "data/"
CSV_OUTPUT_DIR = "csv_output/"
HTML_OUTPUT_DIR = "html_output/"

def get_text_from_mv():
    """mv形式のtxtファイル名とテキストを得る。
    
        Note: txtファイルが1つだけ格納されていることを前提としている。
    """
    flist = glob(f"{DATA_DIR}*.txt")
    txt_text, txt_fname = None, None
    if not flist:
        print(f"txtファイルを{DATA_DIR}に格納してください。")
    elif len(flist) >= 2:
        print(f"txtファイルが{DATA_DIR}に2つ以上格納されています。対象ファイルを1つだけ格納してください。")
    else:
        txt_fname = flist[0]
        with open(txt_fname, 'r', encoding='utf-8') as file:
            txt_text = file.read()
    return txt_text, txt_fname

def get_info_from_one_article(one_article):
    """1記事から属性ごとの情報に関する辞書を得る。
    
        Note: txtファイル内の区切り文字"-----"を参照した実装のため、
        タイトルや本文等に"-----"を含むと正しく動作しない可能性がある。    
    """
    other_text, main_text = one_article.split("-----")[:2]
    # 不要な文字列を削除
    main_text = main_text.replace("BODY:\n", "")

    info_dict = {}
    for info_one_line in other_text.splitlines()[1:]:
        idx = info_one_line.find(":")
        info_dict[info_one_line[:idx]] = info_one_line[idx+2:]

    # 本文
    soup = BeautifulSoup(main_text, 'html.parser')
    info_dict["MAIN_TEXT"] = soup.get_text()

    # html作成のために用いるのでhtmlのままのものも保存しておく。
    date = info_dict.get("DATE", "no_date")
    title = info_dict.get("TITLE", "")
    try:
        date = datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S")
        ymd = date.strftime("%Y年%m月%d日")
    except ValueError:
        ymd = ""
    # 文字化け防止 & 年月+タイトルを冒頭に追加
    info_dict["TEXT_HTML"] = f'<meta charset="UTF-8">\n<h1>{ymd} {title}</h1>\n' + main_text
    return info_dict

def save_one_article_as_html(info_dict: dict):
    """1記事を1つのhtmlファイルとして保存する。
    
        Note:
            - ファイル格納先: HTML_OUTPUT_DIR/YYYYMM/ (自動で作成される)
            - ファイル名: YYYY年MM月DD日_{TITLE}.html
    """
    try:
        title = info_dict.get("TITLE", "no_title")
        date = info_dict.get("DATE", "no_date")
        main_text = info_dict.get("TEXT_HTML", "no_text")
        # フォルダの作成等のため、YYYYMM, YYYY年MM月DD日を取得する。
        try:
            # 文字列をdatetimeオブジェクトに変換
            date = datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S")
            # YYYYMMDD形式に変換
            ymd = date.strftime("%Y年%m月%d日")
            ym = date.strftime("%Y%m")
        except ValueError:
            ymd = ""
            ym = "no_date"
        # 年月別のフォルダを作成してhtmlファイルとして保存
        output_dir = f"{HTML_OUTPUT_DIR}/{ym}"
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/{ymd}_{title}.html", 'w') as f:
            f.write(main_text) # 不要な文字列を除去
    except Exception as e:
        print(e)
        print(f"html保存失敗: {date}: {title}")

def get_info_from_all_articles(content, txt_fname, is_html_save=False):
    """txtファイル内のテキストから情報を抽出し、1つのcsvファイルと記事ごとのhtmlファイルを出力する。
    
        Note:
            - ファイル格納先: HTML_OUTPUT_DIR/YYYYMM/ (自動で作成される)
            - ファイル名: YYYY年MM月DD日_{TITLE}.html
    """
    if content is None:
        return None

    info_dicts = []
    for one_article in content.split("--------")[:-1]:
        info_dict = get_info_from_one_article(one_article)
        info_dicts.append(info_dict)
        if is_html_save:
            save_one_article_as_html(info_dict)

    df = pd.json_normalize(info_dicts)
    df["DATE"] = pd.to_datetime(df["DATE"])
    csv_fname = os.path.splitext(os.path.basename(txt_fname))[0]
    df[["DATE", "TITLE", "MAIN_TEXT"]].to_csv(f"{CSV_OUTPUT_DIR}{csv_fname}.csv", encoding="utf-8-sig")

if __name__ == "__main__":
    for dir in [DATA_DIR, CSV_OUTPUT_DIR, HTML_OUTPUT_DIR]:
        os.makedirs(dir, exist_ok=True)
    
    txt_text, txt_fname = get_text_from_mv()
    get_info_from_all_articles(txt_text, txt_fname, is_html_save=True)