# efFEctive

## アプリ概要
**efFEctive** は、基本情報技術者試験をはじめとする IT 資格試験や、様々な分野の学習に対応できるよう設計しました。
学習進捗管理やランキング機能、リワードシステムを活用しながら、モチベーションを維持しつつ学習を進めることができます。
問題演習の採点結果は記録され、過去の学習履歴を振り返ることが可能です。

## 主な機能
- 問題演習（ランダム出題・難易度自動調整）
- 自動採点・正答率表示
- 学習履歴の記録
- リワード機能（バッジシステム）
  - 問題を解くことで、 **ブロンズ / シルバー / ゴールド** のバッジを獲得
  - 特定のカテゴリでの正解数に応じて各カテゴリのバッジを付与
- ランキング機能
  - 全ユーザーのポイントをランキング機能で可視化
  - バッジを獲得するとランキングページに反映

これにより、単なる問題演習ではなく、ゲーム感覚で楽しく学習を継続できます。
  
## 使用技術

<p align="center">
    <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/HTML.svg" alt="HTML" width="60" height="60"/>
    <img src="https://raw.githubusercontent.com/CSS-Next/logo.css/main/css.svg" alt="CSS" width="60" height="60"/>
    <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/JavaScript.svg" alt="JavaScript" width="60" height="60"/>
    <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Django.svg" alt="Django" width="60" height="60"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" alt="PostgreSQL" width="60" height="60"/>
    <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Docker.svg" alt="Docker" width="60" height="60"/>
    <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/AWS-Dark.svg" alt="AWS" width="60" height="60"/>
    <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Figma-Dark.svg" alt="Figma" width="60" height="60"/>
</p>

## セットアップ方法
1. リポジトリをクローンします。
```sh
git clone git@github.com:hackathon-winter/efFEctive.git
cd efFEctive
```

2. 環境変数の設定
.envファイルを作成し、設定が必要です。

3. Dockerコンテナの起動
以下のコマンドで、アプリケーションをコンテナ化して起動します。
```sh
docker-compose up -d
```

4. データベースのマイグレーション<br>
コンテナ内で、データベースをセットアップします。
```sh
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

5. スーパーユーザーの作成
管理画面にアクセスするためにスーパーユーザーを作成します。
```sh
docker-compose exec web python manage.py createsuperuser
```

6. 開発サーバーの起動
コンテナが正常に起動していることを確認し、<http://localhost>にアクセスしてください。
```sh
docker-compose ps -a
```

6.  Dockerコンテナの停止＆クリーンアップ
```sh
docker-compose down
```

