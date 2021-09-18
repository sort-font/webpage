## 開発環境のセットアップ方法
本アプリケーションは、`make` コマンドの利用を推奨しています。
`make` コマンドがない場合、インストールするか `Makefile` で定義されているコマンドを直接実行してください。

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
