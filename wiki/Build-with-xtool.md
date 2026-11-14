# Build with xtool（Mac なしで iOS アプリをビルド）

`p2pgps-ios` は [xtool](https://github.com/xtool-org/xtool) を使って、Linux / WSL 上で iOS アプリをビルド・インストールできます。macOS は不要です。

## 前提

| 項目 | 内容 |
| :--- | :--- |
| OS | Linux（Arch / Ubuntu など）または Windows + WSL2 |
| Swift | 6.4 ツールチェーン（[swift.org](https://www.swift.org/install/linux/)） |
| usbmuxd | `usbmuxd`（libimobiledevice） |
| Xcode.xip | Apple Developer Downloads から取得（要 Apple ID ログイン） |
| Apple ID | `xtool setup` でログイン（無料 Apple ID はパスワード方式） |
| 実機 | Developer Mode を有効にした iPhone / iPad |

## 手順

```bash
# 1. xtool 本体（AppImage）
curl -fL "https://github.com/xtool-org/xtool/releases/latest/download/xtool-$(uname -m).AppImage" -o ~/.local/bin/xtool
chmod +x ~/.local/bin/xtool

# 2. セットアップ（Apple ID ログイン + Xcode.xip から iOS SDK を生成）
xtool setup
xtool sdk list        # darwin が出れば OK

# 3. ビルド
git clone https://github.com/haruki0420/p2pgps-ios.git
cd p2pgps-ios
./scripts/fetch-vendor.sh    # libidevice_ffi.a を取得（約 93 MB、SHA-256 検証）
xtool dev build

# 4. 実機へインストール
idevice_id -l                # UDID が見えることを確認
xtool dev run
```

## Windows の場合

xtool は Windows ネイティブでは動作しません。**WSL2** を使い、USB パススルー（usbipd）で iOS 端末を WSL に渡してください。詳細は xtool の [Installation (Linux/Windows)](https://xtool.sh/documentation/xtooldocs/installation-linux) を参照。

## トラブル

- `Error: AFCClient.Error.muxError` → [xtool issue #19 のコメント](https://github.com/xtool-org/xtool/issues/19#issuecomment-2898986718)（iTunes 経由のリレー）を参照。
- `libncurses.so.6` が無い（Arch）→ `sudo ln -s libncursesw.so.6 /usr/lib/libncurses.so.6`
- Swift が Ubuntu 向けビルドのため Arch で動かない → swiftly で `--platform ubuntu24.04` を指定。

## CI での検証

GitHub Actions（macOS ランナー）で以下を検証しています。

1. `swift test`（プロトコル/コアのユニットテスト）
2. `swift build --triple arm64-apple-ios17.0 --sdk ...`（iOS 向けコンパイル）
3. XcodeGen + `xcodebuild`（アプリのリンクまで）
