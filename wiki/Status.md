# 状態（Status）

最終更新: 2026-11-21

このページがプロジェクト全体の状態の正本です。他ページはここへリンクし、状態を重複して書かないでください。断定できないものは「要確認」とし、根拠ページへリンクします。

| 領域 | 項目 | 状態 | 根拠・備考 |
| :--- | :--- | :--- | :--- |
| iOS | コンパイル / ユニットテスト | 確認済み | CI（macOS）で `swift test` → iOS クロスビルド → XcodeGen + `xcodebuild`。[Verification](Verification) に手順。最新の実行結果は [Actions](https://github.com/haruki0420/p2pgps-ios/actions) を参照 |
| iOS | iPhone Sender 実機 | 未確認 | ドキュメントに iPhone 実機で送信を確認した記述がない |
| iOS | iPad Receiver + 位置注入 | 要確認 | 「Android 実機 + iPad で確認済み」という記述と、注入は実機必須・CI はコンパイルのみという記述（[iOS Architecture](https://github.com/haruki0420/p2pgps-ios/wiki/Architecture) / [Build](https://github.com/haruki0420/p2pgps-ios/wiki/Build)）が併存している。iOS 実機での再確認が必要 |
| Android | ビルド / JVM テスト | 確認済み | CI（Ubuntu / JDK 21 / Android SDK 36）で `testDebugUnitTest` → `assembleDebug` → `lintDebug`。[Verification](Verification) に手順 |
| Android | BLE 実機 + iPad | 要確認 | [Testing](https://github.com/haruki0420/p2pgps-android/wiki/Testing) §5 は BLE ペリフェラルの実機動作（アドバタイズ・接続・CCCD・notify・MTU）を未検証と記載。以前の Home / FAQ の「確認済み」記述と矛盾していたため、実機での再確認が必要 |
| Android | 公開リポジトリ | public | 2026-11-21 に private から public へ切り替え済み（ユーザー確認）。[Repository](https://github.com/haruki0420/p2pgps-android) |
| UI | 全画面 UI / Dynamic Type / Dark Mode | 未確認 | 実機でのレンダリング確認は未実施（[Design](Design) / [iOS Design](https://github.com/haruki0420/p2pgps-ios/wiki/Design) / [Android Design](https://github.com/haruki0420/p2pgps-android/wiki/Design)） |
| ネットワーク | Tailscale リフレクター | 未確認 | コミュニティ実装の情報に基づく。[Networking](Networking) に「本アプリとの組み合わせは実機未検証」と記載 |
| Protocol | 仕様 / テストベクタ | 確認済み | 仕様 v1.0.1、Python テスト 200 件が CI（Linux / Windows）で通過。macOS は未検証（[Testing](https://github.com/haruki0420/p2pgps-protocol/wiki/Testing)） |

## 更新のしかた

- 実機で確認したら、この表の状態と根拠を更新する。
- 他ページには状態を書かず、このページへのリンクを置く。
- 「確認済み」と書けるのは、再現手順と結果が残っている場合だけ。
