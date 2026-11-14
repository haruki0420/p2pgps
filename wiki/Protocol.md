# Protocol（BLE GATT v1）

正本は [p2pgps-protocol/spec/protocol-v1.md](https://github.com/haruki0420/p2pgps-protocol/blob/main/spec/protocol-v1.md)。ここでは要点のみ。

## UUID

| 役割 | UUID |
| :--- | :--- |
| P2P GPS Service | `B1E5A000-9C3D-4E7A-8F20-1A2B3C4D5E6F` |
| Location Packet（notify, 20B） | `B1E5A001-9C3D-4E7A-8F20-1A2B3C4D5E6F` |
| Control（write） | `B1E5A002-9C3D-4E7A-8F20-1A2B3C4D5E6F` |
| Status（read/notify, 8B） | `B1E5A003-9C3D-4E7A-8F20-1A2B3C4D5E6F` |
| Extended Location（notify, 8B） | `B1E5A004-9C3D-4E7A-8F20-1A2B3C4D5E6F` |

## Location Packet（20 bytes, little-endian）

| Offset | Size | Field | 説明 |
| ---: | ---: | :--- | :--- |
| 0 | 1 | version | `0x01` |
| 1 | 1 | flags | bit0 VALID_FIX / bit1 ALTITUDE_VALID / bit2 SPEED_VALID / bit3 SIMULATED / bit4 CHARGING / bit5 LOW_BATTERY / bit6 MOVING / bit7 reserved |
| 2 | 2 | sequence | uint16、送信ごとに +1 |
| 4 | 4 | latitude | int32、度 × 10^7 |
| 8 | 4 | longitude | int32、度 × 10^7 |
| 12 | 2 | altitude_m | int16、m |
| 14 | 1 | accuracy_m | uint8、m（255 = 不明） |
| 15 | 1 | speed_mps | uint8、m/s（255 = 不明） |
| 16 | 4 | timestamp | uint32、Unix 秒（UTC） |

例（東京駅）:

```
01 03 2A 00 48 86 44 15 52 C5 4E 53 03 00 05 00 00 52 17 69
```

## Control（受信側 → 送信側）

| opcode | 名称 | payload |
| ---: | :--- | :--- |
| 0x01 | START | uint16 interval_ms（0 = 1000） |
| 0x02 | STOP | なし |
| 0x03 | SET_INTERVAL | uint16 interval_ms |
| 0x04 | REQUEST_FIX | なし |
| 0x05 | SET_EXTENDED | uint8 enabled |
| 0x7F | RESET | なし |

## Status（8 bytes）

`version, state, interval_ms(u16), battery_pct, status_flags, last_error, reserved`

## 検証ルール（受信側）

- 長さ 20、version 1、flags bit7 = 0
- 緯度 ±90°、経度 ±180° の範囲内
- `(0,0)` 近傍は無効扱い
- timestamp が ±24 時間を超えたら stale 警告

## テストベクタ

`p2pgps-protocol/tests/vectors/*.json` にあります。iOS / Android のテストは同じカテゴリ・値のベクタを手動でミラーしています（自動同期は将来の CI 課題）。
