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
| [xtool](https://github.com/xtool-org/xtool) | MIT | Mac なしの iOS ビルドツールチェーン |
| [doronz88/DeveloperDiskImage](https://github.com/doronz88/DeveloperDiskImage) | 上流に従う | DDI ファイル配布元 |

## AGPL-3.0 の注意

`p2pgps-ios` は AGPL-3.0 です。改変版をネットワーク経由で提供する場合は、ソースコードの提供義務があります（AGPL §13）。サイドロード配布のみなら通常の GPL と同様です。

## 帰属

`p2pgps-ios` の NOTICE に上流の著作権表示とコミットハッシュを記載しています。詳細は [docs/licensing.md](https://github.com/haruki0420/p2pgps/blob/main/docs/licensing.md) を参照してください。
