# Troubleshooting

## 接続できない

| 症状 | 確認すること |
| :--- | :--- |
| iPad の一覧に送信側が出ない | 送信側で「送信開始」が ON か。iPad の Bluetooth が ON か。距離（10 m 以内）。Android は位置情報権限が「常に許可」か |
| 接続はできるが位置が来ない | 送信側で START を送っているか（Receiver が自動で START を書きます）。Status の state が Streaming か |
| すぐ切断される | 送信側アプリがバックグラウンドで停止していないか。Android は前景サービス通知が出ているか。iPhone は「常に許可」か |

## 位置が反映されない（iPad）

まず **診断** 画面 →「接続診断を実行」を押してください。pairing file の形式（RPPairing か）、Wi-Fi、Remote Pairing ポートへの TCP 到達性を自動で確認します。「トンネル / DDI」の **FFI エラー**（code とメッセージ）も原因特定に役立ちます。

| 症状 | 対処 |
| :--- | :--- |
| トンネルが繋がらない | LocalDevVPN が接続済みか。Wi-Fi に接続しているか。ターゲット IP が `10.7.0.1` か |
| 診断で pairing file が「lockdown のみ」 | iloader でエクスポートし直す（RPPairing を含むファイル） |
| 診断で TCP が「接続待ち / 失敗」 | LocalDevVPN を再接続。他の VPN を切断。Developer Mode とローカルネットワークの許可を確認 |
| 診断の「Remote Pairing ポート」が Fallback になる | 設定 > プライバシーとセキュリティ > ローカルネットワーク で P2P GPS を ON にして、アプリを再起動 |
| iOS 27 で `ConnectionReset`（code 54）になる | iloader の pairing file が RSD で拒否されることがあります。[idevice_pair](https://github.com/jkcoxson/idevice_pair/releases) で Remote pairing を作り直し、Validate → Save to file → 本アプリで再インポート。改善しなければアプリを完全削除 → iPad 再起動 → 再インストール |
| LocalDevVPN が使えない / 他の VPN と競合する | Tailscale + リフレクターなどの代替手段があります（[Networking](Networking)）。iOS で同時に使える VPN は 1 つだけです |
| `Developer Disk Image is not mounted` | Settings → DDI を再ダウンロード。Developer Mode が ON か |
| `pairing file` エラー | pairing file を再インポート。期限切れの場合は再取得 |
| 注入 ON にしても変わらない | 他に位置シミュレーションを行うアプリ（TLocation / StikDebug）が同時に動いていないか。終了して再試行 |
| ポートが使用中（errno 48） | 他の JIT / デバッグ / VPN アプリを終了。LocalDevVPN を再接続。iPad を再起動 |

## ビルド

| 症状 | 対処 |
| :--- | :--- |
| `libidevice_ffi.a` が無い | `./scripts/fetch-vendor.sh` を実行（Windows は `scripts/fetch-vendor.ps1`） |
| SHA-256 不一致 | ダウンロードが壊れている。再実行。上流のファイルが変わった場合は Issue へ |
| `swift build` で iOS SDK が見つからない | `xtool sdk list` で darwin があるか。`xtool setup` を再実行 |
| リンクエラー `_location_simulation_*` | Vendor の取得と `-L Vendor/idevice -lidevice_ffi` の設定を確認 |

## ログの確認

- iOS: アプリの Diagnostics 画面、または `Console.app` / `idevicesyslog`
- Android: `adb logcat -s GpsSenderService`

## 既知の制約

- 実機での動作検証は未実施です（開発環境に実機が無いため）。
- iOS の位置シミュレーションは Apple の非公開サービスに依存するため、OS アップデートで壊れる可能性があります。
- BLE は 1 対 1 接続のみ（v1）。
