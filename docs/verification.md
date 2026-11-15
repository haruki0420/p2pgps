# 検証とリリース

## リリース

| リポジトリ | 最新リリース | 内容 |
| :--- | :--- | :--- |
| [p2pgps](https://github.com/haruki0420/p2pgps) | [v1.0.0](https://github.com/haruki0420/p2pgps/releases/tag/v1.0.0) | プロジェクトハブ（ドキュメント） |
| [p2pgps-ios](https://github.com/haruki0420/p2pgps-ios) | [v1.0.2](https://github.com/haruki0420/p2pgps-ios/releases/tag/v1.0.2) | 最終レビュー R-1/R-2/R-4/R-15 修正 |
| [p2pgps-android](https://github.com/haruki0420/p2pgps-android) | [v1.0.1](https://github.com/haruki0420/p2pgps-android/releases/tag/v1.0.1) | レビュー指摘 C-3〜C-11 / R 群修正 |
| [p2pgps-protocol](https://github.com/haruki0420/p2pgps-protocol) | [v1.0.1](https://github.com/haruki0420/p2pgps-protocol/releases/tag/v1.0.1) | 仕様 v1.0.1（§5.1 / RESET 明確化） |

## リリース成果物

- **p2pgps-ios**: 各リリースに未署名 IPA（`p2pgps-ios-<tag>-unsigned.ipa`）と SHA-256 を添付。SideStore / AltStore 等で署名してインストールしてください。
- **p2pgps-android**: 各リリースにデバッグ署名済み APK（`p2pgps-android-<tag>-debug.apk`）、未署名リリース APK（`...-release-unsigned.apk`）、`checksums.sha256` を添付。
- **p2pgps-protocol / p2pgps**: 実行バイナリは無し（GitHub のソースアーカイブを利用）。

## CI（GitHub Actions）

- **p2pgps-ios**: `macos-15` で `swift test`（76 tests）→ `scripts/fetch-vendor.sh`（SHA-256 検証）→ `swift build --triple arm64-apple-ios17.0 --sdk …`（iOS クロスビルド）→ XcodeGen + `xcodebuild`（リンクまで）。
- **p2pgps-android**: `ubuntu-latest` + JDK 21 + Android SDK 36 で `testDebugUnitTest`（54 tests）→ `assembleDebug` → `lintDebug`（Error 0）。APK とテスト結果を artifact として保存。
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

- 実機での BLE・位置注入・UI の動作検証は未実施です（開発環境に実機が無いため）。
- iPad 側は Developer Mode・LocalDevVPN・pairing file・DDI が必要です（StikDebug と同じ前提）。
- 位置注入は Apple の Developer Disk Image の仕組みに依存するため、iOS の更新で壊れる可能性があります。
- アプリ再起動後、デバイス側に前回のシミュレーションセッションが残る場合があります（既知の制約）。
- v1 は認証なし・1 対 1 接続です。近距離の第三者が偽の位置を送れるため、注入は既定 OFF・明示操作・注入中は常時バナー表示としています。
