# Setup iPad（Receiver）

iPad 側で位置情報をシミュレートするには、StikDebug と同じ前提が必要です。**Mac は不要**ですが、iPad 上での準備が必要です。

## 1. Developer Mode

設定 → プライバシーとセキュリティ → デベロッパモード → ON → 再起動 → ロック解除後に確認ダイアログで ON。

> Developer Mode は「設定」に最初は表示されません。Xcode か SideStore でアプリをインストールすると表示されます。

## 2. LocalDevVPN

[iTunes/App Store: LocalDevVPN](https://apps.apple.com/us/app/localdevvpn/id6755608044)（無料）をインストールし、VPN を接続します。これにより、iPad 自身を `10.7.0.1` としてループバックでき、自分自身の RSD（port 49152）に接続できます。

- 設定 → VPN で「接続済み」になっていることを確認。
- アプリの Settings でターゲット IP が `10.7.0.1` であることを確認（既定値）。

## 3. pairing file

自分の iPad の pairing record が必要です。取得方法は [StikDebug-Guide / pairing_file.md](https://github.com/StikDebug/StikDebug-Guide/blob/main/pairing_file.md) を参照してください。

- 取得したファイルを Files アプリ等で iPad に置き、`p2pgps-ios` の Settings →「pairing file をインポート」で読み込みます。
- アプリは Documents 配下にコピーして保持します。iCloud には同期しません。

## 4. DDI（Developer Disk Image）

Settings →「DDI をダウンロード」を実行します。アプリが以下を取得します（初回のみ）。

- `DDI/BuildManifest.plist`
- `DDI/Image.dmg`
- `DDI/Image.dmg.trustcache`

取得元: [doronz88/DeveloperDiskImage](https://github.com/doronz88/DeveloperDiskImage) の `PersonalizedImages/Xcode_iOS_DDI_Personalized`。

## 5. 接続確認

1. LocalDevVPN を接続。
2. アプリで「受信する（iPad）」→ ステータスが緑（トンネル接続済み）になることを確認。
3. 送信側（iPhone / Android）を起動し、一覧から選択して接続。
4. 「位置情報の注入」を ON。

## 注意

- Wi-Fi に接続している必要があります（インターネット不要。テザリングでも可）。
- iOS 17.4 以降が必要です。
- 位置シミュレーションは Apple の Developer Disk Image の仕組みを使うため、iOS のアップデートで動かなくなる可能性があります。その場合は TLocation の更新を確認してください。
