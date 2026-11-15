# ライセンスと帰属

P2P GPS は複数の上流プロジェクトの上に成り立っています。リポジトリごとにライセンスが異なるため、配布・改変時は以下を確認してください。

## リポジトリ別ライセンス

| リポジトリ | ライセンス | 理由 |
| :--- | :--- | :--- |
| `p2pgps-ios` | **AGPL-3.0** | StikDebug / TLocation のコード（位置シミュレーションエンジン）を移植しているため。上流と同じ AGPL-3.0 を継承 |
| `p2pgps-android` | **MIT** | 独自実装。AGPL コードを含まない |
| `p2pgps-protocol` | **MIT** | 仕様とリファレンス実装は独自 |

`p2pgps-ios` は AGPL-3.0 のため、**改変版をネットワーク経由で提供する場合はソースコードの提供義務**があります（AGPL §13）。サイドロード配布のみなら通常の GPL と同様です。

## 上流プロジェクト

| プロジェクト | ライセンス | 用途 |
| :--- | :--- | :--- |
| [StikDebug](https://github.com/StikDebug/StikDebug)（© Stephen Bove / StikDebug contributors） | AGPL-3.0 | オンデバイス位置シミュレーションの原実装。`p2pgps-ios` の `P2PGPSInjection` はこの派生 |
| [TLocation](https://github.com/truongkma/t-location) | AGPL-3.0 | StikDebug から GPS 固定機能だけを残した最小フォーク。移植元として参照（コミット `5e57f815e5958f133dfbaae8252473054adeccf0`） |
| [idevice](https://github.com/jkcoxson/idevice)（© jkcoxson） | MIT | Apple デバイスサービスとの通信ライブラリ。`libidevice_ffi.a` として静的リンク |
| [libplist](https://github.com/libimobiledevice/libplist)（© Nikias Bassen / Jonathan Beck） | LGPL-2.1-or-later | `idevice.h` に含まれる plist 実装部分。`p2pgps-ios` の `Vendor/idevice/LICENSE.libplist` に全文を同梱 |
| [xtool](https://github.com/xtool-org/xtool) | MIT | Mac なしで iOS アプリをビルドするツールチェーン |
| [Material Icons](https://github.com/google/material-design-icons)（© Google LLC） | Apache-2.0 | Android のランチャー / 通知アイコンの位置ピン（`ic_launcher_foreground.xml` / `ic_stat_location.xml`）の元図形 |
| [doronz88/DeveloperDiskImage](https://github.com/doronz88/DeveloperDiskImage) | 上流の表記に従う | DDI ファイルの配布元（アプリが実行時にダウンロード） |
| [LocalDevVPN](https://apps.apple.com/us/app/localdevvpn/id6755608044) | プロプライエタリ（無料） | オンデバイス RSD 接続のためのループバック VPN |

## 画像・アイコン

| 対象 | 出典・ライセンス |
| :--- | :--- |
| iOS アプリアイコン（`p2pgps-ios/Resources/AppIcon*.png`） | 本プロジェクトのオリジナル（測量標モチーフ）。第三者素材は不使用 |
| Android ランチャーアイコン（`ic_launcher_foreground.xml`） | Material Icons の位置ピン（Apache-2.0）を元にした派生。`p2pgps-android/NOTICE` に帰属を記載 |
| Android 通知アイコン（`ic_stat_location.xml`） | Material Icons の "place"（Apache-2.0）の派生。`p2pgps-android/NOTICE` に帰属を記載 |
| README のバッジ | shields.io が生成する画像（外部サービス）。リポジトリには画像ファイルを含めない |
| StikDebug / TLocation / iloader のスクリーンショット | 本プロジェクトには含めていない |

## `p2pgps-ios` の NOTICE（要旨）

```
P2P GPS iOS
Copyright (C) 2026 haruki0420 and contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program incorporates code derived from:
  - StikDebug (https://github.com/StikDebug/StikDebug), AGPL-3.0
  - TLocation (https://github.com/truongkma/t-location), AGPL-3.0
    (commit 5e57f815e5958f133dfbaae8252473054adeccf0)
  - idevice (https://github.com/jkcoxson/idevice), MIT
  - libplist (https://github.com/libimobiledevice/libplist), LGPL-2.1-or-later
    (idevice.h に含まれる plist 実装部分。全文は Vendor/idevice/LICENSE.libplist)
```

## バイナリの扱い

`libidevice_ffi.a`（約 54.4 MB）はリポジトリに含めず、`scripts/fetch-vendor.sh` が StikDebug の固定コミットから取得して SHA-256 を検証します。

- SHA-256: `4DB23FE1D342927B9480BB9A8577F219994365621DC28AA0018E23EA1990ECC8`
- 取得元: `https://raw.githubusercontent.com/StikDebug/StikDebug/7a80dfce28eeb501faca6498d1746949ac921e74/StikDebug/idevice/libidevice_ffi.a`

MIT ライセンスの `idevice.h` と `module.modulemap` はリポジトリに含めます（帰属表示付き）。
