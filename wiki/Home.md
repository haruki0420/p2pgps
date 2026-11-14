# P2P GPS Wiki — Home

iPhone / Android で取得した GPS 位置情報を **Bluetooth Low Energy (BLE)** で iPad に送り、iPad 上で「その場所にいる」ように位置情報を反映するプロジェクトです。

Mac が無くてもビルドできるよう、iOS アプリは [xtool](https://github.com/xtool-org/xtool) を前提にしています。iPad 側の位置固定は [StikDebug](https://github.com/StikDebug/StikDebug) 由来の GPS シミュレーション機能（最小フォーク [TLocation](https://github.com/truongkma/t-location)）を流用しています。

## リポジトリ

| リポジトリ | 役割 | 技術 |
| :--- | :--- | :--- |
| [p2pgps-ios](https://github.com/haruki0420/p2pgps-ios) | iPhone = Sender / iPad = Receiver のユニバーサルアプリ | Swift 6 / SwiftUI / CoreBluetooth / xtool |
| [p2pgps-android](https://github.com/haruki0420/p2pgps-android) | Android Sender | Kotlin / Jetpack Compose / BLE ペリフェラル |
| [p2pgps-protocol](https://github.com/haruki0420/p2pgps-protocol) | BLE プロトコル仕様の正本・Python リファレンス実装・テストベクタ | Python |

## 全体像

```
┌──────────────────────┐   BLE GATT (20 bytes, 1 Hz)   ┌──────────────────────────┐
│ iPhone / Android     │ ────────────────────────────▶ │ iPad                     │
│  位置情報を取得       │  Service: B1E5A000-...        │  BLE セントラル           │
│  BLE ペリフェラル     │  Location / Status / Extended │  MapKit 表示              │
└──────────────────────┘ ◀──────────────────────────── │  StikDebug 由来エンジンで │
                         Control (START/STOP/interval) │  位置をシミュレート        │
                                                       └──────────────────────────┘
```

- 位置情報はクラウドを経由しません。端末間の P2P のみです。
- 位置パケットは 20 bytes 固定（ATT MTU 23 でも分割不要）。

## ページ一覧

- [Getting Started](Getting-Started) — 最短で動かすまでの手順
- [Architecture](Architecture) — システム構成・データフロー
- [Protocol](Protocol) — BLE プロトコル v1 の要約（正本は p2pgps-protocol）
- [Setup iPad](Setup-iPad) — Developer Mode / LocalDevVPN / pairing file / DDI
- [Build with xtool](Build-with-xtool) — Mac なしで iOS アプリをビルドする
- [Troubleshooting](Troubleshooting) — よくあるエラーと対処
- [FAQ](FAQ)
- [Roadmap](Roadmap)
- [License](License)

## ステータス

- 2026-11-15: プロトコル v1 仕様確定、3 リポジトリ実装開始。
- 実機での動作検証は未実施です（開発環境に Mac / iOS 実機 / Android 実機が無いため）。ビルドとユニットテストは GitHub Actions で検証しています。
