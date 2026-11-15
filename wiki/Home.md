# P2P GPS Wiki

スマートフォンの現在地を Bluetooth で iPad に送り、iPad の位置として使えるようにするプロジェクトです。位置情報はクラウドを通らず、端末同士だけでやり取りします。

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

## はじめての方

- [Getting Started](Getting-Started) — 最短で動かすまでの手順
- [Setup iPad](Setup-iPad) — iPad の準備（Developer Mode / LocalDevVPN / pairing file / DDI）
- [困ったとき](Troubleshooting)
- [よくある質問](FAQ)

## 詳しく知りたい方

- [用語集](Glossary)
- [全体の仕組み](Architecture)
- [通信仕様](Protocol)
- [ネットワークの仕組み](Networking)
- [デザイン](Design)
- [ビルド（xtool）](Build-with-xtool)
- [ライセンス](License)
- [検証状況](Verification)

## 状態

- 2026-11-15: 通信仕様 v1 を確定。
- Bluetooth での位置の受け渡しと、iPad の位置の書き換えは Android 実機 + iPad で確認済みです。全画面 UI・Dynamic Type・Dark Mode は未確認です。
