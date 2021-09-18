# sort-font
![CI](https://github.com/sort-font/webpage/workflows/CI/badge.svg)

このアプリケーションは、入力された文字画像に使われているフォントと似ているフォントを提示するアプリケーションです。

![demo.gif](./docs/demo.gif)

## 開発環境のセットアップ方法
本アプリケーションは、ローカルでの起動とDockerコンテナを用いた軌道が可能です。
実行すべきコマンドや設定方法の詳細は、[setup.md](./docs/setup.md)をご確認ください。

## アプリケーション構成
本アプリケーションは、Flaskでファイルをサーブし、フォントの判定にはKerasを用いる構成です。アプリケーションでのデータの流れや各ディレクトリの詳細は、[architecture.md](./docs/architecture.md)をご確認ください。


## 言語・ライブラリ等
- Python3
  - [requirements.txt](./requirements.txt)
- HTML/CSS/JavaScript