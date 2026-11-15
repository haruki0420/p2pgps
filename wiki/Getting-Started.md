# Getting Started

## 必要なもの

| 役割 | 端末 | 必要なもの |
| :--- | :--- | :--- |
| 受信（位置を反映される側） | iPad（iPadOS 17.4+） | Developer Mode、[LocalDevVPN](https://apps.apple.com/us/app/localdevvpn/id6755608044)、pairing file、`p2pgps-ios` |
| 送信 | iPhone（iOS 17+） | `p2pgps-ios`（Sender モード） |
| 送信 | Android（8.0+） | `p2pgps-android` の APK |

## 1. iPad（Receiver）を準備する

初回セットアップには **Windows / macOS / Linux のコンピュータ + iloader** を使います（Mac は不要）。

1. **iloader** で SideStore をインストール（[iloader.app](https://iloader.app)）。iPad を USB 接続し、Apple ID でサインイン →「Install SideStore (Stable)」。
2. iPad で開発元を信頼（設定 → 一般 → VPN とデバイス管理）→ **Developer Mode** を ON → 再起動。
3. **LocalDevVPN** をインストールして接続（VPN アイコンが出ることを確認）。
4. SideStore を開いてサインイン →「7 DAYS」をタップして更新。
5. **iloader で pairing file を注入**（Manage Pairing File → Place）し、**エクスポート**して iPad の Files に置く。
6. `p2pgps-ios` の未署名 IPA を SideStore でインストール（[ビルド手順](Build-with-xtool) または [Releases](https://github.com/haruki0420/p2pgps-ios/releases)）。
   - SideStore の Sources に `https://raw.githubusercontent.com/haruki0420/p2pgps-ios/main/source/apps.json` を追加すると、以降は更新が自動で一覧に表示されます。
7. アプリで「受信する（iPad）」を選択 → pairing file をインポート → DDI をダウンロード → 接続待ちにする。

詳しい手順は [Setup iPad](Setup-iPad) を参照してください。

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
