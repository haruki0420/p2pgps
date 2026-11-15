# Setup iPad（Receiver）

iPad 側で位置情報をシミュレートするには、StikDebug と同じ前提が必要です。**Mac は不要**ですが、初回セットアップには **Windows / macOS / Linux のコンピュータ + iloader** を使います。

このプロジェクトでは、次の流れを前提とします。

```
iloader で SideStore をインストール
  → iloader で pairing file を注入 / エクスポート
  → SideStore で p2pgps-ios（未署名 IPA）をインストール
  → 本アプリに pairing file をインポート
  → LocalDevVPN 接続 → DDI ダウンロード → 位置注入
```

## 0. 前提

| 項目 | 内容 |
| :--- | :--- |
| 端末 | iPad（iPadOS 17 以降） |
| コンピュータ | Windows / macOS / Linux（初回セットアップのみ。USB 接続） |
| セットアップツール | [iloader](https://iloader.app)（無料・オープンソース。[nab138/iloader](https://github.com/nab138/iloader)） |
| Apple ID | 無料アカウントで可（SideStore の署名に使用） |
| 必須アプリ | [LocalDevVPN](https://apps.apple.com/us/app/localdevvpn/id6755608044)（無料） |
| 必須ファイル | pairing file（`.mobiledevicepairing` / `.mobiledevicepair` / `.plist`） |
| ネットワーク | Wi-Fi（インターネット不要。テザリングでも可） |

## 1. iloader で SideStore をインストール

1. コンピュータに **usbmuxd** を用意します（Windows: iTunes / macOS: 標準搭載 / Linux: パッケージマネージャ）。
2. [iloader.app](https://iloader.app) または [GitHub Releases](https://github.com/nab138/iloader/releases) から iloader をインストールします。
3. iPad を USB ケーブルで接続し、iPad 側で「このコンピュータを信頼」→ パスコードを入力します。
4. iloader を開き、**Apple ID でサインイン**します（大文字・小文字に注意）。
5. デバイスを選択し、**「Install SideStore (Stable)」** を実行します。
6. iPad 側で開発元を信頼します: 設定 > 一般 > **VPN とデバイス管理** > 「デベロッパ App」> Apple ID を選択 > **信頼** > パスコード。
7. **Developer Mode** を ON にします: 設定 > プライバシーとセキュリティ > **デベロッパモード** > ON → 再起動 → ロック解除後に確認。
8. App Store から **LocalDevVPN** をインストールし、開いて **Connect** します。
9. **SideStore** を開き、iloader と同じ Apple ID でサインインします。
10. 「My Apps」で SideStore の **「7 DAYS」** をタップして更新し、セットアップを完了します。

> 無料の Apple ID では、SideStore とインストールしたアプリは **7 日で期限切れ**になります。SideStore の「7 DAYS」をタップして更新するか、iloader から再インストールしてください。

## 2. pairing file を用意する（iloader から注入 / エクスポート）

iloader は SideStore 用の **RPPairing / lockdown pairing file** を自動で配置します。本アプリでも同じ pairing file を使うため、**iloader からエクスポート**して iPad の Files に置きます。

1. iloader でデバイスを選択します。
2. **「Manage Pairing File」** を開き、SideStore（必要なら StikDebug など）の右側の **「Place」** を押して pairing file を配置します（「Pairing file placed successfully!」と表示されれば OK）。
3. エクスポート機能で pairing file をコンピュータに保存します（ファイル名は `pairingFile.mobiledevicepairing` など）。
4. AirDrop / iCloud Drive / Files などで **iPad の Files アプリ**に転送します。

- すでに StikDebug / TLocation を使っている場合は、そのアプリの pairing file をエクスポートして使うこともできます（**必ず同じ iPad の pairing file** を使ってください）。
- **期限切れ・ランダムに無効化された場合**: iloader で「Delete Stored Pairing」→ デバイスで Trust →「Manage Pairing File」→「Place」→ 再度エクスポート → 本アプリで再インポート、の順で復旧します。

> **iloader の対応状況**: iloader v2.4.1 の「ペアリングファイルの管理」には、まだ **P2P GPS が一覧に表示されません**（対応アプリの一覧が固定のため）。**「エクスポート（非推奨）」で pairing file を保存 → AirDrop / Files で iPad に置く → 本アプリでインポート**、の手順を使ってください。本アプリは Documents に置かれた pairing file も自動で読み込みます。

> pairing file は秘密情報です。他人に共有したり、リポジトリにコミットしたりしないでください。本アプリは Application Support 配下に 0600・Data Protection・バックアップ除外で保存します。

## 3. 本アプリ（p2pgps-ios）をインストール

1. [Releases](https://github.com/haruki0420/p2pgps-ios/releases) から未署名 IPA（`p2pgps-ios-<tag>-unsigned.ipa`）をダウンロードします。
2. **SideStore** に IPA を渡してインストールします（SideStore が Apple ID で署名します）。
   - または iloader の「Import any IPA」で直接インストールすることもできます。
3. 初回起動時に「信頼されていない開発元」と表示された場合は、設定 > 一般 > VPN とデバイス管理 で開発元を信頼します。

## 4. 本アプリに pairing file を読み込む

1. P2P GPS を起動し「設定」を開きます。
2. **「pairing file を読み込む」** → Files から手順 2 で保存したファイルを選択します。
3. 「読み込み済み」と表示されれば OK です。トンネルの再試行が自動で走ります。
4. 初回接続時に **「ローカルネットワーク」の許可** を求められます。Remote Pairing サービスを Bonjour（`_remotepairing._tcp`）で検出するために必要なので、**許可**してください。拒否した場合は 設定 > プライバシーとセキュリティ > ローカルネットワーク で P2P GPS を ON にします。

## 5. LocalDevVPN を接続

1. **LocalDevVPN** を開いて **Connect** します（ステータスバーに VPN アイコンが表示されます）。
2. LocalDevVPN は iPad 自身を `10.7.0.1` として公開します。本アプリの Settings の**ターゲット IP が `10.7.0.1`**（既定値）であることを確認してください。
3. **Wi-Fi に接続している必要があります**（RSD / lockdownd は Wi-Fi 関連時のみ開放されます）。
4. Remote Pairing のポートは固定値ではなく、Bonjour で自動検出します（検出できない場合は 49152 にフォールバック）。診断画面の「Remote Pairing ポート」で結果を確認できます。

> LocalDevVPN が使えない場合（他の VPN と競合する、Tailscale を常時使いたい等）は、Tailscale + リフレクターなどの代替手段があります。仕組みと手順は [Networking（LocalDevVPN の仕組みと代替手段）](Networking) を参照してください。

## 6. DDI（Developer Disk Image）

Settings →「DDI をダウンロード」を実行します。アプリが以下を取得します（初回のみ）。

- `DDI/BuildManifest.plist`
- `DDI/Image.dmg`
- `DDI/Image.dmg.trustcache`

取得元: [doronz88/DeveloperDiskImage](https://github.com/doronz88/DeveloperDiskImage) の `PersonalizedImages/Xcode_iOS_DDI_Personalized`。URL は固定コミットに固定し、SHA-256 を検証します。

## 7. 接続確認

1. LocalDevVPN を接続。
2. アプリで「受信する（iPad）」→ ステータスが緑（トンネル接続済み）になることを確認。
3. 送信側（iPhone / Android）を起動し、一覧から選択して接続。
4. 「位置情報の注入」を ON。

## 8. うまくいかないとき

| 症状 | 確認すること |
| :--- | :--- |
| SideStore でアプリが起動しない / 期限切れ | SideStore の「7 DAYS」をタップして更新。改善しなければ iloader から再インストール。 |
| 「信頼されていない開発元」と表示される | 設定 > 一般 > VPN とデバイス管理 で開発元を信頼。 |
| pairing file が無効と言われる | iloader で再配置・再エクスポートしてインポートし直す。期限切れの可能性。 |
| トンネルが繋がらない | 診断画面で pairing file の形式・Wi-Fi・Remote Pairing ポートへの TCP 到達性を確認。LocalDevVPN が接続済みか。Wi-Fi に接続しているか。ターゲット IP が `10.7.0.1` か。Developer Mode が ON か。ローカルネットワークの許可があるか。 |
| 診断でポート検出が Fallback になる | 設定 > プライバシーとセキュリティ > ローカルネットワーク で P2P GPS を ON にして、アプリを再起動。 |
| DDI がマウントできない | DDI を再取得。Developer Mode が ON か。 |

詳しくは [Troubleshooting](Troubleshooting) を参照してください。
