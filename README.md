# sort-font
このアプリケーションは、入力された文字画像に使われているフォントと似ているフォントを提示するアプリケーションです。

![demo.gif](./assets/demo.gif)

## 実行方法
- 本アプリケーションでは `Make` コマンドの利用を推奨します

### ローカルで実行する場合
#### Setup
```bash
make init
```

#### Linux/Mac
```bash
make setup
```

#### Windows(Powershell)
```powershell
make setup/powershell
```

### Dockerで実行する場合
```bash
make docker/build
make docker/run
```

## 言語・ライブラリ等
- Python3
  - [requirements.txt](./requirements.txt)
- HTML/CSS