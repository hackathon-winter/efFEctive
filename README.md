<pre>
efFEctive/
.
├── authentication/              # 認証関連アプリ
│   ├── migrations/              # マイグレーションファイル
│   ├── templates/               # HTMLテンプレート
│   ├── static/                  # CSS, JS, 画像ファイル
│   ├── admin.py                 # 管理画面設定
│   ├── apps.py                  # アプリケーション設定
│   ├── models.py                # データベースモデル
│   ├── tests.py                 # テスト
│   ├── urls.py                  # URL定義
│   └── views.py                 # ビュー（ロジック）
├── questions/                   # 問題管理アプリ
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── progress/                    # 学習進捗管理アプリ
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/                   # 共通HTMLテンプレート
│   └── base.html
├── static/                      # 静的ファイル
│   ├── css/
│   ├── js/
│   └── images/
├── config/                      # プロジェクト設定ディレクトリ
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py              # プロジェクト設定
│   ├── urls.py                  # プロジェクト全体のURL定義
│   └── wsgi.py
├── manage.py                    # Django管理コマンド
├── requirements.txt             # 依存パッケージ
├── Dockerfile                   # Docker設定
├── docker-compose.yml           # Docker Compose設定
├── .env                         # 環境変数
└── README.md                    # プロジェクト説明

</pre>
