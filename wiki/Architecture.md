# Architecture

## コンポーネント

1. **Sender（iPhone / Android）**: OS の位置情報 API で現在地を取得し、BLE ペリフェラルとして 20 bytes の位置パケットを notify する。
2. **Receiver（iPad）**: BLE セントラルとして位置パケットを受信し、MapKit で表示しつつ、StikDebug 由来の位置シミュレーションエンジンで iPad 自身の位置を固定する。
3. **Protocol**: 両者を結ぶ GATT プロファイルとバイナリ形式（[p2pgps-protocol](https://github.com/haruki0420/p2pgps-protocol) が正本）。

```
iPhone/Android ──BLE GATT──▶ iPad ──idevice FFI──▶ iPadOS (location simulation)
```

## iOS アプリのモジュール

| モジュール | 役割 |
| :--- | :--- |
| `P2PGPSProtocol` | UUID・LocationPacket(20B)・Extended(8B)・Control・Status の encode/decode。純粋 Swift |
| `P2PGPSCore` | GPSFix モデル・設定・ログ・FixFilter（外れ値除去） |
| `P2PGPSBLE` | CoreBluetooth: ReceiverCentral（CBCentralManager）/ SenderPeripheral（CBPeripheralManager） |
| `P2PGPSLocation` | CoreLocation: Sender の位置取得とバックグラウンド維持 |
| `P2PGPSInjection` | StikDebug 由来: idevice FFI・pairing file・DDI・Tunnel・LocationSimulationEngine・URL スキームフォールバック |
| `P2PGPSApp` | SwiftUI アプリ本体（@main）・画面・Info.plist |

## 位置注入の流れ（iPad）

1. BLE notify 受信 → `LocationPacket.decode` → 検証。
2. `FixFilter` で外れ値を除去 → MapKit に反映。
3. 注入 ON なら `LocationSimulationEngine.set(lat, lon)` を直列キューで実行。
4. エンジン内部:
   - pairing file を読み込み
   - `tunnel_create_rppairing` で `10.7.0.1:<Bonjour で検出した Remote Pairing ポート>` に接続（LocalDevVPN 経由。検出できない場合は 49152）
   - `remote_server_connect_rsd` で `com.apple.dt.simulatelocation` に接続
   - DDI が未マウントなら `mountPersonalDDI`
   - `location_simulation_new` → `location_simulation_set(lat, lon)`
5. 停止時は `location_simulation_clear` → `location_simulation_free`。切断時もクリア。

## Android アプリ

- `protocol/`（純 Kotlin codec）、`ble/`（BluetoothLeAdvertiser + BluetoothGattServer）、`location/`（LocationManager）、`service/`（前景サービス）、`ui/`（Compose）。

## テスト戦略

| 層 | 方法 |
| :--- | :--- |
| Protocol | 3 実装（Swift / Kotlin / Python）が同じテストベクタ JSON を検証 |
| BLE | 実機なしでは検証困難。プロトコル層と分離し、状態遷移をユニットテスト |
| 注入エンジン | 実機必須。CI ではコンパイルのみ |
| CI | iOS: macOS + SwiftPM クロスビルド + XcodeGen/Xcode。Android: Ubuntu + Gradle。Protocol: Ubuntu/Windows + pytest |
