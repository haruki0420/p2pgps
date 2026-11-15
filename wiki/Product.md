# Product

<!-- impeccable:product-schema 1 -->

## Platform

adaptive

（iPadOS / iOS は SwiftUI、Android は Jetpack Compose。iPad は Receiver 専用、iPhone / Android は Sender。）

## Stack

- iOS/iPadOS: Swift 6 + SwiftUI + CoreBluetooth + CoreLocation + MapKit。SwiftPM + [xtool](https://github.com/xtool-org/xtool)（Mac なしビルド）。位置注入は TLocation 由来の idevice FFI。
- Android: Kotlin + Jetpack Compose + `BluetoothLeAdvertiser` / `BluetoothGattServer` + `LocationManager`。Gradle。
- Protocol: Python リファレンス実装 + テストベクタ（仕様の正本）。
- CI: GitHub Actions（macOS / Ubuntu / Windows）。

## Users

- **本人（第一利用者）**: Mac を持たず、iPad の位置を iPhone / Android から合わせたい技術志向のユーザー。位置情報ゲーム・位置依存アプリの検証・デモが目的。Developer Mode / サイドロード / VPN の用語に抵抗が少ない。
- **アプリ開発者・QA**: 任意の座標を iPad に流し込み、位置依存機能を再現テストしたい人。
- **位置情報ゲームのプレイヤー（将来）**: iPad 上で、スマホの実位置をそのまま使いたい人。

## Product Purpose

iPhone / Android が取得した GPS 位置を BLE GATT で iPad に転送し、iPad 上で「その位置にいる」ように位置情報を反映する。クラウドを介さない P2P。成功とは「送信側で開始し、受信側で 1 回接続し、注入を ON にすれば、以降は放置で位置が追従している」こと。

## Positioning

- 近距離・1 対 1・アカウント不要・クラウドなし。座標は端末外に出さない。
- Mac 不要（xtool + SideStore 等でのサイドロード）。PC を介さず iPad 単体で完結。
- 位置注入は StikDebug 由来のオンデバイス方式を内蔵し、既定 OFF・明示操作・常時バナー。

## Operating Context

- Sender: 屋外・移動中。画面 OFF / バックグラウンドが多い。バッテリー制約あり。
- Receiver: 屋内でセットアップし、その後は画面を点けたまま/消灯して放置。注入中は「どの送信元の、いつ受信した、どの座標か」を常時確認したい。
- 失敗の主因は BLE ではなくセットアップ（LocalDevVPN・pairing file・DDI・Developer Mode）。
- 日本語 UI。技術用語（BLE / DDI / pairing file）はそのまま提示し、短い説明を添える。

## Capabilities and Constraints

- できること: ロール選択、Sender の位置送信、Receiver の受信・地図表示・軌跡、位置注入 ON/OFF、pairing file インポート、DDI ダウンロード/マウント、LocalDevVPN 案内、ターゲット IP 設定、自動再接続、診断（hex / FFI ログ）。
- 制約: 実機・シミュレータ・Xcode が開発環境に無い（CI でコンパイル検証のみ）。位置注入は Apple 非公開 API 相当で、TLocation と同一 FFI に固定。壊れた場合は `tlocation://` URL スキームへ委譲するフォールバック。
- v1 は同時 1 台接続。ボンディングなし。近距離の第三者が偽位置を送れるため、自動接続は許可した送信元のみ、注入は既定 OFF、注入中は常時バナー表示。
- ライセンス: iOS は AGPL-3.0（StikDebug / TLocation 派生）、Android / Protocol は MIT。

## Brand Commitments

- 名称: **P2P GPS**（`p2pgps`）。日本語 UI。
- ネイティブ作法を守る（HIG / Material 3）。web 風 UI はしない。
- 派手さより「状態が一目で分かること」。ただし、システム既定のままの無個性な画面にはしない（下記 DESIGN.md の視覚世界に従う）。

## Evidence on Hand

- 仕様: `https://github.com/haruki0420/p2pgps-protocol/blob/main/spec/protocol-v1.md`（v1 凍結）, `wiki/Architecture.md`
- 参照実装: TLocation（AGPL-3.0, 上流コミット固定）
- 既存の xtool プロジェクト（構成・CI 慣例）
- 実機スクリーンショット・利用ログ: **無し**（設計は推定）

## Product Principles

1. **セットアップの詰まりを可視化する。** 何が足りないかを画面が名指しし、1 タップで回復手順へ。
2. **注入は常にユーザーの明示操作。** 既定 OFF、状態は常時表示。
3. **送信側は「置いておけば動く」。受信側は「状態が読める」。**
4. **計器のように正確に読める。** 座標・精度・最終受信時刻は一目で比較できる。
5. **ローカル完結。** 座標をクラウドに出さない。ログも既定で丸める。

## Accessibility & Inclusion

- Dynamic Type / システムフォントスケール、44×44pt のタップ領域、VoiceOver ラベル、Reduce Motion 尊重。
- 色だけで状態を伝えない（アイコン + テキスト + 形の併用）。
- 座標は VoiceOver で「北緯 35.681236、東経 139.767125」と読む。
- 日本語を既定とし、英語併記はしない（v1）。
