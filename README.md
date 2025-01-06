# Ediloader

## About

EDINET 書類一覧 API(提出書類一覧及びメタデータ)を実行し、メタデータを Google Cloud へロードするスクリプト

## How to execute

実行に必要な環境変数を設定する。

```sh
export PROJECT_ID=<project id>
export EDINET_API_KEY=<edinet api key>
export BUCKET_NAME=<bucket name of metadata>
```

依存ライブラリをダウンロードする。

```sh
pip install -r requirements.txt
```

実行する。(Python 3.12+)

```sh
python3 main.py
```
