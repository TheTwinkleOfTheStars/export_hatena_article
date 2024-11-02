# はてなブログの記事データを元にcsv / htmlファイルを作成する

## はじめに
はてなブログでは、ブログの記事データをtxtファイルとして書き出すことができる。このtxtファイルはMT(Movable Type)形式で書き出されたものであり、ファイル内に各記事の情報が保持されている。

この記事情報を取得し、各記事の日付、タイトル、本文等を1つのcsvに書き出す。
また、記事ごとにHTMLファイルとして書き出す。


## ツリー
```
.
├── README.md
├── data
├── get_info.py
├── poetry.lock
├── pyproject.toml
└── sample.hatenablog.com.export.txt
```