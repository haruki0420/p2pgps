# iPad の準備

iPad に受信アプリを入れて、位置を書き換えられるようにするまでの手順です。

## 1. 必要なもの

- iPad（iPadOS 17 以降）
- Windows / macOS / Linux のパソコン（初回の準備だけ）
- USB ケーブル
- 無料の **LocalDevVPN**（iPad に入れます）
- **pairing file**（iPad とパソコンを結び付けるファイル）
- **DDI**（Apple の開発用イメージ。アプリが自動で取得します）

## 2. SideStore を入れる

1. パソコンで [iloader](https://iloader.app) を開きます。
2. iPad を USB でつなぎ、SideStore をインストールします。
3. iPad の 設定 > 一般 > VPN とデバイス管理 で開発元を信頼します。
4. iPad の 設定 > プライバシーとセキュリティ > デベロッパモード を ON にします。

## 3. 受信アプリを入れる

1. iPad の SideStore に [P2P GPS のソース](https://raw.githubusercontent.com/haruki0420/p2pgps-ios/main/source/apps.json) を追加します。
2. P2P GPS をインストールします。

## 4. pairing file を入れる

1. パソコンの iloader で「Manage Pairing File」→「Place」を押します。
2. 「エクスポート」で pairing file を保存します。
3. iPad の Files に移し、P2P GPS の設定画面で読み込みます。

> iOS 27 でうまくいかない場合は、[idevice_pair](https://github.com/jkcoxson/idevice_pair/releases) の Windows x86_64 版で pairing file を作り直してください。

## 5. LocalDevVPN を入れる

1. iPad に LocalDevVPN をインストールします。
2. LocalDevVPN を開いて「Connect」を押します。
3. Wi-Fi に接続したままにします。

## 6. DDI を準備する

1. P2P GPS の設定画面で「DDI をダウンロード」を押します。
2. ダウンロードが終わったら「DDI を使える状態にする」を押します。

## 7. つなぐ

1. 送信側（iPhone / Android）で「送信を開始」を押します。
2. iPad で「受信する」→「スキャン開始」→ 送信元を選びます。
3. 送信元と接続済み（緑）になったら、「位置情報を反映」を ON にします。

## 8. うまくいかないとき

| 症状 | 確認すること |
| :--- | :--- |
| SideStore でアプリが起動しない | SideStore の「7 DAYS」を押して更新する |
| 「信頼されていない開発元」と出る | 設定 > 一般 > VPN とデバイス管理 で開発元を信頼する |
| pairing file が通らない | pairing file を作り直して、もう一度読み込む |
| iPad 内部への接続ができない | LocalDevVPN が接続済みか、Wi-Fi につながっているか確認する |
| 位置が変わらない | 「位置情報を反映」が ON か、DDI が準備済みか確認する |

## 9. 別の VPN を使いたい場合

LocalDevVPN の代わりに Tailscale などを使う方法は [Networking](Networking) を見てください。
