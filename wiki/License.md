# License

## リポジトリ別

| リポジトリ | ライセンス |
| :--- | :--- |
| [p2pgps-ios](https://github.com/haruki0420/p2pgps-ios) | **AGPL-3.0**（StikDebug / TLocation の派生のため） |
| [p2pgps-android](https://github.com/haruki0420/p2pgps-android) | **MIT** |
| [p2pgps-protocol](https://github.com/haruki0420/p2pgps-protocol) | **MIT** |
| このハブ（ドキュメント） | **MIT**（ただし仕様・図は各リポジトリのライセンスに従う） |

## 上流プロジェクト

| プロジェクト | ライセンス | 用途 |
| :--- | :--- | :--- |
| [StikDebug](https://github.com/StikDebug/StikDebug) | AGPL-3.0 | オンデバイス位置シミュレーションの原実装 |
| [TLocation](https://github.com/truongkma/t-location) | AGPL-3.0 | StikDebug の GPS 固定機能の最小フォーク（移植元） |
| [idevice](https://github.com/jkcoxson/idevice) | MIT | Apple デバイスサービス通信ライブラリ（`libidevice_ffi.a`） |
| [Material Icons](https://github.com/google/material-design-icons) | Apache-2.0 | Android のランチャー / 通知アイコンの位置ピンの元図形 |
| [xtool](https://github.com/xtool-org/xtool) | MIT | Mac なしの iOS ビルドツールチェーン |
| [doronz88/DeveloperDiskImage](https://github.com/doronz88/DeveloperDiskImage) | 上流に従う | DDI ファイル配布元 |

## 画像・アイコン

| 対象 | 出典・ライセンス |
| :--- | :--- |
| iOS アプリアイコン | 本プロジェクトのオリジナル（測量標モチーフ）。第三者素材は不使用 |
| Android ランチャー / 通知アイコン | Material Icons の位置ピン（Apache-2.0）の派生。`p2pgps-android/NOTICE` に帰属を記載 |
| README のバッジ | shields.io が生成（リポジトリに画像ファイルは含めない） |
| StikDebug / TLocation / iloader のスクリーンショット | 本プロジェクトには含めていない |

## AGPL-3.0 の注意

`p2pgps-ios` は AGPL-3.0 です。改変版をネットワーク経由で提供する場合は、ソースコードの提供義務があります（AGPL §13）。サイドロード配布のみなら通常の GPL と同様です。

## 帰属

`p2pgps-ios` の NOTICE に上流の著作権表示とコミットハッシュを記載しています。詳細は [docs/licensing.md](https://github.com/haruki0420/p2pgps/blob/main/docs/licensing.md) を参照してください。
