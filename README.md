# P2P GPS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

iPhone / Android で取得した GPS 位置情報を **Bluetooth Low Energy (BLE)** で iPad に送り、iPad 上で「その場所にいる」ように位置情報を反映するアプリケーション群です。

Mac を持っていなくてもビルドできるよう、iOS アプリは [xtool](https://github.com/xtool-org/xtool)（SwiftPM ベースの Xcode 代替）を前提としています。iPad 側の位置固定は [StikDebug](https://github.com/StikDebug/StikDebug) 由来の GPS シミュレーション機能（最小フォーク [TLocation](https://github.com/truongkma/t-location)）を流用しています。

## リポジトリ

| リポジトリ | 役割 | 技術 | ライセンス |
| :--- | :--- | :--- | :--- |
| [`p2pgps-ios`](https://github.com/haruki0420/p2pgps-ios) | iPhone = Sender / iPad = Receiver のユニバーサルアプリ | Swift 6 / SwiftUI / CoreBluetooth / xtool | AGPL-3.0 |
| [`p2pgps-android`](https://github.com/haruki0420/p2pgps-android) | Android Sender | Kotlin / Jetpack Compose / BLE ペリフェラル | MIT |
| [`p2pgps-protocol`](https://github.com/haruki0420/p2pgps-protocol) | BLE プロトコル仕様の正本・Python リファレンス実装・テストベクタ | Python | MIT |

## 仕組み

```
┌──────────────────────┐    BLE GATT (20 bytes, 1 Hz)    ┌──────────────────────────┐
│ iPhone / Android     │ ──────────────────────────────▶ │ iPad                     │
│  位置情報を取得       │   Service: B1E5A000-...         │  BLE セントラル           │
│  BLE ペリフェラル     │   Location / Status / Extended  │  MapKit 表示              │
└──────────────────────┘ ◀────────────────────────────── │  StikDebug 由来エンジンで │
                          Control (START/STOP/interval)  │  位置をシミュレート        │
                                                         └──────────────────────────┘
```

- 位置パケットは **20 bytes 固定**（ATT MTU 23 でも分割不要）。詳細は [`docs/protocol-spec.md`](docs/protocol-spec.md)。
- iPad 側は pairing file + LocalDevVPN + Developer Disk Image を使って `com.apple.dt.simulatelocation` に接続し、受信した座標を設定します（StikDebug と同じ方式）。
- 位置情報はクラウドを経由しません。端末間の P2P のみです。

## クイックスタート

### 1. iPad（Receiver）

1. コンピュータ（Windows / macOS / Linux）で **[iloader](https://iloader.app)** を使い、iPad に **SideStore** をインストール（iPad を USB 接続 → Apple ID でサインイン →「Install SideStore (Stable)」）。
2. iPad で開発元を信頼（設定 → 一般 → VPN とデバイス管理）→ **Developer Mode** を有効化 → 再起動。
3. [LocalDevVPN](https://apps.apple.com/us/app/localdevvpn/id6755608044)（無料）をインストールして接続。
4. **iloader で pairing file を注入**（Manage Pairing File → Place）し、**エクスポート**して iPad の Files に置く。
5. `p2pgps-ios` の未署名 IPA を SideStore でインストールし、アプリで pairing file をインポート。
6. アプリで「受信する（iPad）」を選び、DDI をダウンロード → 送信側を選択 → 注入 ON。

詳しくは [Setup iPad](https://github.com/haruki0420/p2pgps/wiki/Setup-iPad) を参照してください。

### 2. iPhone（Sender）

同じ `p2pgps-ios` をインストールし、「送信する（iPhone）」を選んで START。位置情報の許可は「常に許可」を推奨。

### 3. Android（Sender）

`p2pgps-android` の APK をインストールし、位置情報・Bluetooth の権限を許可して「送信開始」。

### ビルド（Mac なし）

```bash
# iOS (xtool / Linux or WSL)
cd p2pgps-ios
xtool dev build        # ビルド
xtool dev run          # 接続中の実機へインストール

# Android
cd p2pgps-android
./gradlew :app:assembleDebug

# Protocol (Python)
cd p2pgps-protocol
python -m pytest
```

## ドキュメント

- [プロトコル仕様 v1](docs/protocol-spec.md)
- [アーキテクチャ](docs/architecture.md)
- [用語集（Glossary）](docs/glossary.md) — DDI・pairing file・BLE などの用語解説
- [ネットワーク構成（LocalDevVPN の仕組みと代替手段）](docs/networking.md) — Tailscale / WireGuard / Surge での実装
- [カーナビ用途での適性](docs/car-navigation.md) — 遅延・精度・推奨設定
- [プロジェクト計画 / 進行状況](docs/plan.md)
- [レビューと修正の記録](docs/review-summary.md)
- [検証とリリース](docs/verification.md)
- [ライセンスと帰属](docs/licensing.md)
- 各リポジトリの Wiki（Getting Started / Protocol / Architecture / Troubleshooting / FAQ）

## Wiki

このリポジトリの `wiki/` はプロジェクト全体の Wiki（Getting Started / Glossary / Architecture / Protocol / Design / Setup iPad / Build with xtool / Troubleshooting / FAQ / Roadmap / License）です。GitHub の仕様で Wiki の初回ページだけは手動作成が必要です。

1. https://github.com/haruki0420/p2pgps/wiki を開き「Create the first page」→ そのまま Save。
2. `./scripts/publish-wiki.sh` を実行すると `wiki/*.md` が Wiki に同期されます。

各サブリポジトリ（`p2pgps-ios` / `p2pgps-android` / `p2pgps-protocol`）にも Wiki 用 Markdown と同期スクリプトがあります。

## 既知の制約

- iPad 側の位置注入には Developer Mode・LocalDevVPN・pairing file・DDI が必要です（StikDebug と同じ前提）。
- iOS 17.4 以降が対象です。
- 実機での動作検証は開発環境の制約により未実施です。ビルド・ユニットテスト・仕様整合までを CI で保証しています。手順は Wiki を参照してください。

## ライセンス

- `p2pgps-ios`: **AGPL-3.0**（StikDebug / TLocation の派生のため）
- `p2pgps-android` / `p2pgps-protocol`: **MIT**

詳細と帰属表示は [docs/licensing.md](docs/licensing.md) を参照してください。
