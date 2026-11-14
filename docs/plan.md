# P2P GPS — プロジェクト計画（オーケストレーション）

最終更新: 2026-11-15 / 進行担当: 担当

## 1. ゴール

iPhone / Android で取得した GPS 位置を BLE で iPad に送り、iPad 上で「その位置にいる」ように位置情報を反映するアプリケーション群を作る。iPad 側の位置固定は [StikDebug](https://github.com/StikDebug/StikDebug) 由来の GPS シミュレーション機能（[TLocation](https://github.com/truongkma/t-location) が最小フォークとして公開）を流用する。Mac を持っていないため、iOS ビルドは [xtool](https://github.com/xtool-org/xtool) を前提とする。成果物は GitHub（`haruki0420`）へ公開する。

## 2. 成果物（3 リポジトリ）

| リポジトリ | 内容 | ライセンス |
| :--- | :--- | :--- |
| [`p2pgps-ios`](https://github.com/haruki0420/p2pgps-ios) | iPhone = Sender / iPad = Receiver のユニバーサル SwiftUI アプリ。xtool (SwiftPM) ビルド。Receiver は StikDebug 由来エンジンで位置を注入 | AGPL-3.0（上流の派生のため必須） |
| [`p2pgps-android`](https://github.com/haruki0420/p2pgps-android) | Android Sender。Kotlin + Jetpack Compose、BLE ペリフェラル、前景サービス | MIT |
| [`p2pgps-protocol`](https://github.com/haruki0420/p2pgps-protocol) | BLE GATT プロトコル仕様の正本、Python リファレンス実装、テストベクタ、CLI | MIT |

各リポジトリに Wiki（Home / Getting Started / Protocol / Architecture / Troubleshooting / FAQ）を用意する。`p2pgps-protocol` をドキュメントのハブとする。

## 3. アーキテクチャ概要

```
┌──────────────────────┐        BLE GATT (20B notify, 1Hz)        ┌──────────────────────┐
│ iPhone (Sender)      │ ───────────────────────────────────────▶ │ iPad (Receiver)      │
│  CoreLocation        │   Service B1E5A000-...                   │  CoreBluetooth       │
│  CoreBluetooth       │   Location / Status / Extended           │  MapKit 表示         │
│  peripheral          │ ◀─────────────────────────────────────── │  central             │
└──────────────────────┘        Control (START/STOP/interval)      └──────────┬───────────┘
                                                                             │ 位置注入
┌──────────────────────┐                                                     ▼
│ Android (Sender)     │                                        ┌──────────────────────────┐
│  LocationManager     │                                        │ StikDebug 由来エンジン    │
│  BluetoothLeAdvertiser│                                       │  idevice FFI (静的リンク) │
│  GATT server         │                                        │  pairing file + LocalDevVPN│
└──────────────────────┘                                        │  DDI mount → location_    │
                                                                │  simulation_set()         │
                                                                └──────────────────────────┘
```

## 4. フェーズと担当

| Phase | 内容 | 担当 | 状態 |
| :--- | :--- | :--- | :--- |
| P0 | 調査・設計・プロトコル仕様確定 | lead | ✅ 完了（仕様 v1.0.1） |
| P1 | iOS 実装（Sender/Receiver/注入エンジン/UI） | ios-dev | ✅ 完了（CI 緑: swift test / クロスビルド / xcodebuild リンク） |
| P2 | Android 実装（Sender/BLE/前景サービス/UI） | android-dev | ✅ 完了（CI 緑: test 54 / assembleDebug / lint） |
| P3 | プロトコルリポジトリ（仕様正本/Python 実装/テスト） | protocol-dev | ✅ 完了（pytest 200 / CI 緑） |
| P4 | レビュー（コード・セキュリティ・ライセンス・整合性） | reviewer | ✅ 完了（REVIEW.md / レビュー記録 / REVIEW-FIXES.md / レビュー記録） |
| P5 | 公開（GitHub push、CI 緑、Wiki 整備、Release） | lead | ✅ 完了（4 リポジトリ public・Release 作成。Wiki は初回ページのみ手動作成待ち） |
| P6 | 最終検証・報告 | lead | ✅ 完了 |

## 5. エージェント運用ルール

- ルートはプロジェクトルート（`p2pgps/`）。各エージェントは担当ディレクトリ（`p2pgps-ios/`, `p2pgps-android/`, `p2pgps-protocol/`）のみ書き込む。
- 共有契約は `docs/protocol-spec.md`。勝手に変更しない。変更が必要なら lead に報告。
- 各担当は自分のリポジトリで `git init` + 初回コミットまで行う。**GitHub への push は lead が行う**（レビュー前公開を避けるため）。
- 参照実装: `_research/t-location`（StikDebug の GPS 固定機能の最小フォーク、AGPL-3.0）、`_research/xtool`（xtool 本体・ドキュメント・サンプル）、`_ref/[private-project]` / `_ref/[private-project]`（ユーザーの既存プロジェクトの構成・CI 慣例）。
- ビルド検証は GitHub Actions（macOS / Ubuntu）で行う。ローカルに Xcode / Swift / JDK は無い前提で、CI を緑にするまで lead が修正指示を出す。

## 6. 受け入れ基準

1. 3 リポジトリが public で、README・LICENSE・Wiki が揃っている。
2. iOS: `swift build`（macOS ランナーで iOS 向けクロスビルド）と `xcodebuild`（XcodeGen 生成プロジェクト）が成功。プロトコルのユニットテストが緑。
3. Android: CI で `assembleDebug` とユニットテストが成功。BLE ペリフェラルの実装が仕様の UUID / パケットと一致。
4. Protocol: Python 実装のテストが全緑で、仕様書とテストベクタが一致。
5. レビュー報告書で重大指摘ゼロ（または修正済み）。
6. 既知の制約（iPad 側は Developer Mode + DDI + LocalDevVPN + pairing file が必要、実機検証は未実施 等）が README / Wiki に明記されている。

## 7. リスクと対策

| リスク | 対策 |
| :--- | :--- |
| ローカルに Swift / Java / Android SDK が無くビルドできない | GitHub Actions で検証。iOS は macOS ランナーで SwiftPM クロスビルド + XcodeGen ビルド |
| `libidevice_ffi.a` (92.6 MB) をリポジトリに置けない | `scripts/fetch-vendor.sh` で TLocation の固定コミットから取得し SHA-256 検証。`.gitignore` 対象 |
| StikDebug 由来コードのライセンス | iOS リポジトリを AGPL-3.0 にし、NOTICE に上流コミット・著作権を明記 |
| BLE は実機なしで動作確認できない | プロトコル層を純粋関数としてユニットテスト。受信側にシミュレータ（PC から流す CLI）を用意 |
| iPad の位置注入は Apple 非公開 API 相当で壊れやすい | TLocation と同一の idevice FFI バージョンに固定。失敗時は URL スキームで TLocation に委譲するフォールバックを実装 |
| xtool は Windows ネイティブ非対応（WSL 必須） | README に WSL / Linux 手順を明記。`docs/setup-linux.md` を用意 |

## 8. 進行ログ

- 2026-11-15: P0 完了（調査・仕様・計画）。リポジトリ作成、P1–P3 を並列着手。
