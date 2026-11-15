# 困ったとき

## まず確認すること

1. 送信側で「送信を開始」を押しているか
2. iPad の Bluetooth が ON か
3. 2 台を近く（10 m 以内）に置いているか
4. iPad で LocalDevVPN が接続済みか
5. iPad で Developer Mode が ON か

## 症状別

| 症状 | 対処 |
| :--- | :--- |
| iPad の一覧に送信側が出ない | 送信側で「送信を開始」を押す。iPad の Bluetooth を ON。近づける。Android は位置情報を「常に許可」にする |
| 接続できるが位置が来ない | 送信側が現在地を測位できているか確認。屋内では時間がかかることがある。iPad 側で「位置情報を反映」が ON か確認 |
| すぐ切れる | 送信側アプリを画面の前に出す。Android は通知が出ているか確認。iPhone は位置情報を「常に許可」にする |
| 位置が変わらない | iPad で「位置情報を反映」を ON にする。他の位置変更アプリ（TLocation / StikDebug）が動いていないか確認 |
| DDI がマウントできない | 設定で DDI をダウンロードし直す。Developer Mode と LocalDevVPN を確認 |
| pairing file が通らない | 設定で pairing file を読み込み直す。iOS 27 では下の「iOS 27 の pairing file」を見る |
| ポートが使用中と言われる | 他の VPN / デバッグアプリを終了。LocalDevVPN を再接続。iPad を再起動 |

## iOS 27 の pairing file

iOS 27 では、iloader が作る pairing file が iPad に拒否されることがあります。

- 実機（iOS 27.2 / Windows）では、iloader では直らず、**`idevice_pair--windows-x86_64`（Windows x86_64 版）** で作り直すと成功しました。
- 手順: [idevice_pair](https://github.com/jkcoxson/idevice_pair/releases) を起動 → デバイスを選ぶ → Remote pairing → Create → Validate → Save to file → アプリの設定で古い pairing file を削除 → 新しいファイルを読み込む。

## 詳しい情報（開発者向け）

- 接続の確認は、アプリの「困ったとき」画面で「つながらないときの確認」を押す。
- 技術的なエラー（`ConnectionReset`、`FFI`、`RSD`、`DDI` など）は、同じ画面の「動作記録」に残る。
- ビルドで `libidevice_ffi.a` が無い場合は `./scripts/fetch-vendor.sh` を実行する（Windows は `scripts/fetch-vendor.ps1`）。

## 既知の制約

- BLE 購読・位置注入・シミュレート位置の移動は Android 実機 + iPad で確認済みです。全画面 UI・Dynamic Type・Dark Mode は未確認です。
- iPad の位置変更は Apple の非公開機能に依存するため、OS の更新で動かなくなる可能性があります。
- Bluetooth は 1 対 1 接続です。
