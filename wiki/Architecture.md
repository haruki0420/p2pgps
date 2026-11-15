# P2P GPS — アーキテクチャ

## 1. 全体像

3 つのコンポーネントからなる。

1. **Sender（iPhone / Android）**: OS の位置情報 API で現在地を取得し、BLE ペリフェラルとして 20 bytes の位置パケットを notify する。
2. **Receiver（iPad）**: BLE セントラルとして位置パケットを受信し、MapKit で表示しつつ、StikDebug 由来の位置シミュレーションエンジンで iPad 自身の位置を固定する。
3. **Protocol**: 両者を結ぶ GATT プロファイルとバイナリ形式。`p2pgps-protocol` が正本。

```
iPhone/Android ──BLE GATT──▶ iPad ──idevice FFI──▶ iPadOS (location simulation)
```

## 2. iOS アプリ（`p2pgps-ios`）

### 2.1 モジュール構成（SwiftPM）

```
Sources/
├── P2PGPSProtocol/    # 純粋 Swift。UUID・パケット encode/decode・Control/Status
├── P2PGPSCore/        # モデル、設定、ログ、位置フィルタ（移動平均・外れ値除去）
├── P2PGPSBLE/         # CoreBluetooth: ReceiverCentral / SenderPeripheral
├── P2PGPSLocation/    # CoreLocation: Sender 用の位置取得とバックグラウンド維持
├── P2PGPSInjection/   # StikDebug 由来: idevice FFI ラッパ、pairing file、DDI、Tunnel、位置注入
└── P2PGPSApp/         # SwiftUI アプリ本体（@main）、画面、Info.plist
```

- `P2PGPSProtocol` / `P2PGPSCore` は macOS でもビルド可能にし、`swift test` の対象にする。
- `P2PGPSInjection` は iOS 専用（`#if canImport(UIKit)` 等でガード）。

### 2.2 画面

| 画面 | 内容 |
| :--- | :--- |
| ロール選択 / ホーム | 「送信する（iPhone）」「受信する（iPad）」を選択。iPad では受信を既定に |
| Receiver | 接続状態、送信元名、最終受信時刻、MapKit 地図、軌跡、注入 ON/OFF、開始/停止 |
| Sender | 現在地、精度、送信状態、START/STOP、バックグラウンド維持の説明 |
| Settings | pairing file のインポート、DDI のダウンロード/再取得、LocalDevVPN 接続確認、接続先（既定 `10.7.0.1`）、自動接続、ログ |
| Diagnostics | 受信パケットの hex、FFI エラー、注入セッション状態 |

### 2.3 位置の書き換え機能（StikDebug 流用）

[TLocation](https://github.com/truongkma/t-location)（StikDebug の GPS 固定機能だけを残した AGPL-3.0 フォーク）から以下を移植する。

1. **pairing file**: 端末自身の pairing record（`.mobiledevicepairing`）を Files からインポート。`PairingFileStore` で Documents に保存。
2. **LocalDevVPN**: 端末自身を `10.7.0.1` としてループバックさせる VPN。これが無いと自分自身の Remote Pairing サービスに接続できない。
3. **Tunnel**: `tunnel_create_rppairing` で `10.7.0.1:<Bonjour で検出した Remote Pairing ポート>` に RSD ハンドシェイクし、`remote_server_connect_rsd` で `com.apple.dt.simulatelocation` サービスへ接続（検出できない場合は 49152 にフォールバック）。
4. **DDI**: `DeveloperDiskImageService` が GitHub の [doronz88/DeveloperDiskImage](https://github.com/doronz88/DeveloperDiskImage) から `Image.dmg` / `Image.dmg.trustcache` / `BuildManifest.plist` を取得し、`mountPersonalDDI` でマウント。
5. **Location simulation**: `location_simulation_new` → `location_simulation_set(lat, lon)` を 1 秒間隔で呼ぶ。停止時は `location_simulation_clear` → `location_simulation_free`。
6. **フォールバック**: 埋め込みエンジンが使えない場合、TLocation の URL スキーム `tlocation://simulate-location?lat=..&lon=..` / `tlocation://clear-location` へ委譲するモードを設定で選択可能にする。

FFI は `libidevice_ffi.a`（[idevice](https://github.com/jkcoxson/idevice), MIT）を静的リンクする。リポジトリには含めず、`scripts/fetch-vendor.sh` が StikDebug の固定コミット（iOS 26 の Remote Pairing 対応を含む idevice ビルド）から取得して SHA-256 を検証する。

### 2.4 バックグラウンド

- Receiver: `bluetooth-central` + `location` の UIBackgroundModes。BLE 受信と注入ループを維持するため、TLocation と同様に低精度の位置更新で keep-alive する。
- Sender: `bluetooth-peripheral` + `location`。前景サービス相当は iOS では background mode で担保。

## 3. Android アプリ（`p2pgps-android`）

- Kotlin 2.x + Jetpack Compose、minSdk 26 / targetSdk 35–36。
- `LocationManager`（GPS + NETWORK）で位置取得（Google Play Services 非依存）。
- `BluetoothLeAdvertiser` + `BluetoothGattServer` でペリフェラル実装。
- 前景サービス（`connectedDevice` タイプ）で画面 OFF でも送信継続。通知に現在座標と停止ボタン。
- 権限: `ACCESS_FINE_LOCATION`, `BLUETOOTH_ADVERTISE`, `BLUETOOTH_CONNECT`, `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_CONNECTED_DEVICE`, `POST_NOTIFICATIONS`。
- 画面: 送信 ON/OFF、接続中セントラル数、現在地、送信レート、ログ、シミュレート位置（デバッグ用）。
- プロトコル実装は `protocol/` パッケージに分離し、JVM ユニットテストで encode/decode を検証。

## 4. データフロー（Receiver）

1. BLE notify 受信（20 bytes）→ `LocationPacket.decode`。
2. 検証（version / 範囲 / flags）→ 不正なら破棄。
3. `FixFilter`（外れ値除去・精度による重み付け）→ 表示用 `GPSFix`。
4. MapKit 更新（1 Hz、UI は 10 Hz までに間引き）。
5. 注入が ON なら `LocationSimulationEngine.set(lat, lon)` をキュー経由で実行（FFI は直列キューで呼ぶ。TLocation と同じ理由: トンネルの単一占有）。
6. 5 秒ごとに再送（シミュレーションの維持）。切断時は `clear`。

## 5. テスト戦略

| 層 | 方法 |
| :--- | :--- |
| Protocol (Swift) | XCTest。仕様のテストベクタ JSON を共有 |
| Protocol (Kotlin) | JUnit。同じテストベクタ JSON |
| Protocol (Python) | pytest。正本実装として全ベクタを検証 |
| BLE | 実機なしでは検証困難。CoreBluetooth / Android BLE はプロトコル層から分離し、モックで状態遷移をテスト |
| 注入エンジン | 実機必須。CI ではコンパイルのみ。手順書を Wiki に用意 |
| CI | iOS: macOS ランナーで SwiftPM クロスビルド + XcodeGen/Xcode ビルド。Android: Ubuntu + JDK 21 + Gradle。Protocol: Ubuntu/Windows + Python 3.12 |

## 6. 既知の制約

- iPad 側の位置の書き換えは Apple の Developer Disk Image と LocalDevVPN、pairing file を必要とする（StikDebug と同じ前提）。**Mac は不要**だが、iPad で Developer Mode を有効化し、SideStore 等でサイドロードする必要がある。
- iOS 17.0 以降を対象（idevice の RSD トンネル方式）。
- BLE は近距離・1 対 1。同時多接続は v2 以降。
- 実機での動作検証はこの開発環境では実施できない。ビルド・ユニットテスト・仕様整合までを保証し、実機手順を Wiki に記載する。
