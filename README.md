# P2P GPS

スマートフォンで取得した現在地を Bluetooth で iPad に送り、iPad の位置として使えるようにするアプリのセットです。位置情報はクラウドを経由せず、端末同士だけでやり取りします。

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
- [用語集](https://github.com/haruki0420/p2pgps/wiki/Glossary)
- [困ったとき](https://github.com/haruki0420/p2pgps/wiki/Troubleshooting)
- [よくある質問](https://github.com/haruki0420/p2pgps/wiki/FAQ)

## ライセンス

- `p2pgps-ios`: AGPL-3.0
- `p2pgps-android` / `p2pgps-protocol`: MIT

詳しくは [License](https://github.com/haruki0420/p2pgps/wiki/License) を参照してください。
