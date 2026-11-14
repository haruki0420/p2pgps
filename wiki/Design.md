# Design（視覚世界とトークン）

P2P GPS の UI は **Operate モード**（利用者がタスクを完了するアプリ）として設計します。
視覚世界は「**測量標（benchmark）**」— 地図と座標が主役の計測器です。装飾ではなく、読むための画面。

- 正本: [p2pgps/DESIGN.md](https://github.com/haruki0420/p2pgps/blob/main/DESIGN.md) / [PRODUCT.md](https://github.com/haruki0420/p2pgps/blob/main/PRODUCT.md)
- 対象: iOS/iPadOS（SwiftUI / HIG）と Android（Compose / Material 3）の両方

## 原則

1. **座標が主役**。画面で最も大きい数字が緯度経度。UI は黒子。
2. **構造はヘアラインと余白**。カードの山・グラデーション・影・絵文字アイコンは禁止。
3. **記憶に残る要素は 1 つ**。リードアウトプレートと、地図上のクロスヘア + レンジリング。
4. **状態は色だけに頼らない**。アイコン + テキスト + 形で伝える。
5. **ネイティブ作法**。HIG / Material 3 のコントロールはそのまま使う。

## トークン（light）

| token | hex | 用途 |
| :--- | :--- | :--- |
| paper | `#F2F4F2` | 背景 |
| surface | `#FBFCFB` | プレート |
| ink | `#17252A` | 本文・座標 |
| inkSecondary | `#55666A` | ラベル |
| line | `#C9D3CE` | ヘアライン |
| pine | `#1E6B5A` | 主アクション・接続・軌跡 |
| live | `#A8502E` | 注入 ON |
| liveFill | `#B85C38` | ライブの塗り |
| amber | `#8A5A12` | 警告 |
| danger | `#A32E24` | エラー |

dark は [DESIGN.md](https://github.com/haruki0420/p2pgps/blob/main/DESIGN.md) を参照。

## タイポグラフィ

- UI: SF Pro（iOS）/ Roboto（Android）、Dynamic Type / sp スケール。
- **座標・数値: SF Mono / Roboto Mono、tabular figures**。
- カスタムフォントは使わない。見出し上の ALL CAPS アイブロウは禁止。

## 画面

- **Receiver（iPad）**: 上部ステータスレール（LED + 状態テキスト + 送信元 + 最終受信 + シグナルバー + 精度）→ フルブリード地図（クロスヘア + レンジリング + 軌跡）→ 下部リードアウトプレート（座標 + 標高/精度/速度 + 52pt の「位置情報を反映」トグル）。注入中は上部にライブバナー。
- **Sender（iPhone / Android）**: リードアウトプレート + 状態テキスト + 52pt 主ボタン + BLE 3 状態。
- **Home**: カードではなく 2 行のロール選択。
- **Settings / Diagnostics**: ネイティブの Form / List。
- 塗りボタンの文字色は **`onPrimary`**（light: 白、dark: `paper` #0F1A1E）。白固定は禁止（dark の pine #6FBFA8 に白は 2.17:1 で不合格）。

## モーション

- fix 到着: 座標の 120ms クロスフェードのみ。
- 接続中: LED は静的表示 + 状態テキスト（パルスは使わない）。
- 注入 ON/OFF: プレート枠色 200ms。
- Reduce Motion 時は無効化。

## コピー

- 日本語。ボタンは動作を名指し（「送信を開始」「反映を停止」「再試行」）。
- エラーは「何が起きたか + どう直すか」の 2 文。
- 感嘆符・絵文字・フィラーは使わない。

## Anti-slop チェックリスト

- [ ] クリーム背景 + セリフ + テラコッタ / 近黒 + 蛍光アクセント のテンプレにしていない
- [ ] 同一角丸カードの乱用・影の乱用・グラデーション・絵文字アイコンがない
- [ ] ALL CAPS アイブロウ、`A · B · C` メタ、`→` 付きボタンがない
- [ ] 座標が画面で最も大きい数字になっている
- [ ] 状態が色だけで伝わっていない（LED には状態テキストを併記）
- [ ] 44×44pt / Dynamic Type / Reduce Motion に対応
- [ ] 塗りボタンの文字色が `onPrimary`（白固定でコントラスト不足にしていない）

## スキルの導入

このプロジェクトでは以下の DSH スキルを導入しています（`~/.dsh/skills/`）。

- `impeccable` — デザインの方向づけ・critique・native audit・DESIGN.md 生成
- `frontend-design` — テンプレ的でない視覚設計のガイド
- `web-design-guidelines` — UI コードのレビュー観点

ネイティブアプリのため `impeccable` の native モード（HIG / Material 3）を使用します。
