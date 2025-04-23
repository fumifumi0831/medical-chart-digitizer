# 紙カルテ電子化・構造化システム

紙カルテ画像（JPEG, PNG）をアップロードし、Google Gemini 2.5 Pro を用いて診療情報（主訴、現病歴など指定項目）を抽出し、構造化されたテキストデータとして表示・CSVダウンロードするWebアプリケーションです。

## システム概要

このシステムは、紙カルテの電子化と構造化を行うためのMVP（Minimum Viable Product）です。

- **フロントエンド**: Next.js (TypeScript) - 画像アップロード、結果表示、CSVダウンロード機能
- **バックエンド**: FastAPI (Python) - 画像処理、AI連携、データベース操作
- **データベース**: PostgreSQL - 構造化データの保存
- **ストレージ**: Google Cloud Storage - 画像ファイルの保存
- **AI処理**: Google Gemini 2.5 Pro API - テキスト情報の抽出と構造化

## リポジトリ構成

```
medical-chart-digitizer/
├── backend/             # FastAPI バックエンドサービス
│   ├── app/             # アプリケーションコード
│   │   ├── core/        # 設定、認証などコア機能
│   │   ├── db/          # データベースモデル、セッション管理
│   │   ├── routers/     # APIエンドポイント
│   │   ├── schemas/     # Pydanticスキーマ
│   │   ├── services/    # ビジネスロジック
│   │   └── tasks/       # 非同期処理タスク
│   ├── tests/           # テストコード
│   ├── Dockerfile       # バックエンド用Dockerファイル
│   └── requirements.txt # Python依存関係
├── frontend/            # Next.js フロントエンドサービス
│   ├── app/             # Next.js App Router
│   │   ├── components/  # Reactコンポーネント
│   │   ├── lib/         # ユーティリティ、APIクライアント
│   │   └── page.tsx     # メインページ
│   ├── Dockerfile       # フロントエンド用Dockerファイル
│   └── package.json     # Node.js依存関係
├── docs/                # ドキュメント類
└── docker-compose.yml   # ローカル開発用Docker構成
```

## 機能概要

- 紙カルテ画像（JPEG/PNG）のアップロード
- 画像からのテキスト情報抽出（主訴、現病歴、既往歴、家族歴、身体所見、検査所見、診断、治療計画）
- 構造化データの表示
- CSVダウンロード

## セットアップ手順

### 前提条件

- [Docker](https://www.docker.com/get-started) および [Docker Compose](https://docs.docker.com/compose/install/)
- [Google Cloud](https://cloud.google.com/) アカウントとプロジェクト
- Gemini API アクセスキー

### 1. リポジトリのクローン

```bash
git clone https://github.com/fumifumi0831/medical-chart-digitizer.git
cd medical-chart-digitizer
```

### 2. 環境変数の設定

バックエンド:
```bash
cd backend
cp .env.example .env
# .envファイルを編集して必要な値を設定
```

フロントエンド:
```bash
cd frontend
cp .env.example .env
# .envファイルを編集して必要な値を設定
```

### 3. Google Cloud の設定

1. Google Cloud プロジェクトを作成
2. Cloud Storage バケットを作成
3. Gemini API の有効化とAPIキーの取得
4. サービスアカウントの作成と認証情報のダウンロード

### 4. Docker Compose によるローカル環境起動

```bash
docker-compose up -d
```

これにより以下のサービスが起動します:
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- PostgreSQL: localhost:5432
- MinIO (ローカル開発用GCSエミュレーション): http://localhost:9001

### 5. 開発時のコマンド

バックエンドの開発:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

フロントエンドの開発:
```bash
cd frontend
npm install
npm run dev
```

## API エンドポイント

- `POST /api/v1/charts` - カルテ画像のアップロードと処理開始
- `GET /api/v1/charts/{chart_id}/status` - 処理ステータスの確認
- `GET /api/v1/charts/{chart_id}` - 抽出結果の取得
- `GET /api/v1/charts/{chart_id}/csv` - 抽出結果のCSVダウンロード

詳細なAPI仕様はバックエンドが起動している状態で `/docs` にアクセスすることでSwagger UIで確認できます。

## 将来的な拡張

- ユーザー認証機能
- 画像領域とテキストのマッピング (ハイライト表示)
- 抽出結果の手動編集機能
- 複数ページのカルテ対応
- OCR品質向上のための前処理
- バッチ処理による複数ファイルの一括処理

## 貢献方法

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

## ライセンス

[MIT License](LICENSE)
