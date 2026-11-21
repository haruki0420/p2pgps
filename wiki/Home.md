# P2P GPS Wiki

スマートフォンの現在地を Bluetooth で iPad に送り、iPad の位置として使えるようにするプロジェクトです。位置情報はクラウドを通らず、端末同士だけでやり取りします。

## 読者別の導線

### 1. はじめて使う

- [Getting Started](Getting-Started) — 最短で動かすまでの手順
- [Setup iPad](Setup-iPad) — iPad の準備（Developer Mode / LocalDevVPN / pairing file / DDI）
- [FAQ](FAQ)
- [Troubleshooting](Troubleshooting)

### 2. 開発する

- [Architecture](Architecture) — 全体の仕組み
- [Build with xtool](Build-with-xtool) — Mac なしの iOS ビルド
- [Product](Product) — 対象ユーザーとスコープ
- [Design](Design) — 視覚世界とトークン
- [Networking](Networking) — RSD / VPN / リフレクター
- [License](License)
- 各リポジトリ: [iOS](https://github.com/haruki0420/p2pgps-ios/wiki) / [Android](https://github.com/haruki0420/p2pgps-android/wiki) / [Protocol](https://github.com/haruki0420/p2pgps-protocol/wiki)

### 3. 仕様・QA

- [Protocol](Protocol) — BLE プロトコルの要点
- [Compatibility](Compatibility) — 対応 OS・送信間隔・配布形式
- [Verification](Verification) — CI とリリース
- [Status](Status) — 検証状況の正本
- [Glossary](Glossary) — 用語集

### 4. 困ったとき・状態

- [Status](Status) — 何が確認済みで、何が未確認か
- [Troubleshooting](Troubleshooting)
- [Security & Privacy](Security-and-Privacy) — 認証なし・クラウドなしの前提と注意

## アプリ

| リポジトリ | 役割 |
| :--- | :--- |
| [p2pgps](https://github.com/haruki0420/p2pgps) | 全体の説明・セットアップ手順（この Wiki） |
| [p2pgps-ios](https://github.com/haruki0420/p2pgps-ios) | iPhone 用の送信アプリ / iPad 用の受信アプリ |
| [p2pgps-android](https://github.com/haruki0420/p2pgps-android) | Android 用の送信アプリ |
| [p2pgps-protocol](https://github.com/haruki0420/p2pgps-protocol) | 通信仕様とテスト用の実装 |

## 使い方の流れ

1. iPad に受信アプリを入れて、位置を書き換える準備をする
2. iPhone または Android に送信アプリを入れる
3. 送信アプリで「送信を開始」、iPad 側で送信元を選んで「位置情報を反映」を ON にする

## 状態

検証状況・既知の制約・リポジトリの公開範囲は [Status](Status) に集約しています。

- 2026-11-15: 通信仕様 v1.0.1 を確定。
