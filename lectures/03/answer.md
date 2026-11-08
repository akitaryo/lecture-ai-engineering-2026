# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
素のLLMは3レベルを宿題全体の難易度として解釈したのに対し、今回のLLMは用語集にある基礎・実装・発展の3つのキーワードを根拠に宿題の構成としてのレベル3という正確な解答を出力した。

- `--trace` で見えたツール呼び出し（ツール名と引数）：
ツール名 : search_glossary()
引数 : {'query': 'LoRA'}

- 1つの質問での LLM 呼び出し回数（`requests`）：
requests=2

- 追加したツールと、docstring に書いた説明：

追加したツール : make_quiz(lecture: int) -> str:
docstringに書いた説明 : 
"""指定した回の用語から1つを選び、
    確認問題と答えを返す。

    「第2回の確認問題を出して」のように、
    復習用の問題を求められたときに使う。
    """

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
基礎・実装・発展すべて行った。

- やったこと：
【基礎】
app/agent.py の INSTRUCTIONS や、app/tools.py のツールの docstring を、以下の5通りで書き換えた。質問は どの場合も"LoRAとQLoRAの違いは？"共通で、
--trace 付きで実行し、ツールの呼ばれ方や回答がどう変わるかを比べて記録した。
例① : 変更なし
例②：INSTRUCTIONS から「必ず search_glossary で用語集を確認する」の行を消し、検索せずに答えるようになるかを検証した。
例③：docstring の「用語を1つだけ入れる」を「まとめて入れる」に変え、検索の回数がどう変わるかを検証した。
例④ : 「宿題の答えそのものを書く」ようINSTRUCTIONSで指定し、回答の出力形式を検証した。
例⑤ : 講座（AIE2026）に固有の言葉について答える前の使用を指定せず、回答のボキャブラリーや表現に変化があるか検証した。
※なおmodelはすべてgemini-3.5-flash-liteで行った。

【実装】
学習の記録を learning_log/ に保存するsave_learning_log()をtools.pyに実装した。
呼び出す前に利用者の確認を得るために、agent.pyにpydantic_aiを用いてoutput_typeが指定できるようagentの定義を改良し、requires_approval=Trueの形で利用者が確認する過程を導入できるようにした。

【発展】
adk_agent/glossary_agent/ フォルダを新たに作成し、 INSTRUCTIONとtoolsをagentに設定するagent.pyと agentをimportする__init__.pyを作成した。
そのうえで、adk上で今までと同様、"LoRAとQLoRAの違いは？"の質問を入力した。

- 結果：
【基礎】
5例の出力結果は下記の通り。
例①　変更なし
<出力結果>
LoRAとQLoRAの主な違いは、**ベースモデルの重みの保持方法（量子化の有無）**にあります。

* **LoRA**: 事前学習済みの重みをそのまま（通常は16ビットなどの高精度で）固定し、追加の小さな低ランク行列（アダプタ）のみを学習してパラメータ数やメモリを削減するPEFT手法です。
* **QLoRA**: ベースモデルの重みをさらに4ビットなどに**量子化**してメモリ消費を大幅に抑えた状態で固定し、その上でLoRAによる学習を行う手法です。これにより、より小さなGPUでも大型モデルのファインチューニングが可能になります。

第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0009057'), details={'text_prompt_tokens': 1494}, input_text_tokens=1494, input_tokens=1494, output_tokens=183, requests=2, tool_calls=2)


例①：INSTRUCTIONS から「必ず search_glossary で用語集を確認する」の行を消すと、検索せずに答えるようになるか
<出力結果>
LoRAとQLoRAの違いは以下の通りです。

* **LoRA**: 事前学習済みの重みは固定したまま、重みの更新分を小さな低ランク行列（2つの行列の積）で表し、その部分だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習パラメータや保存ファイルを減らすことができます。
* **QLoRA**: ベースモデルの重みを4ビットなどに量子化（Quantization）してメモリを大きく節約したうえで、LoRAによるファインチューニングを行う手法です。これにより、より大きなモデルを小さなGPUでも扱えるようになります。

関係する回：第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008838'), details={'text_prompt_tokens': 1446}, input_text_tokens=1446, input_tokens=1446, output_tokens=180, requests=2, tool_calls=2)



例③：docstring の「用語を1つだけ入れる」を「まとめて入れる」に変えると、検索の回数がどう変わるか
<出力結果>
**LoRA**と**QLoRA**の主な違いは、ベースモデルの重みをそのままの精度（16ビットなど）で使うか、量子化して削減するかという点です。

* **LoRA（Low-Rank Adaptation）**
  * 事前学習済みの重みを固定したまま、小さな低ランク行列（アダプタ）だけを追加・学習するPEFT（Parameter-Efficient Fine-Tuning）の手法です。
  * 学習パラメータ数が大幅に削減され、効率的にファインチューニングを行えます。

* **QLoRA（Quantized LoRA）**
  * ベースモデルの重みを **4ビットなどに量子化（Quantization）** してメモリ使用量をさらに極限まで抑えた状態で、LoRAによる学習を行う手法です。
  * これにより、通常のLoRAよりも大きなモデルを、より小さなGPU環境で動かせるようになります。

---
関連する回：第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[usage] RunUsage(cost=Decimal('0.0009199'), details={'text_prompt_tokens': 1183}, input_text_tokens=1183, input_tokens=1183, output_tokens=226, requests=2, tool_calls=1)


例④ : 宿題の答えそのものは書く、と指定した場合には？
<出力結果>
講座の用語集によると、LoRAとQLoRAの違いは以下のとおりです。

* **LoRA**
  事前学習済みの重みを固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習するパラメータが少なく、学習結果も小さなファイルで保存できます。

* **QLoRA**
  ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAによる学習を行う手法です。これにより、より大きなモデルを小さなGPUで扱えるようになります。

関係する回：第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0009037'), details={'text_prompt_tokens': 1454}, input_text_tokens=1454, input_tokens=1454, output_tokens=187, requests=2, tool_calls=2)


例⑤ : この講座（AIE2026）に固有の言葉について答える前に使うのを指定しなかった場合には？
<出力結果>
LoRAとQLoRAの違いは、ベースモデルの重みをそのまま使うか、量子化してメモリを節約するかにあります。

* **LoRA**: 事前学習済みの重みは固定したまま、重みの更新分を小さな低ランク行列で表し、その部分だけを学習する手法です。
* **QLoRA**: ベースモデルの重みを4ビットなどに量子化（低精度化）してメモリをさらに節約した上で、LoRAと同様に低ランク行列を学習する手法です。これにより、より大きなモデルを小さなGPU環境でも扱えるようになります。

関係する回：第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008627'), details={'text_prompt_tokens': 1434}, input_text_tokens=1434, input_tokens=1434, output_tokens=173, requests=2, tool_calls=2)

【発展】
<出力結果>
[user]: "LoRAとQLoRAの違いは？"
[glossary_agent]: LoRAとQLoRAの違いは以下のとおりです。

* **LoRA（Low-Rank Adaptation）**
  事前学習済みの重みは固定したまま、重みの更新分を小さな低ランク行列で表し、その部分だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習するパラメータやメモリを大幅に削減できます。
* **QLoRA**
  ベースモデルの重みを4ビットなどに量子化してメモリをさらに節約したうえで、LoRAによるファインチューニングを行う手法です。これにより、より大きなモデルを小さなGPU環境でも扱えるようになります。

関係する回：第2回


- 気づき・疑問：
【基礎】
・例①と例③を比較すると、docstringでまとめて入れるに変更することで、requests=2に対して、tool_calls (検索の回数)が1回に、Iuput Tokenは1446→1183と減少し、Output tokenの数が183→226に増加していた。③以外の例のInput tokenが1400-1500、output tokenの数が170-190であったことを踏まえる有意な変化であったが、これは用語集の文章をまとまってcallしたことで、1つのreturnでより多くの情報が含有することになったと考えられる。
・例④では参照する用語集をそのまま回答で使用するよう指示したため、出力内容は用語集の表現のままであったが、token数に明確な変化は見られなかった。例⑤の講座固有の用語の使用を支持しなかった場合にも、token数に明確な変化はなかった。細かな表現の変化をとらえるパラメータがあるのか疑問に思った。

【発展】
・agentに対するINSTRUCTIONの入力に関しては、ADKでもAgentの設定時点で引数に渡す必要があるのに対し、toolの設定やモデルの設定もagent作成時に必要な点が相違点であった。(Pydantic AIではtoolの設定はagent作成後にtool_plain()で登録し、モデルはコマンド実行時に指定できる)


