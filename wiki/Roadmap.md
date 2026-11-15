# Roadmap

## v1（現在）

- [x] BLE GATT プロトコル v1 仕様の確定
- [x] iOS: Sender（iPhone）/ Receiver（iPad）+ StikDebug 由来の位置注入
- [x] Android: BLE ペリフェラル Sender + 前景サービス
- [x] Python リファレンス実装 + テストベクタ
- [x] CI（GitHub Actions）
- [x] 実機での動作検証（BLE 購読・位置注入は Android 実機 + iPad で確認済み）
- [x] Wiki の初回ページ作成

## v1.1

- [ ] 送信側の軌跡記録・再生（ルートシミュレーション）
- [ ] 受信側の移動平均・外れ値除去のチューニング UI
- [ ] Android のシミュレート位置モード（開発用）
- [ ] 接続履歴・自動再接続の安定化

## v2（検討中）

- [ ] アプリ層の認証（HMAC / ペアリングコード）— Control に `AUTH` opcode を予約済み
- [ ] 複数送信側の同時接続（iPad が複数地点を切り替え）
- [ ] 位置の補間（1 Hz 未満の受信でも滑らかに）
- [ ] iOS の位置注入を URL スキーム委譲ではなく完全内蔵に（内蔵エンジン。失敗時は URL スキームにフォールバック）
- [ ] Apple Watch / Android Wear からの送信

## 非目標

- クラウド経由の位置共有
- 追跡・監視用途（プライバシー配慮のため、明示的な UI とバナーを必須にしています）
