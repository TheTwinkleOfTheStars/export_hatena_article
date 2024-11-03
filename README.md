# はてなブログのエクスポートファイルの整形

## はじめに
はてなブログは、ブログの記事データをtxtファイルとしてエクスポートできる([参照](https://help.hatenablog.com/entry/export))。このファイルはMT(Movable Type)形式で書き出されており、ファイル内に各記事の情報が保持されている。

このtxtファイルを整形し、csvファイル、htmlファイルとして出力する。


## ディレクトリ構成
```
.
├── README.md
├── data
├── get_info.py
├── poetry.lock
├── pyproject.toml
└── sample.hatenablog.com.export.txt
```

## PoetryによるPythonの環境構築
Poetryを使用してPythonのパッケージを行う。

#### 前提条件
- Python 3.12がインストールされていること。

### Poetryのインストール
- Poetryをインストールする。
```
    curl -sSL https://install.python-poetry.org | python3 -
```
以下のように表示されたら、表示にしたがってコマンドを入力する。
```
To get started you need Poetry's bin directory (/Users/beginning/.local/bin) in your `PATH`
environment variable.

Add `export PATH="/Users/[Username]/.local/bin:$PATH"` to your shell configuration file.
```
- `poetry --version`と入力し、Pooetryのバージョンが表示されればインストール完了。

### 仮想環境の作成
- プロジェクトのディレクトリに移動する。
- `pyproject.toml`と`poetry.lock`を基に必要なパッケージをインストールし、仮想環境を設定する。
```
    poetry install
```

### 仮想環境のアクティベート、ライブラリのインストール
- 仮想環境をアクティベートする。
```
    poetry shell
```
- 必要なライブラリをインストールする。
```
    poetry install --no-dev
```

## 実行方法
- ターミナルを起動する。
- 仮想環境をアクティベートする。
```
    poetry shell
```
- `main.py`を実行する。
```
    python main.py
```
- `main.py`の実行が完了すると、`csv_output/`ディレクトリ内にcsvファイルが出力され、`html_output/`ディレクトリにhtmlファイルが出力される。