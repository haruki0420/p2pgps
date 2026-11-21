# 対応環境とバージョン（Compatibility）

最終更新: 2026-11-21

検証状況の正本は [Status](Status) です。このページは対応バージョンと設定範囲だけをまとめます。

## 対応バージョン

| 領域 | 対応 | 根拠 |
| :--- | :--- | :--- |
| iOS / iPadOS | 17.0 以降 | `p2pgps-ios` の README / `Package.swift` |
| Android | 8.0 以降（minSdk 26 / target 35 / compile 36） | `p2pgps-android/app/build.gradle.kts` |
| プロトコル | v1.0.1 | [`spec/protocol-v1.md`](https://github.com/haruki0420/p2pgps-protocol/blob/main/spec/protocol-v1.md) |
| BLE | 1 対 1・近距離 | 仕様 §1 / §8 |

## 送信間隔

| 設定場所 | 選択肢 |
| :--- | :--- |
| プロトコル | 100〜60000 ms。0 は 1000、1〜99 は 100、60001〜65535 は 60000 に正規化（仕様 §5.1） |
| iOS の UI | 100 / 500 / 1000 / 2000 / 5000 ms（既定 1000 ms） |
| Android の UI | 200 / 500 / 1000 / 2000 / 5000 ms（既定 1000 ms） |

- Android は位置取得も設定した間隔に合わせて要求します（電池消費は増えます）。
- iOS の CoreLocation は更新頻度を保証しないため、設定より遅くなることがあります。
- 詳細は [Networking](Networking) の「高頻度更新」を参照。

## 配布

| アプリ | 配布形式 |
| :--- | :--- |
| iOS / iPadOS | Releases の未署名 IPA。SideStore / AltStore で署名してインストール |
| Android | Releases のデバッグ署名済み APK / リリース署名済み APK |
| Protocol / ハブ | 実行バイナリなし。ソースアーカイブを利用 |

リリースごとの成果物と CI は [Verification](Verification) を参照してください。

## 位置の書き換え（iPad）

- iPad 側だけが Developer Mode・LocalDevVPN・pairing file・DDI を使います。
- 位置の変更は Apple の非公開 API（`com.apple.dt.simulatelocation`）に依存します。OS の更新で動かなくなる可能性があります。
- 送信側（iPhone / Android）に DDI や pairing file は不要です。

## 未確認

- iPhone Sender の実機動作。
- Android BLE 実機 + iPad の組み合わせ（ドキュメント間で記述が矛盾）。
- 全画面 UI / Dynamic Type / Dark Mode。
- Tailscale リフレクターとの組み合わせ。

いずれも [Status](Status) に根拠をまとめています。
