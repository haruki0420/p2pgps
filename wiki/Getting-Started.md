# Getting Started

## 必要なもの

| 役割 | 端末 | 必要なもの |
| :--- | :--- | :--- |
| 受信（位置を書き換える側） | iPad（iPadOS 17.0 以降） | Developer Mode、LocalDevVPN、pairing file、DDI、`p2pgps-ios` |
| 送信 | iPhone（iOS 17.0 以降） | `p2pgps-ios` |
| 送信 | Android（8.0 以降） | `p2pgps-android` の APK |

## 1. iPad を準備する

初回だけ、Windows / macOS / Linux のパソコンを使います。Mac は不要です。

1. **iloader** で SideStore を入れる（[iloader.app](https://iloader.app)）。iPad を USB でつなぎ、Apple ID でサインインして「Install SideStore (Stable)」を押す。
2. iPad で開発元を信頼する（設定 → 一般 → VPN とデバイス管理）。
3. **Developer Mode** を ON にして再起動する（設定 → プライバシーとセキュリティ → デベロッパモード）。
4. **LocalDevVPN** を入れて接続する。
5. **pairing file** を用意する。iOS 27 では iloader の pairing file でうまくいかないことがある。その場合は [idevice_pair の Windows x86_64 版](https://github.com/jkcoxson/idevice_pair/releases) で作り直す。
6. **p2pgps-ios** の IPA を SideStore で入れる（[Releases](https://github.com/haruki0420/p2pgps-ios/releases)）。
7. アプリで「受信する」を選ぶ → pairing file を読み込む → DDI をダウンロードしてマウントする。

詳しい手順は [Setup iPad](Setup-iPad) を見てください。

## 2. 送信側を準備する

### iPhone

`p2pgps-ios` を入れて「送信する」を選ぶ。位置情報は「常に許可」にする。

### Android

`p2pgps-android` の APK を入れる。位置情報・Bluetooth・通知を許可する。

## 3. つないで位置を反映する

1. 送信側（iPhone / Android）で「送信を開始」を押す。
2. iPad の画面で「スキャン開始」を押す。
3. 送信元の名前（`P2PGPS-...`）を選ぶ。
4. iPad で「位置情報を反映」を ON にする。
5. iPad の地図が送信側の位置に変わり、iPad の位置情報もその場所になる。

## うまくいかないとき

[困ったとき](Troubleshooting) を見てください。
