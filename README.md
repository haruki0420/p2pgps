# P2P GPS

スマートフォンで取得した現在地を Bluetooth で iPad に送り、iPad の位置として使えるようにするアプリのセットです。位置情報はクラウドを経由せず、端末同士だけでやり取りします。

## 3分でわかる

- **何**: iPhone / Android の GPS を BLE で iPad に送り、iPad の位置として使うアプリ。
- **誰向け**: Mac を持たず iPad の位置を合わせたい技術志向の人。位置依存アプリの QA・デモ担当。
- **最短**: iPad に受信アプリ → スマホに送信アプリ → 送信開始 → iPad で「位置情報を反映」を ON。
- **制約**: iPadOS / iOS 17+、Android 8+。初回だけ PC が必要で、Developer Mode / LocalDevVPN / pairing file / DDI を用意する。1 対 1 接続、認証なし。位置変更は Apple の非公開 API に依存する。
- **状態**: 検証状況は [Status](https://github.com/haruki0420/p2pgps/wiki/Status) を参照。Android リポジトリは 2026-11-21 に public 化済み。

[Status](https://github.com/haruki0420/p2pgps/wiki/Status) · [Compatibility](https://github.com/haruki0420/p2pgps/wiki/Compatibility) · [Getting Started](https://github.com/haruki0420/p2pgps/wiki/Getting-Started) · [Setup iPad](https://github.com/haruki0420/p2pgps/wiki/Setup-iPad)

## アプリ

| リポジトリ | 役割 |
| :--- | :--- |
| [p2pgps](https://github.com/haruki0420/p2pgps) | 全体の説明・セットアップ手順（このリポジトリ） |
| [p2pgps-ios](https://github.com/haruki0420/p2pgps-ios) | iPhone 用の送信アプリ / iPad 用の受信アプリ |
| [p2pgps-android](https://github.com/haruki0420/p2pgps-android) | Android 用の送信アプリ |
| [p2pgps-protocol](https://github.com/haruki0420/p2pgps-protocol) | 通信仕様とテスト用の実装 |

## 使い方

1. iPad に受信アプリを入れて、位置を書き換える準備をする
2. iPhone または Android に送信アプリを入れる
3. 送信アプリで「送信を開始」、iPad 側で送信元を選んで「位置情報を反映」を ON にする

詳しい手順は [Wiki の Getting Started](https://github.com/haruki0420/p2pgps/wiki/Getting-Started) と [Setup iPad](https://github.com/haruki0420/p2pgps/wiki/Setup-iPad) を見てください。

## ビルド

- iOS: [Build](https://github.com/haruki0420/p2pgps-ios/wiki/Build)
- Android: [Getting Started](https://github.com/haruki0420/p2pgps-android/wiki/Getting-Started)
- 通信仕様: [p2pgps-protocol](https://github.com/haruki0420/p2pgps-protocol)

## ドキュメント

- [Wiki の Home](https://github.com/haruki0420/p2pgps/wiki)
- [Status](https://github.com/haruki0420/p2pgps/wiki/Status) — 検証状況の正本
- [Compatibility](https://github.com/haruki0420/p2pgps/wiki/Compatibility) — 対応 OS・送信間隔
- [Security & Privacy](https://github.com/haruki0420/p2pgps/wiki/Security-and-Privacy)
- [用語集](https://github.com/haruki0420/p2pgps/wiki/Glossary)
- [困ったとき](https://github.com/haruki0420/p2pgps/wiki/Troubleshooting)
- [よくある質問](https://github.com/haruki0420/p2pgps/wiki/FAQ)

## ライセンス

- `p2pgps`: MIT
- `p2pgps-ios`: AGPL-3.0
- `p2pgps-android` / `p2pgps-protocol`: MIT

詳しくは [License](https://github.com/haruki0420/p2pgps/wiki/License) を参照してください。
