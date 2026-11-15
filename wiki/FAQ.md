# FAQ

## Q. Mac が無くても使えますか？

A. はい。iOS アプリのビルドは xtool で Linux / WSL から行えます。ただし iPad 側の初回セットアップには **Windows / macOS / Linux のコンピュータ + [iloader](https://iloader.app)** が必要です（SideStore のインストールと pairing file の注入）。位置シミュレーションには Developer Mode・LocalDevVPN・pairing file・DDI も必要です（StikDebug と同じ前提）。

## Q. pairing file はどうやって用意しますか？

A. **iloader** を使うのが簡単です。iloader で SideStore をインストールすると pairing file が自動で配置されるので、「Manage Pairing File」で SideStore に **Place** し、**エクスポート**したファイルを iPad の Files に置いて本アプリでインポートします。期限切れ時は iloader で「Delete Stored Pairing」→ Trust →「Manage Pairing File」→ Place → 再エクスポート、で復旧できます。

> **P2P GPS は iloader v2.4.1 の対応アプリ一覧にまだ入っていません**（一覧が固定のため）。**「エクスポート（非推奨）」→ Files → 本アプリでインポート**を使ってください。本アプリは Documents に置かれた pairing file も自動で読み込みます。詳細は [Setup iPad](Setup-iPad) を参照してください。

## Q. iPad の位置情報を「本物の GPS」に戻すには？

A. Receiver 画面で「位置情報の注入」を OFF にするか、送信側で STOP。アプリは `location_simulation_clear` を呼び、iPad の位置は実 GPS に戻ります。

## Q. 位置情報はどこかに送られますか？

A. 送られません。iPhone/Android と iPad の間の BLE のみです。クラウド・サーバーは使いません。

## Q. 複数の iPad に同時に送れますか？

A. v1 では 1 対 1 です。Android は複数セントラルからの接続自体は受けられますが、アプリの UI は 1 台を想定しています。v2 でマルチ接続を検討しています。

## Q. 送信側は iPhone と Android のどちらでもよい？

A. どちらでも構いません。プロトコルは共通です。iPad 側の Receiver は同じ `p2pgps-ios` です。

## Q. 位置の更新間隔は変えられますか？

A. Receiver の Settings、または Control の `SET_INTERVAL` で 100 ms〜60 s に変更できます（既定 1 s）。

## Q. 送信側のバッテリー消費は？

A. BLE ペリフェラル + 位置情報取得のため、連続使用で 1 時間あたり数 %〜10 % 程度を想定しています（実測未実施）。間隔を 5 s にすると節約できます。

## Q. StikDebug / TLocation との関係は？

A. `p2pgps-ios` の位置注入エンジンは TLocation（StikDebug の GPS 固定機能の最小フォーク）から移植しています。AGPL-3.0 を継承しています。TLocation がインストールされている場合、URL スキーム `tlocation://simulate-location?lat=..&lon=..` に委譲するフォールバックモードも選べます。

## Q. LocalDevVPN 以外の方法はありますか？

A. あります。**Tailscale + リフレクター**（tailnet 上の Linux ノードでパケットを反射）、**StosVPN**、**WireGuard + 反射サーバー**、**Surge / Clash の reflect** などです。仕組み・比較・手順は [Networking（LocalDevVPN の仕組みと代替手段）](Networking) を参照してください。本アプリは Settings の「ターゲット IP」を変更するだけで、これらの方式にも対応できます。

## Q. なぜ 20 bytes 固定なのですか？

A. BLE 4.0 の既定 ATT MTU 23（ペイロード 20 bytes）でもフラグメンテーション不要にするためです。緯度経度は 10^-7 度（約 1 cm）精度で int32 に収まります。

## Q. ライセンスは？

A. `p2pgps-ios` は AGPL-3.0（StikDebug/TLocation の派生のため）、`p2pgps-android` と `p2pgps-protocol` は MIT です。詳細は [License](License)。
