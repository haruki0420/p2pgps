# Design

> `p2pgps` の視覚世界（visual world）とトークン。**Operate モード**（利用者がタスクを完了するアプリ UI）。
> iOS / Android の両方に適用する。実装より先にこのファイルが正であり、UI 変更はここを更新してから行う。
> 全画面のレンダリング確認は未実施です（実機で確認してください）。

## Surface

- Mode: **Operate**（スキャン性・一貫性・ネイティブ作法が優先。ブランドは精密なディテールに宿す）
- Platform: `adaptive` — iOS/iPadOS は HIG、Android は Material 3。共通の視覚世界を各 OS の作法に翻訳する。
- 画面: Home（ロール選択）、Receiver、Sender、Settings、Diagnostics

## Visual world — 「測量標（benchmark）」

地図と座標が主役の**計測器**。装飾ではなく、読むための画面。
参照する世界: 測量標・海図・GPS 受信機の表示部。真鍮のセオドライト、ベンチマークプレート、
等高線、レンジリング。**「かわいいカードの寄せ集め」にはしない。**

- 画面の主役は **座標の数字**。UI は黒子に徹する。
- 構造はヘアライン（1px の罫線）と余白で作る。影・グラデーション・カードの山は使わない。
- 記憶に残る要素は 1 つだけ: **リードアウトプレート**（下部の座標パネル）と、地図上の**クロスヘア + レンジリング**。
- 色は「紙（paper）・インク（ink）・パイン（pine）・ライブ（live）」の 4 系統に絞る。

## Color tokens

### Light

| token | hex | 用途 |
| :--- | :--- | :--- |
| `paper` | `#F2F4F2` | 画面背景（地図以外） |
| `surface` | `#FBFCFB` | リードアウトプレート・シート |
| `ink` | `#17252A` | 本文・座標 |
| `inkSecondary` | `#55666A` | ラベル・補助 |
| `line` | `#C9D3CE` | ヘアライン・区切り |
| `pine` | `#1E6B5A` | 主アクション・接続済み・軌跡 |
| `live` | `#A8502E` | 注入 ON・ライブ状態（テキストにも使える濃さ） |
| `liveFill` | `#B85C38` | ライブの塗り（文字は白。コントラスト 4.54:1） |
| `amber` | `#8A5A12` | 警告・stale（テキスト用） |
| `danger` | `#A32E24` | エラー |

### Dark

| token | hex | 用途 |
| :--- | :--- | :--- |
| `paper` | `#0F1A1E` | 背景 |
| `surface` | `#16252A` | プレート |
| `ink` | `#E8EEEC` | 本文・座標 |
| `inkSecondary` | `#9FB0B2` | ラベル |
| `line` | `#2A3B40` | ヘアライン |
| `pine` | `#6FBFA8` | 主アクション・接続済み |
| `live` | `#E08A5F` | 注入 ON |
| `liveFill` | `#C96A42` | ライブの塗り |
| `amber` | `#E0B25C` | 警告 |
| `danger` | `#E0705F` | エラー |

- 状態色は必ず **アイコン + テキスト + 形** と併用（色だけに依存しない）。
- グラデーション禁止。影は使わない（`line` と `surface` の差で階層を作る）。
- 既定の青 tint は使わない。ブランドの色は `pine`。
- **塗りボタンの文字色は `onPrimary` を使う**（light: 白、dark: `paper` #0F1A1E）。白固定は禁止。dark の `pine` #6FBFA8 に白を載せるとコントラスト 2.17:1 で不合格。

## Typography

| 役割 | iOS | Android | 備考 |
| :--- | :--- | :--- | :--- |
| 画面タイトル | `.title2` semibold（SF Pro） | `titleLarge`（Roboto） | 日本語は system |
| 本文・ラベル | `.body` / `.subheadline` | `bodyMedium` / `labelMedium` | Dynamic Type 追従 |
| **座標** | `.title3` **monospaced** semibold | `titleMedium` **Roboto Mono** | 数字は tabular。折り返し許容 |
| 補助数値（標高・精度・速度） | `.footnote` **monospaced** | `bodySmall` **Roboto Mono** | |
| hex / ログ | `.caption` **monospaced** | `bodySmall` **Roboto Mono** | |

- カスタムフォントは使わない（SF Pro / SF Mono / Roboto / Roboto Mono のみ）。
- すべての数値に tabular figures（`.monospacedDigit()` / `FontFeatureSettings("tnum")`）。
- 見出しの上に ALL CAPS のアイブロウラベルを付けない。
- 1 語だけ色や斜体で強調しない。

## Layout

### Receiver（iPad）

```
┌──────────────────────────────────────────────┐
│ ● P2PGPS-IOS-7F3C   最終受信 0.8s   ▂▄▆█ ±5m │  status rail (hairline bottom)
├──────────────────────────────────────────────┤
│                                              │
│                 ✛  (crosshair)               │  Map (full-bleed)
│            ◎ range rings                     │  trail = pine
│                                              │
├──────────────────────────────────────────────┤
│  緯度  35.6812360                            │  readout plate (surface, top corners 16)
│  経度 139.7671250                            │  coordinates: mono title3
│  標高 3m   精度 ±5m   速度 0.0m/s  更新 0.8s │  metrics: mono footnote
│  ┌────────────────────────────────────────┐  │
│  │        位置情報を反映（OFF）            │  │  primary toggle 52pt
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

- ステータスレールは高さ 44–56pt。左: 接続 LED + **状態テキスト** + 送信元名、中央: 最終受信、右: シグナルバー（4 本）+ 精度。
- 地図はフルブリード。ピンではなく **クロスヘア + 3 本のレンジリング**（10/50/100 m 目安）。
- リードアウトプレートは上端のみ角丸 16pt、上辺にヘアライン。カードを並べない。
- 注入中は画面上部（safe area inset）に **ライブバナー**: `liveFill` 10% 背景 + `live` の左ボーダー、送信元・座標・停止ボタン。

### Sender（iPhone / Android）

- 上部: 同じリードアウトプレート（座標 + 精度 + fix 品質バー）。
- 中央: 状態テキスト「送信中」/「停止中」と送信間隔（mono）。
- 下部: 主ボタン「送信を開始」/「送信を停止」（52pt、`pine` 塗り、文字は `onPrimary`）。
- BLE の状態を「アドバタイズ中 / 接続 1 台 / 購読 0」の 3 状態で明示。

### Home / Settings / Diagnostics

- Home: ロール選択は 2 行の大きな行（カードではない）。ヘアライン区切り、アイコンタイルなし。
- Settings / Diagnostics: ネイティブの `Form` / `List`（inset grouped）。カードを作らない。tint だけトークンに合わせる。

## Components

| 名前 | 仕様 |
| :--- | :--- |
| Status rail | 背景 `paper`、下辺 `line` 1px。LED は 8pt 円（接続=pine、待機=amber、エラー=danger、未接続=inkSecondary の輪郭）。**LED の隣に状態テキストを必ず併記**（色だけに依存しない） |
| Signal bars | 4 本の縦バー（3×10pt、間隔 2pt）。受信強度/購読状態を表現。色は `ink`、未達は `line` |
| Readout plate | `surface`、上角丸 16pt、上辺 `line`、内側 16pt パディング |
| Primary action | 高さ 52pt、角丸 10pt、`pine` 塗り / 文字は `onPrimary`（light: 白、dark: `paper`）。押下で 0.98 スケール |
| Live toggle | 高さ 52pt、角丸 10pt。OFF: `surface` + `line` 枠 + `ink` 文字。ON: `liveFill` 塗り + 文字は白 + 左に 3pt の `live` バー |
| Live banner | `liveFill` 10% 背景、左 3pt `live` ボーダー、`ink` 文字、右に「停止」 |
| Range rings | `pine` 12% の線、1px、破線なし。中心クロスヘアは `pine` |
| Trail | `pine` 70% の 3pt ライン、丸キャップ |

## Motion

- fix 到着時: 座標数字の **120ms クロスフェード**のみ（スライドイン禁止）。
- 接続中: LED は静的表示 + 状態テキスト（パルスは使わない。Reduce Motion と実装差を避けるため v1.0.1 で削除）。
- 注入 ON/OFF: プレートの枠色 200ms。
- Reduce Motion 時はすべて無効化。画面遷移は OS 標準のみ。

## Copy

- 日本語。ボタンは動作を名指し: 「送信を開始」「送信を停止」「接続する」「反映を停止」「再試行」。
- 状態: 「最終受信 0.8 秒前」「精度 ±5 m」「送信元 P2PGPS-IOS-7F3C」「購読 0 台」。
- エラーは 2 文: 何が起きたか + どう直すか。例:「LocalDevVPN が未接続です。VPN を接続してから再試行してください。」
- 感嘆符・絵文字・「〜しましょう」調のフィラーは使わない。

## Anti-slop rules（レビューで必ず確認）

- [ ] クリーム背景 + セリフ見出し + テラコッタの組み合わせを使っていない
- [ ] 近黒背景 + 単一の蛍光アクセント（酸緑・朱）にしていない
- [ ] 同一角丸のカードを並べていない。影（rgba(0,0,0,.1)）を撒いていない
- [ ] 見出し上の ALL CAPS アイブロウ、`A · B · C` のメタ文字列、`WORD — fragment` ラベル、`→` 付きボタンを使っていない
- [ ] グラデーション・ガラス風ブラー・絵文字アイコンを使っていない
- [ ] 01 / 02 / 03 の番号は「本当に順序がある」ときだけ
- [ ] 座標が主役になっている（画面で最も大きい数字が座標）
- [ ] 状態が色だけで伝わっていない（アイコン + テキスト併用。LED には状態テキストを併記）
- [ ] タップ領域 44×44pt 以上、Dynamic Type / Reduce Motion 対応
- [ ] 塗りボタンの文字色が `onPrimary`（白固定でコントラスト不足にしていない）

## Platform mapping

- **iOS**: `Color` extension（`P2PColor.paper` など）を `Assets` ではなくコードで定義（xtool のリソース制約を避ける）。`@Environment(\.colorScheme)` で light/dark を切替。SF Symbols のみ。
- **Android**: `MaterialTheme` の `colorScheme` にマップしつつ、`P2PColors`（paper/surface/ink/line/pine/live）を `CompositionLocal` で提供。Material Icons（outlined）のみ。`Roboto Mono` は `FontFamily.Monospace`。
- 両 OS で「同じ画面の骨格」を保ち、OS 標準のコントロール（スイッチ・リスト・シート）はそのまま使う。
