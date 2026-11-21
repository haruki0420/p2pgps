# ネットワーク構成 — LocalDevVPN の仕組みと代替手段（Tailscale / WireGuard / Surge）

iPad 側の位置の書き換えでは、どうしても「VPN」という言葉が出てきます。このページでは、**なぜ VPN が必要なのか**、**LocalDevVPN は何をしているのか**、そして **Tailscale などで同じことを実現する方法**を説明します。

> このページの LocalDevVPN / StosVPN の説明は、公開されている実装（`jkcoxson/LocalDevVPN`、`SideStore/StosVPN`）のソースを読んで整理したものです。Tailscale 方式はコミュニティ実装（`shiqi917/sidestore-vpn-tailscale` など）の情報に基づくもので、**本プロジェクトの iPad アプリとの組み合わせは実機未検証**です。

---

## 1. なぜ VPN が必要なのか

iOS 17 以降の位置シミュレーションは、次の流れで動きます。

1. アプリが **pairing file** を使って、端末自身の **Remote Pairing サービス** に接続する（RSD のポートはトンネル確立時に通知されます）
2. RSD 経由で `com.apple.dt.simulatelocation` サービスを開く
3. 受信した座標をそのサービスに設定する

ここで問題になるのが 1 の「端末自身に接続する」部分です。

- Remote Pairing サービスや lockdownd（ポート 62078）は **127.0.0.1（ループバック）では待ち受けていません**。アプリが `127.0.0.1` の固定ポートに接続しても届きません。
- Remote Pairing サービスのポートは固定とは限らず、**Bonjour（`_remotepairing._tcp`）で検出**する必要があります（検出できない場合は 49152 にフォールバック）。Bonjour を使うため、アプリには **ローカルネットワークの許可** が必要です。
- これらのサービスは **Wi-Fi に接続している間だけ**開放されます（セルラーのみでは閉じています。コミュニティで検証済み）。
- そこで「端末自身の中に、自分自身へ到達するための仮想的な IP アドレス」を作る必要があります。これが LocalDevVPN などの役割です。

---

## 2. LocalDevVPN の仕組み

LocalDevVPN は、iOS の **NetworkExtension（Packet Tunnel Provider）** を使って「端末内でパケットを反射するだけの VPN」を作ります。

### 2.1 設定されるネットワーク

LocalDevVPN の既定値（ソースの `TunnelConstants`）:

| 項目 | 値 | 意味 |
| :--- | :--- | :--- |
| インターフェース IP | `10.7.1.1/32` | VPN インターフェース（utun）に付くアドレス |
| ピア（反射）IP | `10.7.0.1/32` | アプリが接続しに行く「仮想の相手」 |
| デフォルトルート | 除外 | インターネット通信は VPN を通さない |

`NEPacketTunnelProvider` は次のように設定します（要旨）。

```swift
let ipv4 = NEIPv4Settings(addresses: ["10.7.1.1"], subnetMasks: ["255.255.255.255"])
ipv4.includedRoutes = [NEIPv4Route(destinationAddress: "10.7.0.1", subnetMask: "255.255.255.255")]
ipv4.excludedRoutes = [.default()]   // インターネットは VPN に流さない
let settings = NEPacketTunnelNetworkSettings(tunnelRemoteAddress: "10.7.0.1")
settings.ipv4Settings = ipv4
setTunnelNetworkSettings(settings) { ... }
```

ポイントは **`10.7.0.1/32` 宛のパケットだけ**を VPN（utun）に流し、それ以外は通常のネットワークに流すことです。

### 2.2 パケットの反射

VPN に入ってきたパケットを、LocalDevVPN は **送信元と宛先の IPv4 アドレスを入れ替えて、そのまま書き戻します**。

```swift
packetFlow.readPackets { packets, protocols in
    var modified = packets
    for i in modified.indices where protocols[i].int32Value == AF_INET {
        modified[i].withUnsafeMutableBytes { bytes in
            let ptr = bytes.baseAddress!.assumingMemoryBound(to: UInt32.self)
            let src = ptr[3], dst = ptr[4]
            ptr[3] = dst   // 送信元 ← 宛先
            ptr[4] = src   // 宛先   ← 送信元
        }
    }
    packetFlow.writePackets(modified, withProtocols: protocols)
    // 以下繰り返し
}
```

これにより、次のことが起きます。

```
アプリ ──(宛先 10.7.0.1:<Remote Pairing ポート>)──▶ utun ──▶ PacketTunnelProvider
                                              │ src/dst を入れ替え
                                              ▼
                                    端末自身の IP:<Remote Pairing ポート>
                                              │
アプリ ◀──(送信元 10.7.0.1:<Remote Pairing ポート>)── utun ◀──┘（戻りも同様に反射）
```

つまり **「10.7.0.1 は端末自身の別名」** になり、アプリは `10.7.0.1` の Remote Pairing サービスに接続するだけで、自分自身の RSD に到達できます。通信は端末の外には一切出ません。

### 2.3 制約

- **Wi-Fi に接続している必要があります**（RSD / lockdownd が Wi-Fi 関連時のみ開放されるため）。
- **iOS で同時に使える VPN は 1 つだけ**です。LocalDevVPN を有効にすると、他の VPN（社内 VPN・DNS ブロッカー・Tailscale など）は切断されます。
- 実装には **NetworkExtension の entitlement**（`com.apple.developer.networking.networkextension` の `packet-tunnel-provider`）が必要です。App Store 配布の LocalDevVPN はこれを持っていますが、**サイドロードした自作アプリに組み込む場合は、署名プロファイルにこの entitlement が含まれている必要があります**（無料の Apple ID では難しい場合があります）。

---

## 3. Tailscale で実装する方法

Tailscale も iOS では **Packet Tunnel Provider** として動き、端末に `100.x.y.z/32` の utun アドレスを割り当てます。これを利用して、LocalDevVPN の代わりに「反射役」を tailnet 上に置く方法があります。

### 3.1 なぜ「反射役」が必要か

Tailscale の utun はポイントツーポイントで、端末の Tailscale IP は端末自身に付きます。しかし SideStore の新しい minimuxer などは **「utun の IP + 1」** を接続先として使うため、そのアドレスに応答する相手が必要です。そこで **tailnet 上の Linux ノード**に「パケットを送り返すだけのプログラム（リフレクター）」を置きます。

```
iPad ──(宛先 NODE_ADDR:<Remote Pairing ポート>)──▶ Tailscale（暗号化）──▶ リフレクターノード
                                                          │ TUN で受信
                                                          │ src/dst を入れ替え
                                                          ▼
iPad ◀──────────────── Tailscale ◀──────────────── 端末自身へ戻す
                                                          │
                                              端末の Remote Pairing サービスに配信
```

リフレクターの中身は非常に単純で、TUN デバイスを作り、特定アドレス宛の IPv4 パケットの送信元・宛先を入れ替えて書き戻すだけです（Rust で約 60 行）。

### 3.2 既存の実装を使う（おすすめ）

`shiqi917/sidestore-vpn-tailscale` は、まさにこの構成を Docker で提供しています。

1. **tailnet に Linux ノードを用意**（NAS、VPS、ラズパイなど。Docker が動けば OK）
2. `.env` に `TS_AUTHKEY` を設定して起動

   ```bash
   cp .env.example .env      # TS_AUTHKEY を記入
   docker compose up -d --build
   docker logs sidestore-vpn | grep "node address"   # NODE_ADDR を控える
   ```

3. **iPad 側**: Tailscale をインストールして常時接続（Wi-Fi に接続していること）
4. **本アプリ**: Settings → **接続先** を `NODE_ADDR`（リフレクターノードの Tailscale IP）に変更
5. 接続テスト: 本アプリの「困ったとき」画面、または SideStore の Health Check で到達性を確認

> この構成のポイント:
> - Tailscale の CGNAT 範囲（`100.64.0.0/10`）は subnet route として配布できないため、リフレクターノード自身の Tailscale IP を反射アドレスにし、DNAT で TUN に流します。
> - Tailscale の `--snat-subnet-routes=false` が必要です（SNAT が送信元を書き換えると反射が壊れるため）。
> - ルーターで UDP 41642 を開放すると DERP リレーを避けて直接接続できます（`tailscale ping <NODE_ADDR>` で確認）。

### 3.3 自前でリフレクターを書く場合

最小構成は次のとおりです。

1. Linux ノードに TUN デバイスを作る（例: `10.7.0.0/24`、destination を反射アドレスに）
2. TUN から読み込んだ IPv4 パケットのうち、宛先が反射アドレスのものだけ **src/dst を入れ替えて書き戻す**
3. Tailscale 側で、反射アドレス宛のパケットがこの TUN に入るように DNAT / ルーティングを設定
4. iPad の Tailscale から反射アドレスに到達できることを確認

（実装例: `shiqi917/sidestore-vpn-tailscale` の `src/main.rs`、元実装 `xddxdd/sidestore-vpn`）

### 3.4 セキュリティ上の注意

- RSD への経路が tailnet 経由になります。**Tailscale ACL で「iPad」と「リフレクターノード」だけに通信を制限**してください。
- リフレクターは「送られてきたパケットを送信元に返す」だけですが、ノード自体の SSH 等の防御は通常どおり必要です。
- pairing file は引き続き秘密情報です。Tailscale 経由でも、pairing file を他者に渡さないでください。

### 3.5 制約

- Tailscale も VPN なので、**LocalDevVPN とは同時に使えません**（切り替えが必要）。
- **Wi-Fi 接続は必須**です（RSD / lockdownd の仕様）。
- リフレクターノードの**常時稼働**が必要です。
- DERP リレー経由になるとレイテンシが増えます（接続確立には影響しにくいですが、体感は変わります）。
- **本アプリ + Tailscale リフレクターの組み合わせは実機未検証**です。接続先を変えるだけで動く設計ですが、実機で確認してください。

---

## 4. その他の代替手段

| 方式 | 必要なもの | 通信経路 | 向いている場面 |
| :--- | :--- | :--- | :--- |
| **LocalDevVPN** | App Store アプリ | 端末内で反射 | もっとも簡単。通常はこれで OK |
| **StosVPN** | サイドロード（SideStore 公式） | 端末内で反射 | LocalDevVPN が使えない環境。オープンソース |
| **Tailscale + リフレクター** | tailnet + Linux ノード | tailnet（暗号化） | Tailscale を常時使いたい / VPN 切り替えを避けたい |
| **WireGuard + 反射サーバー** | 公衆 IP のサーバー | インターネット | LocalDevVPN が使えない地域向け（`lj2000lj/SideStore-WireGuard`） |
| **Surge / Clash などの TUN アプリ** | 有料アプリ | 端末内で反射 | 既に導入している場合（Surge の `IP Rewrite = reflect`） |
| **LAN 内の反射役** | LAN 上のサーバー | LAN | VPN を一切使いたくない場合（ネットワーク構成が必要） |

- **StosVPN**: `SideStore/StosVPN`。LocalDevVPN と同じ Packet Tunnel Provider 方式で、オフラインでも動くのが特徴です。
- **WireGuard**: `10.7.0.1/32` 宛の通信だけを WireGuard サーバーに流し、サーバー側で反射させます。公衆 IP のサーバーが必要で、LocalDevVPN / StosVPN が使えない環境のための回避策です。
- **Surge / Clash**: TUN の `included-routes` に `10.7.0.1/32` を追加し、`IP Rewrite` で `10.7.0.1 = reflect` とします（Surge の reflect 機能）。有料アプリですが、VPN の切り替えを避けられます。

---

## 5. 本アプリでの設定

本アプリは **接続先を設定で変更できます**（既定 `10.7.0.1`）。LocalDevVPN 以外の方式を使う場合は、この値を環境に合わせて変更してください。

1. iPad の Settings → **接続先** を設定
   - LocalDevVPN / StosVPN: `10.7.0.1`（既定）
   - Tailscale + リフレクター: リフレクターノードの Tailscale IP（`NODE_ADDR`）
   - WireGuard / LAN 反射: 反射役の IP
2. VPN（または Tailscale）を接続
3. **Wi-Fi に接続**していることを確認
4. 本アプリで pairing file をインポート → DDI をダウンロード → 受信側を開始
5. 接続に失敗する場合は [Troubleshooting](Troubleshooting) を参照

> 接続先ポートは固定ではなく、アプリが **Bonjour（`_remotepairing._tcp`）で検出**します（検出できない場合は 49152 にフォールバック）。反射役は TCP/UDP のポートを問わずアドレスを入れ替えるだけなので、ポートの設定変更は不要です。

### 5.1 pairing file の入手（iOS 27 以降）

iOS 27 では iloader がエクスポートする pairing file が RSD ハンドシェイクで拒否されることがあります。実機（iOS 27.2 / Windows）では **iloader では解消せず、`idevice_pair--windows-x86_64`（Windows x86_64 版）で RPPairing を作り直すと成功**しました。詳細は [p2pgps-ios の Setup iPad](https://github.com/haruki0420/p2pgps-ios/blob/main/wiki/Setup-iPad.md) を参照してください。

### 5.2 高頻度更新

送信間隔は iOS で 100 ms、Android で 200 ms まで選択できます（既定は 1000 ms）。Android は位置取得も選択した間隔に合わせて要求します（電池消費は増えます）。iOS の CoreLocation は更新頻度を保証しないため、実測は設定より遅くなることがあります。

---

## 6. 参考リンク

- [jkcoxson/LocalDevVPN](https://github.com/jkcoxson/LocalDevVPN) — LocalDevVPN の実装（Packet Tunnel Provider）
- [SideStore/StosVPN](https://github.com/SideStore/StosVPN) — StosVPN の実装
- [shiqi917/sidestore-vpn-tailscale](https://github.com/shiqi917/sidestore-vpn-tailscale) — Tailscale リフレクター（Docker）
- [xddxdd/sidestore-vpn](https://github.com/xddxdd/sidestore-vpn) — 元になったリフレクター実装
- [lj2000lj/SideStore-WireGuard](https://github.com/lj2000lj/SideStore-WireGuard) — WireGuard 方式
- [derbalkon/surge-localdevvpn](https://github.com/derbalkon/surge-localdevvpn) — Surge の reflect モジュール
- [StikDebug-Guide / pairing_file.md](https://github.com/StikDebug/StikDebug-Guide/blob/main/pairing_file.md) — pairing file の取得方法

---

## 関連ページ

- [Setup iPad](Setup-iPad) — Developer Mode / LocalDevVPN / pairing file / DDI の手順
- [Glossary（用語集）](Glossary) — RSD / DDI / pairing file などの用語
- [Troubleshooting](Troubleshooting) — 接続できないときの対処
- [FAQ](FAQ) — よくある質問
