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

各リポジトリに Wiki（Home / Getting Started / Protocol / Architecture / Troubleshooting / FAQ）を用意する。`p2pgps`（このリポジトリ）をドキュメントの入口とする。

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
| P5 | 公開（GitHub push、CI 緑、Wiki 整備、Release） | lead | ✅ 完了（4 リポジトリ public・Release 作成・Wiki 同期済み） |
| P6 | 最終検証・報告 | lead | ✅ 完了 |

## 5. エージェント運用ルール

- ルートはプロジェクトルート（`p2pgps/`）。各エージェントは担当ディレクトリ（`p2pgps-ios/`, `p2pgps-android/`, `p2pgps-protocol/`）のみ書き込む。
- 共有契約は `https://github.com/haruki0420/p2pgps-protocol/blob/main/spec/protocol-v1.md`。勝手に変更しない。変更が必要なら lead に報告。
- 各担当は自分のリポジトリで `git init` + 初回コミットまで行う。**GitHub への push は lead が行う**（レビュー前公開を避けるため）。
- 参照実装: TLocation（StikDebug の GPS 固定機能の最小フォーク、AGPL-3.0）、xtool（xtool 本体・ドキュメント・サンプル）、既存の xtool プロジェクト（構成・CI 慣例）。
- ビルド検証は GitHub Actions（macOS / Ubuntu）で行う。ローカルに Xcode / Swift / JDK は無い前提で、CI を緑にするまで lead が修正指示を出す。

## 6. 受け入れ基準

1. 3 リポジトリが public で、README・LICENSE・Wiki が揃っている。
2. iOS: `swift build`（macOS ランナーで iOS 向けクロスビルド）と `xcodebuild`（XcodeGen 生成プロジェクト）が成功。プロトコルのユニットテストが緑。
3. Android: CI で `assembleDebug` とユニットテストが成功。BLE ペリフェラルの実装が仕様の UUID / パケットと一致。
4. Protocol: Python 実装のテストが全緑で、仕様書とテストベクタが一致。
5. レビュー報告書で重大指摘ゼロ（または修正済み）。
6. 既知の制約（iPad 側は Developer Mode + DDI + LocalDevVPN + pairing file が必要、実機検証は限定的 等）が README / Wiki に明記されている。

## 7. リスクと対策

| リスク | 対策 |
| :--- | :--- |
| ローカルに Swift / Java / Android SDK が無くビルドできない | GitHub Actions で検証。iOS は macOS ランナーで SwiftPM クロスビルド + XcodeGen ビルド |
| `libidevice_ffi.a` (54.4 MB) をリポジトリに置けない | `scripts/fetch-vendor.sh` で StikDebug の固定コミットから取得し SHA-256 検証。`.gitignore` 対象 |
| StikDebug 由来コードのライセンス | iOS リポジトリを AGPL-3.0 にし、NOTICE に上流コミット・著作権を明記 |
| BLE は実機なしで動作確認できない | プロトコル層を純粋関数としてユニットテスト。受信側にシミュレータ（PC から流す CLI）を用意 |
| iPad の位置注入は Apple 非公開 API 相当で壊れやすい | TLocation と同一の idevice FFI バージョンに固定。失敗時は URL スキームで TLocation に委譲するフォールバックを実装 |
| xtool は Windows ネイティブ非対応（WSL 必須） | README に WSL / Linux 手順を明記。`wiki/Build.md` を用意 |

## 8. 進行ログ

- 2026-11-15: P0 完了（調査・仕様・計画）。リポジトリ作成、P1–P3 を並列着手。
- 2026-11-15: P1–P6 完了（実装・レビュー・公開・Release）。最終レビューで重大 0 件を確認。
- 2026-11-15: ユーザー指示により 4 リポジトリを **public** に変更（個人データ監査済み）。


---

# レビューと修正の記録

P2P GPS は「計画 → 実装 → レビュー → 修正 → 公開」を補助担当連携で実施しました。このページは公開用の要約です（詳細なレビュー報告書はリポジトリ外の作業ディレクトリに保持）。

## レビューの流れ

| ラウンド | 対象 | 主な指摘 | 結果 |
| :--- | :--- | :--- | :--- |
| 1 | protocol / Android | 重大 2 件（Control `interval_ms` の 3 実装不一致、Python `FixFilter` の no-fix 誤受理）、中 9 件、軽微 27 件 | すべて修正。テストベクタを 3 実装で共有 |
| 2 | iOS 正式レビュー | 重大 3 件（Receiver のバックグラウンド維持が未実装、stale fix の破棄、pairing file の二重保存）、中 13 件、軽微 20 件 | すべて修正（M6 の FFI 所有権のみ上流由来の既知の制約として文書化） |
| 3 | 全体の最終確認 | 重大 1 件（注入 OFF 直後にデバイス側セッションが残る regression）、中 3 件、軽微 13 件 | 修正。最終判定 **重大 0 件・リリース可** |

## 主な修正

- **プロトコル**: `interval_ms` の正規化を仕様 §5.1 で明確化（0→1000 / 1–99→100 / 100–60000 そのまま / 60001–65535→60000）。`RESET` はストリーミング状態を変更しない。共有テストベクタ 45 件を iOS / Android / Python が実際に読み込んで検証。
- **Android**: GATT サーバのスレッド安全性、端末名復元、coarse-only 権限、ダークコントラスト、状態テキスト、IME、`BLUETOOTH_SCAN` 削除、Dynamic Type 対応。
- **iOS**: バックグラウンド維持（`BackgroundKeepAlive`）、stale は警告のみ、pairing file の保存強化（Application Support / 0600 / Data Protection / backup 除外）、トンネル再接続と FFI 直列化、DDI の固定コミット + SHA-256 検証、購読者追跡、再接続、設定反映、RSSI、VoiceOver、ライセンス帰属。
- **注入の安全性**: 注入 ON → 直後 OFF でもデバイス側セッションが残らないよう、clear の常時キューイングと世代番号による順序保証を実装。

## 検証エビデンス

| リポジトリ | CI | 結果 |
| :--- | :--- | :--- |
| p2pgps-ios | GitHub Actions `macos-15` | `swift test` 76 tests / SwiftPM iOS クロスビルド / XcodeGen + `xcodebuild` リンク **成功** |
| p2pgps-android | GitHub Actions `ubuntu-latest` | `testDebugUnitTest` 54 tests / `assembleDebug` / `lintDebug`（Error 0）**成功** |
| p2pgps-protocol | GitHub Actions `ubuntu-latest` + `windows-latest` | `pytest` 200 passed **成功** |

- 共有テストベクタ 5 ファイルの SHA-256 が 3 リポジトリで一致することを確認。
- DDI の固定コミット `a1020f81b6429f5ce40408cbe21c690512b613b5` と 3 ファイルの SHA-256 を独立検証。
- BLE 購読・位置注入は Android 実機 + iPad で確認済み。全画面 UI は未確認です（CI はコンパイル・リンク・ユニットテストまで）。
