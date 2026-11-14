# Getting Started

## 必要なもの

| 役割 | 端末 | 必要なもの |
| :--- | :--- | :--- |
| 受信（位置を反映される側） | iPad（iPadOS 17.4+） | Developer Mode、[LocalDevVPN](https://apps.apple.com/us/app/localdevvpn/id6755608044)、pairing file、`p2pgps-ios` |
| 送信 | iPhone（iOS 17+） | `p2pgps-ios`（Sender モード） |
| 送信 | Android（8.0+） | `p2pgps-android` の APK |

## 1. iPad（Receiver）を準備する

1. **Developer Mode** を有効化: 設定 → プライバシーとセキュリティ → デベロッパモード → ON → 再起動。
2. **LocalDevVPN** をインストールして接続（VPN アイコンが出ることを確認）。
3. **pairing file** を用意（[StikDebug-Guide / pairing_file.md](https://github.com/StikDebug/StikDebug-Guide/blob/main/pairing_file.md)）。
4. `p2pgps-ios` を SideStore / AltStore でインストール（[ビルド手順](Build-with-xtool) 参照）。
5. アプリで「受信する（iPad）」を選択 → pairing file をインポート → DDI をダウンロード → 接続待ちにする。

## 2. 送信側を準備する

### iPhone

同じ `p2pgps-ios` をインストールし、「送信する（iPhone）」を選択 → 位置情報を「常に許可」→ START。

### Android

`p2pgps-android` の APK をインストール → 位置情報・Bluetooth・通知の権限を許可 → 「送信開始」。

## 3. 接続して反映する

1. iPad の Receiver 画面に `P2PGPS-...` が表示される。
2. タップして接続 → Status を読み、Location を購読。
3. 「位置情報の注入」を ON にする（既定 OFF。ON の間は画面上部にバナーが出ます）。
4. 送信側で START → iPad の地図が送信側の位置に追従し、iPad のシステム位置情報もその座標になります。

## うまくいかないとき

[Troubleshooting](Troubleshooting) を参照してください。
