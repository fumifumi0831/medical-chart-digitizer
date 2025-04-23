# 紙カルテ電子化・構造化システム

紙カルテ画像（JPEG, PNG）をアップロードし、Google Gemini 2.5 Pro を用いて診療情報（主訴、現病歴など指定項目）を抽出し、構造化されたテキストデータとして表示・CSVダウンロードするWebアプリケーションです。

## システム構成

- **Frontend**: Next.js (TypeScript)
- **Backend API**: FastAPI (Python)
- **データベース**: PostgreSQL
- **ストレージ**: Google Cloud Storage
- **AI処理**: Google Gemini 2.5 Pro API

## 機能概要

- 紙カルテ画像（JPEG/PNG）のアップロード
- 画像からのテキスト情報抽出（Gemini APIによる）
- 構造化データの表示
- CSVダウンロード

## リポジトリ構成

このリポジトリは以下のディレクトリ構造で構成されています：

```
medical-chart-digitizer/
├── backend/             # FastAPI バックエンドサービス
├── frontend/            # Next.js フロントエンドサービス
├── docs/                # ドキュメント類
└── docker-compose.yml   # ローカル開発用Docker構成
```

## 開発環境構築

### 前提条件

- Docker および Docker Compose
- Google Cloud アカウントとプロジェクト
- Gemini API アクセスキー

### 環境構築手順

1. リポジトリをクローン
2. 必要な環境変数を設定
3. Docker Compose によるローカル環境起動

詳細は各ディレクトリの README を参照してください。

## ライセンス

[MIT License](LICENSE)
