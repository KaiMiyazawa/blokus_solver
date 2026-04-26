# Blokus Solver

SMART SCAPE CUP で開発したブロックス・デュオ向けの AI 対戦システムです。チーム Penguin として参加し、準優勝しました。

## 概要

- AI クライアント、ゲームエンジン、対戦ビューアを 1 リポジトリで管理
- 戦略は相手の選択肢を狭める `sticky` 方針
- Python / WebSocket / Electron / React ベース

## 構成

- `client/`: AI クライアント
  - `sticky` コマンドで起動
- `game/`: ブロックス・デュオのゲーム本体
  - `start_blocksduo` コマンドで起動
- `viewer/`: 対戦結果を可視化するデスクトップビューア

## セットアップ

```bash
python3 -m venv ssvenv
source ssvenv/bin/activate
pip install -U ./game
pip install -U ./client
```

## 実行例

```bash
start_blocksduo sticky sticky
```

サンプルプレイヤーでの確認もできます。

```bash
start_blocksduo ss_tarou ss_tarou
```

## 技術スタック

- Python 3.8+
- WebSocket
- NumPy
- Electron
- React
- TypeScript
- Material UI
- Express

## 実績

SMART SCAPE CUP ハッカソン 準優勝

詳細: https://www.dreamnews.jp/press/0000299920/
