# 検証とリリース

> このページは開発者向けです。

## リリース

| リポジトリ | 最新リリース | 内容 |
| :--- | :--- | :--- |
| [p2pgps](https://github.com/haruki0420/p2pgps) | [v1.0.0](https://github.com/haruki0420/p2pgps/releases/tag/v1.0.0) | プロジェクトハブ（ドキュメント） |
| [p2pgps-ios](https://github.com/haruki0420/p2pgps-ios) | [Releases](https://github.com/haruki0420/p2pgps-ios/releases) | 最新版を参照 |
| [p2pgps-android](https://github.com/haruki0420/p2pgps-android) | [Releases](https://github.com/haruki0420/p2pgps-android/releases) | 最新版を参照 |
| [p2pgps-protocol](https://github.com/haruki0420/p2pgps-protocol) | [Releases](https://github.com/haruki0420/p2pgps-protocol/releases) | 最新版を参照 |

## リリース成果物

- **p2pgps-ios**: 各リリースに未署名 IPA（`p2pgps-ios-<tag>-unsigned.ipa`）と SHA-256 を添付。SideStore / AltStore 等で署名してインストールしてください。
- **p2pgps-android**: 各リリースにデバッグ署名済み APK（`p2pgps-android-<tag>-debug.apk`）、リリース署名済み APK（`p2pgps-android-<tag>-release.apk`）、`checksums.sha256` を添付。
- **p2pgps-protocol / p2pgps**: 実行バイナリは無し（GitHub のソースアーカイブを利用）。

## CI（GitHub Actions）

- **p2pgps-ios**: `macos-15` で `swift test` → `scripts/fetch-vendor.sh`（SHA-256 検証）→ `swift build --triple arm64-apple-ios17.0 --sdk …`（iOS クロスビルド）→ XcodeGen + `xcodebuild`（リンクまで）。
- **p2pgps-android**: `ubuntu-latest` + JDK 21 + Android SDK 36 で `testDebugUnitTest` → `assembleDebug` → `lintDebug`（Error 0）。APK とテスト結果を artifact として保存。
- **p2pgps-protocol**: `ubuntu-latest` / `windows-latest` + Python 3.12 で `pip install -e ".[test]"` → `pytest`（200 passed）→ CLI スモーク（encode / decode / vectors）。

## 再現手順

```bash
# iOS（Linux / WSL + xtool）
cd p2pgps-ios
./scripts/fetch-vendor.sh
xtool dev build

# Android
cd p2pgps-android
./gradlew :app:testDebugUnitTest :app:assembleDebug

# Protocol
cd p2pgps-protocol
pip install -e ".[test]"
python -m pytest
```

## 既知の制約

- 実機での確認範囲（BLE 接続・位置の書き換え・全画面 UI）は [Status](Status) にまとめています。
- iPad 側は Developer Mode・LocalDevVPN・pairing file・DDI が必要です（StikDebug と同じ前提）。
- 位置の書き換えは Apple の Developer Disk Image の仕組みに依存するため、iOS の更新で壊れる可能性があります。
- アプリ再起動後、デバイス側に前回のシミュレーションセッションが残る場合があります（既知の制約）。
- v1 は認証なし・1 対 1 接続です。近距離の第三者が偽の位置を送れるため、位置の書き換えは既定 OFF・明示操作・書き換え中は常時バナー表示としています。
