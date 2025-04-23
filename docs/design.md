# 詳細設計書: 紙カルテ電子化・構造化システム

## 1. システム概要

本システムは、紙カルテ画像（JPEG, PNG）をアップロードし、Google Gemini 2.5 Pro を用いて診療情報（主訴、現病歴など指定項目）を抽出し、構造化されたテキストデータとして表示・CSVダウンロードするWebアプリケーションです。

詳細な設計ドキュメントは元の詳細設計書を参照してください。

## 主要コンポーネント

### Frontend (Next.js)

- ImageUploader
- ResultDisplay
- StatusBar
- CsvDownloader

### Backend API (FastAPI)

- `/charts` (POST) - 画像アップロード処理
- `/charts/{chart_id}/status` (GET) - 処理ステータス取得
- `/charts/{chart_id}` (GET) - 抽出結果取得
- `/charts/{chart_id}/csv` (GET) - CSV形式でのダウンロード

### データモデル

- charts テーブル - カルテメタデータ
- extracted_data テーブル - 抽出テキストデータ

## アーキテクチャ

Next.js + FastAPI + PostgreSQL + Google Cloud Storage + Google Gemini API