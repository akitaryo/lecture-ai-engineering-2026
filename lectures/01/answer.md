# 第1回 解答

## 演習

- 講座に固有の質問（宿題の3レベル）へのモデルの回答（要約でよい）：

AIE2026（AIエンジニア育成講座など）の宿題における「3レベル」という言葉は、通常、**受講者のスキルや進度、あるいは課題の難易度に合わせて用意された3段階の課題（レベル1〜3）**を指します。

*   **レベル1（基礎・入門）:**
    *   **内容:** チュートリアル通りにコードを動かす、穴埋め問題、基本的な用語の理解など。
    *   **対象:** 初学者や、まず基本の操作をマスターしたい人。
*   **レベル2（応用・実践）:**
    *   **内容:** 自力でコードを書く、少し条件を変えてみる、簡単なバグを取るなど。
    *   **対象:** 基本的な概念を理解し、自分で手を動かして実装してみたい人。
*   **レベル3（発展・応用挑戦）:**
    *   **内容:** オープンな課題解決、より高度なアルゴリズムの実装、独自の工夫を加えるなど。
    *   **対象:** すでに知識がある人や、より高いレベルを目指したい挑戦的な人。


- 用語集の正しい意味と比べて気づいたこと：
正しい"レベル3"の定義は"内容確認"、"実装"、"調査・考察"、と演習のパイプラインの上流から下流を指しているものであるが、素のLLMは"基礎"、"応用"、"発展"と演習全体の難易度でクラス分けしている、という点で異なっている。

- 表示できたトークン数（入力 / 出力）：
入力トークン数: 22, 出力トークン数: 439

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展 : 
基礎、実装、発展

- やったこと：
以下の質問に関して、モデル・Temperatureを変えた3条件下で回答を得た。
また、その際の入出力トークン数、応答時間を出力し比較した。

質問 : "LoRAとは何ですか？"
条件A : AIE_MODEL=gemini-3.5-flash-lite, tempareture = 1.0
条件B : AIE_MODEL=gemini-3.5-flash-lite, tempareture = 2.0
条件C : AIE_MODEL=gemini-3.8-flash, tempareture = 2.0

比較に際して、以下の①から④の機能をコードに実装した。

①ask.pyにTemperatureの入出力を可能にする下記のコードの実装

def parse_temperature(value: str) -> float:
    try:
        temperature = float(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError("temperature は数値で指定してください") from e
    if not 0.0 <= temperature <= 2.0:
        raise argparse.ArgumentTypeError("temperature は 0.0〜2.0 の範囲で指定してください")
    return temperature

②ask.pyのask()関数内に、応答時間を計測し出力する下記のコードの実装

started_at = time.perf_counter()
response_time_ms = (time.perf_counter() - started_at) * 1000
if response.usage_metadata:
    print(f"[response time] {response_time_ms:.0f} ms")

③ask.pyに入出力トークン数の出力を可能にする下記のコードの実装

if response.usage_metadata:
    print(
        f"[usage] 入力トークン数: {response.usage_metadata.prompt_token_count}, "
        f"出力トークン数: {response.usage_metadata.candidates_token_count}"

④ask.py に会話履歴を保ったまま続けて質問できるようにする下記のコードを実装

conversation_history: list[tuple[str, str]] = []

また、ask()関数内には下記のコードを実装

conversation_history.append((question, response.text))


- 結果：

〇トークン数と応答時間
・条件A
[model] gemini-3.5-flash-lite
[temperature] 1.0
[質問] LoRAとは何ですか？
[usage] 入力トークン数: 7, 出力トークン数: 682
[response time] 5977 ms
・条件B
[model] gemini-3.5-flash-lite
[temperature] 2.0
[質問] LoRAとは何ですか？
[usage] 入力トークン数: 7, 出力トークン数: 609
[response time] 3403 ms
・条件C
[model] gemini-3.8-flash
[temperature] 2.0
[質問] LoRAとは何ですか？
[usage] 入力トークン数: 7, 出力トークン数: 782
[response time] 157831 ms

- 気づき・疑問：

〇3条件の解答の違い
・モデルの違いの影響
3-8-flashでは、LoRAの低ランク適用の具体的な手法(数学的に、「巨大な行列の変更データ」を「2つの小さな行列のかけ算」に分解（低ランク近似）)や、LoRAの活用例の列挙数 (Stable diffusionとLLMで3-4つずつ)に関して、より高粒度の解答が出力された。また出力トークン数、応答時間を見ても増加傾向にあったが、モデルの性能が高く学習に要する時間が増大することをふまえると、直感的理解と一致する。
・Temparetureの違いの影響
数値が大きいほど、情報科学の分野では馴染みのない (やや冗長な) 比喩や表現が散見される傾向にあるように思われる。(低ランク近似を"辞書に貼る付箋"と例える、LoRAによるモデル修正を"自由に着せ替え"と例えるなど)。出力トークン数、応答時間を見ると低下傾向にあったが、トークン選択時のランダムさが増加することを踏まえると直感的には違和感のある結果だった。



