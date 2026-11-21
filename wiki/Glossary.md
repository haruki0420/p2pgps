# 用語集（Glossary）

初めて見る用語が出てきたら、このページに戻ってください。カテゴリ別に「意味」と「このプロジェクトでの役割」をまとめています。

- 対象読者: アプリを使う人 / ビルドする人 / コードを読む人
- 表記: 初出は英語、括弧内に日本語の言い換え

---

## 1. プロジェクトの基本

| 用語 | 意味 | このプロジェクトでは |
| :--- | :--- | :--- |
| **P2P** | Peer-to-Peer。サーバーを介さず端末同士が直接通信すること | iPhone / Android と iPad が BLE で直接つながり、位置情報をクラウドに送りません |
| **Sender（送信側）** | 位置情報を送る端末 | iPhone（iOS アプリの Sender モード）または Android アプリ |
| **Receiver（受信側）** | 位置情報を受け取る端末 | iPad（iOS アプリの Receiver モード） |
| **位置の書き換え** | 端末の実際の GPS 位置を、指定した座標に置き換えること | iPad 側で受信した座標を「iPad の現在地」として反映します。既定は OFF で、明示的に ON にしたときだけ行います |
| **GPS fix（フィックス）** | GPS が現在地を測位できた 1 回分の結果 | 緯度・経度・標高・精度・速度・時刻のセット。1 秒ごと（1 Hz）に送ります |
| **1 Hz** | 1 秒に 1 回の頻度 | 既定の位置送信間隔。Control コマンドで 100 ms〜60 s に変更できます |
| **stale（ステイル）** | 古い・鮮度切れ | 受信した位置の時刻が現在から 24 時間以上ずれている状態。破棄はせず、画面に警告だけ出します |
| **accuracy（精度）** | 位置の誤差の目安（メートル） | 小さいほど正確。精度が悪い fix は地図表示や注入の判断材料になります |
| **Null Island** | 緯度 0・経度 0 の地点（大西洋上） | 「測位できていない」ことを表す (0,0) を誤って有効扱いしないための判定基準 |
| **軌跡（trail）** | 受信した位置の履歴 | iPad の地図に線で表示します |

---

## 2. BLE（Bluetooth Low Energy）

| 用語 | 意味 | このプロジェクトでは |
| :--- | :--- | :--- |
| **BLE** | 省電力版の Bluetooth。近距離の機器間通信に使われる | iPhone / Android と iPad の通信方式。Wi-Fi やクラウドは不要です |
| **GATT** | BLE でデータをやり取りするための規格（サービスとキャラクタリスティックの集まり） | 位置情報・制御コマンド・状態を GATT で定義しています |
| **Service（サービス）** | GATT の機能のまとまり | `B1E5A000-…` が P2P GPS のサービス UUID |
| **Characteristic（キャラクタリスティック）** | サービス内の個々のデータ項目 | Location（位置）/ Control（制御）/ Status（状態）/ Extended（拡張）の 4 つ |
| **UUID** | サービスやキャラクタリスティックを識別する 128 bit の ID | `B1E5A000-9C3D-4E7A-8F20-1A2B3C4D5E6F` など |
| **notify（ノーティファイ）** | ペリフェラルからセントラルへ、変化があったときに自動で送る方式 | 位置パケットを 1 Hz で notify します |
| **read / write** | セントラルが値を読む / 書く操作 | Status を read、Control を write します |
| **CCCD** | Client Characteristic Configuration Descriptor。notify の購読設定を保持する | 受信側が「このキャラクタリスティックを購読する」と宣言するために使います |
| **MTU** | 1 回の BLE 通信で送れる最大バイト数 | 既定の ATT MTU 23（ペイロード 20 bytes）でも分割不要なよう、位置パケットを 20 bytes 固定にしています |
| **Central（セントラル）** | BLE 接続を開始する側 | iPad（Receiver） |
| **Peripheral（ペリフェラル）** | アドバタイズして接続を待つ側 | iPhone / Android（Sender） |
| **アドバタイズ** | ペリフェラルが「自分はここにいる」と周囲に知らせること | `P2PGPS-<PLATFORM>-<XXXX>` という名前で発信します |
| **RSSI** | 電波の強さ（受信信号強度） | iPad のステータスレールの「iPad 接続」表示に使います |
| **CoreBluetooth** | iOS の BLE フレームワーク | `CBCentralManager`（受信側）/ `CBPeripheralManager`（送信側） |
| **Location Packet** | 位置情報を格納した 20 bytes のパケット | 緯度・経度・標高・精度・速度・時刻・フラグ |
| **Extended Location** | 補助情報の 8 bytes パケット（任意） | 進行方向・バッテリー・衛星数など |
| **Status** | 送信側の状態を表す 8 bytes のパケット | 送信中 / 停止中 / エラー、送信間隔など |
| **Control** | 受信側から送信側への制御コマンド | START / STOP / SET_INTERVAL / REQUEST_FIX / SET_EXTENDED / RESET |
| **リトルエンディアン** | 複数バイトの数値を下位バイトから並べる方式 | パケット内のすべての数値で採用 |
| **10^7 スケール** | 度 × 10,000,000 の整数表現 | 緯度 35.6812360° → `356812360`。小数を使わず正確に送るため |
| **sequence（シーケンス）** | パケットの通し番号 | 欠落・重複・順序の入れ替わりを検出します |
| **flags** | 状態を表すビット列 | 有効な fix か、標高・速度が有効か、テスト用の位置か、充電中か等 |

---

## 3. iPad 側のセットアップ（DDI・pairing file など）

ここは特に聞き慣れない用語が多いところです。

| 用語 | 意味 | このプロジェクトでは |
| :--- | :--- | :--- |
| **Developer Mode（デベロッパモード）** | iOS / iPadOS の開発者向け機能を有効にする設定 | 設定 → プライバシーとセキュリティ → デベロッパモード。位置シミュレーションに必要 |
| **サイドロード** | App Store を経由せず、IPA を端末にインストールすること | SideStore / AltStore 等を使って `p2pgps-ios` を iPad に入れます |
| **iloader** | SideStore のインストールと pairing file の注入を行うデスクトップツール（Windows / macOS / Linux） | 初回セットアップで使用。Apple ID でサインインし、SideStore の導入と pairing file の配置・エクスポートを行います |
| **SideStore / AltStore** | サイドロード用のアプリ管理ツール | 未署名 IPA にご自身の Apple ID で署名してインストールします。無料 Apple ID では 7 日で期限切れになるため更新が必要です |
| **RPPairing** | RSD 接続に使う pairing file の形式（idevice 系） | iloader は SideStore 用に RPPairing と lockdown の pairing file を配置します |
| **usbmuxd** | USB 経由で iOS デバイスと通信するためのデーモン | iloader がデバイスを認識するために必要（Windows は iTunes、macOS は標準、Linux はパッケージ） |
| **IPA** | iOS アプリのパッケージファイル（Android の APK に相当） | Releases に未署名 IPA を添付しています |
| **pairing file** | Apple デバイスとコンピュータ（または自分自身）をペアリングした記録ファイル | iPad 自身の RSD 接続に必要。アプリにインポートして使います。秘密情報なので扱いに注意 |
| **LocalDevVPN** | 端末自身を `10.7.0.1` としてループバックさせる VPN アプリ（NetworkExtension のパケット反射） | これがないと iPad が自分自身の Remote Pairing サービスに接続できません。仕組みは [Networking](https://github.com/haruki0420/p2pgps/wiki/Networking) を参照 |
| **StosVPN** | LocalDevVPN と同じ方式のオープンソース VPN（SideStore 公式） | LocalDevVPN が使えない環境の代替 |
| **Tailscale** | WireGuard ベースのメッシュ VPN。iOS では Packet Tunnel Provider として動く | 常時接続のまま、tailnet 上のリフレクター経由で自分自身の RSD に到達する使い方ができます（[Networking](https://github.com/haruki0420/p2pgps/wiki/Networking)） |
| **リフレクター（reflector）** | パケットの送信元と宛先を入れ替えて送り返す小さなプログラム | LocalDevVPN / Tailscale / WireGuard 方式の中心となる仕組み |
| **NetworkExtension / Packet Tunnel Provider** | iOS で VPN を実装するためのフレームワーク | LocalDevVPN / StosVPN / Tailscale が使用。entitlement が必要 |
| **RSD（Remote Service Discovery）** | iOS 17 以降のデバイス内部サービスを発見・接続する仕組み | `10.7.0.1` の Remote Pairing サービスに接続し、位置シミュレーションサービスを呼び出します（ポートは Bonjour で自動検出、フォールバック 49152） |
| **Remote Pairing サービス** | RSD への接続を受け付けるデバイス側のサービス。Bonjour（`_remotepairing._tcp`）で広告されます | 固定ポートとは限らないため、アプリが Bonjour で検出します。検出にはローカルネットワークの許可が必要です |
| **DDI（Developer Disk Image）** | Apple が提供する開発用のディスクイメージ | 使える状態にすると、位置の書き換えなどの開発用サービスが使えます。アプリがダウンロードして準備します |
| **trustcache** | 「このバイナリは信頼できる」というリスト | DDI の一部。`Image.dmg.trustcache` としてダウンロードします |
| **BuildManifest** | DDI のビルド情報ファイル | `BuildManifest.plist` としてダウンロードします |
| **マウント** | ディスクイメージを OS に認識させること | DDI を使える状態にしてから位置の書き換えを開始します |
| **`com.apple.dt.simulatelocation`** | Apple の位置シミュレーションサービス名 | 受信した座標をここに設定します |
| **StikDebug** | iOS 向けのオンデバイス・デバッガ / JIT 有効化アプリ | 位置シミュレーションの原実装。本プロジェクトの iPad 側エンジンの由来です |
| **TLocation** | StikDebug から GPS 固定機能だけを残した最小フォーク | 本プロジェクトが移植した実装（AGPL-3.0） |
| **idevice** | Apple デバイスのサービスと通信する Rust ライブラリ | `libidevice_ffi.a` として静的リンク。DDI の準備や位置の書き換えに使用 |
| **FFI** | Foreign Function Interface。他言語の関数を呼ぶ仕組み | Swift から idevice の C 関数を呼びます |
| **RPPairing / `tunnel_create_rppairing`** | pairing file を使って RSD トンネルを張る処理 | 位置シミュレーションの接続確立に使います |
| **UDID** | 端末ごとの一意な ID | pairing file や端末識別に使われます |
| **JIT** | Just-In-Time コンパイル。実行時にコードを生成する仕組み | StikDebug の本来の機能。本プロジェクトでは位置シミュレーションのみ流用 |

> セットアップの詳しい手順は [Setup iPad](Setup-iPad) を参照してください。

---

## 4. iOS アプリの実装

| 用語 | 意味 | このプロジェクトでは |
| :--- | :--- | :--- |
| **Swift** | Apple のプログラミング言語 | iOS アプリの実装言語 |
| **SwiftUI** | Swift の宣言的 UI フレームワーク | 画面の実装 |
| **SwiftPM（Swift Package Manager）** | Swift のパッケージ管理・ビルドシステム | 依存関係とビルドの構成 |
| **xtool** | Mac なしで iOS アプリをビルドするクロスプラットフォームツール | Linux / WSL から `xtool dev build` でビルドするために使用 |
| **XcodeGen** | YAML から Xcode プロジェクトを生成するツール | CI でのリンク検証に使用（`project.yml`） |
| **xcodebuild** | Xcode のコマンドラインビルドツール | CI でアプリのコンパイル・リンクを検証 |
| **Swift 6 / strict concurrency** | Swift の並行性安全チェック | Protocol / Core 層は Swift 6 モード、移植コードは Swift 5 モード |
| **Combine** | Apple のリアクティブプログラミングフレームワーク | 設定変更の反映などに使用 |
| **CoreLocation** | iOS の位置情報フレームワーク | 送信側の位置取得、バックグラウンド維持 |
| **MapKit** | iOS の地図フレームワーク | 受信側の地図表示・軌跡・クロスヘア |
| **Dynamic Type** | 文字サイズをユーザー設定に合わせる仕組み | 座標やラベルが拡大しても崩れないように対応 |
| **Reduce Motion** | 動きを減らすアクセシビリティ設定 | アニメーションを無効化 |
| **HIG（Human Interface Guidelines）** | Apple の UI 設計ガイドライン | ネイティブな作法を守るために参照 |
| **VoiceOver** | iOS のスクリーンリーダー | 座標を「北緯 35.681236」のように読み上げ |
| **Data Protection** | iOS のファイル暗号化・保護クラス | pairing file を保護（`.completeUntilFirstUserAuthentication`） |
| **Application Support / Documents** | アプリのデータ保存先ディレクトリ | pairing file は Application Support 配下に 0600 で保存 |
| **AGPL-3.0** | ネットワーク越しの利用にもソース公開を求めるライセンス | StikDebug / TLocation 由来のため iOS アプリは AGPL-3.0 |

---

## 5. Android アプリの実装

| 用語 | 意味 | このプロジェクトでは |
| :--- | :--- | :--- |
| **Kotlin** | Android の主要プログラミング言語 | Android アプリの実装言語 |
| **Jetpack Compose** | Android の宣言的 UI フレームワーク | 画面の実装 |
| **Material 3** | Google の UI 設計システム | Android 側のデザイン基盤 |
| **Gradle / AGP** | Android のビルドシステム / Android Gradle Plugin | ビルドとテスト |
| **JDK** | Java 開発キット | Gradle の実行に必要（CI は JDK 21） |
| **APK** | Android アプリのパッケージファイル | Releases に添付しています |
| **前景サービス（foreground service）** | 通知を出しながらバックグラウンドで動き続ける仕組み | 画面 OFF 中も位置送信を継続するために使用 |
| **connectedDevice / location タイプ** | Android 14 以降の前景サービスの種類 | BLE 接続維持と位置取得のために宣言 |
| **LocationManager** | Android の位置情報 API | GPS / NETWORK から位置を取得 |
| **BluetoothLeAdvertiser** | BLE のアドバタイズを行う API | ペリフェラルとして自分を発信 |
| **BluetoothGattServer** | BLE の GATT サーバー API | サービス・キャラクタリスティックを提供 |
| **BLUETOOTH_ADVERTISE / CONNECT** | Android 12 以降の BLE 権限 | 実行時許可が必要 |
| **R8 / minify** | コード縮小・難読化ツール | リリースビルドで使用 |
| **debug keystore** | デバッグ署名用の鍵 | デバッグ APK の署名に使用（そのままインストール可能） |
| **minSdk / targetSdk / compileSdk** | 対応する Android バージョンの範囲 | minSdk 26 / targetSdk 35 / compileSdk 36 |
| **TalkBack** | Android のスクリーンリーダー | 座標の読み上げに対応 |

---

## 6. ビルド・配布・開発

| 用語 | 意味 | このプロジェクトでは |
| :--- | :--- | :--- |
| **CI（継続的インテグレーション）** | 変更のたびに自動でビルド・テストすること | GitHub Actions で iOS / Android / Protocol を検証 |
| **GitHub Actions** | GitHub の CI/CD サービス | macOS / Ubuntu / Windows ランナーでテスト・ビルド |
| **workflow_dispatch** | GitHub Actions を手動実行するトリガー | IPA / APK のリリースビルドに使用 |
| **artifact** | CI が生成する成果物 | APK やテスト結果を保存 |
| **Release / タグ / SemVer** | バージョン付きの配布単位 / 目印 / バージョン番号規則 | `v1.0.2` などのタグに IPA / APK を添付 |
| **SHA-256** | データの指紋（ハッシュ） | ダウンロードしたファイルの検証に使用 |
| **未署名 / 署名** | アプリに開発者の証明書を付けるかどうか | iOS の IPA は未署名（SideStore 等で署名）、Android の debug APK はデバッグ署名済み |
| **プロビジョニングプロファイル** | Apple がアプリのインストールを許可する証明書の組 | サイドロード時に必要 |
| **実機検証** | 実際の端末で動作を確認すること | 確認範囲は [Status](Status) を参照 |
| **anti-slop** | AI 生成にありがちな没個性・テンプレ的なデザインを避けること | `DESIGN.md` のチェックリストで管理 |

---

## 7. ライセンス

| 用語 | 意味 | このプロジェクトでは |
| :--- | :--- | :--- |
| **MIT** | ゆるいオープンソースライセンス（著作権表示のみ） | `p2pgps-android` / `p2pgps-protocol` は MIT |
| **AGPL-3.0** | 強いコピーレフト。ネットワーク越しの利用にもソース公開を求める | `p2pgps-ios` は StikDebug / TLocation 派生のため AGPL-3.0 |
| **派生著作物** | 既存の作品を元にした作品 | iOS の位置の書き換え機能は TLocation の派生 |
| **NOTICE** | 上流の著作権・ライセンス表示をまとめたファイル | `p2pgps-ios/NOTICE` に StikDebug / TLocation / idevice / libplist の帰属を記載 |
| **SPDX** | ライセンスを短い識別子で表す規格 | ソース先頭の `SPDX-License-Identifier: AGPL-3.0-or-later` など |

---

## 関連ページ（Wiki）

- [Getting Started](https://github.com/haruki0420/p2pgps/wiki/Getting-Started) — 最短で動かす
- [Setup iPad](https://github.com/haruki0420/p2pgps/wiki/Setup-iPad) — DDI / pairing file / LocalDevVPN の手順
- [Protocol](https://github.com/haruki0420/p2pgps/wiki/Protocol) — BLE プロトコルの詳細
- [Troubleshooting](https://github.com/haruki0420/p2pgps/wiki/Troubleshooting) — うまくいかないとき
- [FAQ](https://github.com/haruki0420/p2pgps/wiki/FAQ) — よくある質問
