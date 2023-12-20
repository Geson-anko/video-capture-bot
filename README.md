# Video Recording Bot

定期的に動画を撮影し、ディスコードのチャネルに投稿するDiscord BOTです。

## Installation

### Prerequirements

- OBS (See <https://obsproject.com>)
- git
- ffmpeg
- python3 (3.10 >=)
- pip
- poetry

```bash
sudo apt install -y git ffmpeg python3 python3-pip && sudo pip3 install poetry
```

### インストール

1. このリポジトリをクローンし、プロジェクトフォルダに入る。
2. pythonの依存関係をインストールする。
   ```bash
   poetry install
   ```

## 使い方

### OBS 設定

1. 録画したいものをキャプチャする。
2. `ツール(Tools)`から `WebSocketサーバ設定`を選択し、WebSocketサーバを有効にする。
3. サーバポートが`4455`になっていることを確認する。
4. 認証（サーバーパスワード）を設定する場合は、パスワードのメモを取っておく。

### Discord Botの設定

1. Discord BotのTOKENを取得する。
2. 開発者モードにしたDiscordで投稿したいチャネルを右クリックし、チャネルIDを取得する。

### `.env`ファイル（環境変数）を設定する

BOTのトークンなどの機密情報を漏洩しないために、`.env`ファイルを作成する。

1. [`.env.example`](/.env.example)を複製し、`.env`ファイルという名前にする。
2. `.env`ファイルにDiscordbotのトークン、投稿先のチャネルID、OBS Websocket Serverのパスワードを記述する。

### Bot を起動する

1. `poetry shell`をこのプロジェクトのディレクトリで実行する。
2. `python bot.py --post-message "Hello, I'm Video Recording BOT!"`

### コマンドライン引数

全てのコマンド引数のリストは `python bot.py -h`を実行してください。
