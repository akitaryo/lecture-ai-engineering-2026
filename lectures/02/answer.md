# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：
{
  "base_model": "Qwen/Qwen3.5-0.8B",
  "revision": "2fc06364715b967f1860aea9cf38778875588b17",
  "seed": 42,
  "num_train_epochs": 20,
  "warmup_steps": 6,
  "lr": 0.0002,
  "lora_r": 16,
  "lora_alpha": 32,
  "max_seq_len": 512,
  "max_new_tokens": 96,
  "gen": {
    "do_sample": false
  },
  "work_dir": "/content/qlora_lab",
  "drive_dir": "/content/drive/MyDrive/aie2026/qlora_lab"
}
- 自分で学習を実行したか（`executed_training_myself`）：はい
- 学習前：`format_rate` =　 0.095238 / `content_rate` = 0.000000　
- 学習後：`format_rate` =　 1.000000 / `content_rate` = 0.904762
- 退行した質問：[]
- 学習後に残った失敗と、その型（根拠なしの質問に断定した / 根拠ありの質問に確認要求で逃げた / 形式の崩れ）：
根拠なしの質問2つに断定した。1つは成績の開示と提出期限の誤認識、もう一方はオフィスアワーの事前予約の有無を、時間帯と誤認識。
- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：
 "knowledge": [
    {
      "質問": "この講座の最終課題の締切はいつですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"9 月 30 日 23:59\"}",
      "学習後の分類": "asserted",
      "学習後の出力": "{\"answer\": \"課題の提出期限は 9 月 30 日 23:59（日本時間）です。\", \"needs_review\": false}"
    },
    {
      "質問": "担当教員の名前は何ですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"確認が必要\"}",
      "学習後の分類": "needs_review",
      "学習後の出力": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}"
    },
    {
      "質問": "次回の講義のテーマは何ですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"次回の講義のテーマは「学習ポータル」の「課題」欄で提出する PDF 1 ファイルを提出します。\"}",
      "学習後の分類": "needs_review",
      "学習後の出力": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}"
    },
    {
      "質問": "課題の提出期限はいつですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"9 月 30 日 23:59\"}",
      "学習後の分類": "asserted",
      "学習後の出力": "{\"answer\": \"課題の提出期限は 9 月 30 日 23:59（日本時間）です。\", \"needs_review\": false}"
    }
  ],

"最終"という2語が課題の前につくことで、指示する内容が大きく異なるが、ファインチューニングではその文脈の変化を感知出来ていないのがわかる。

- 学習で変わったこと・変わらなかったこと：
変わったのは、特定の形式の質問の学習することで、正しい判断ができる質問の種類が増え content_rateやformat_rateが向上した点。
変わらなかったのは、知識を問う質問への対応は完全にできない点。局所的なパラメータの更新では、形式を変えた場合には対応できない。


## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
基礎、実装、発展すべて行った。
- 変えた設定やデータ：
【基礎】
"lora_r": 16→8, # LoRA の行列の次元を小さくし、学習するパラメータを減らした
【実装】  
既存データを以下のように置き換え、train,valid,test,goldを設定した。
FAQ = {
    "Teaching_assitants" : "ティーチングアシスタントは山田　太郎 (yamada_t@gg.com)です。",
    "AI permission" : "ChatGPTなど生成AIの使用は可能ですが、必ず使用した箇所とプロンプトをレポートに明記してください。",
    "materials" : "出題範囲は講義資料の第10章のP250からP294です。",
    "enviroment" : "Pythonの推奨環境はVer.4.1.1です。",
    "font" : "レポートのフォントはTimes New Romanの12ptです。",
}
# 根拠あり: (FAQ キー, 質問テンプレート群, 正解の answer に含まれるべき語)
GROUNDED = {
    "Teaching_assitants": (["質問は誰に聞けばいいですか", "TAはいますか", "メールで質問する場合の宛先は誰ですか", "先生以外に質問することは可能ですか"], ["TA", "山田　太郎","yamada_t@gg.com"]),
    "AI permission": (["AIは使っていいですか","ChatGPTは使用可ですか","生成AIの取り扱いを教えてください","AIを使った場合のレポートにどう書けばいいですか"], ["使用可", "使用した箇所","プロンプト","明記"]),
    "materials": (["資料はレポートの助けになりますか","出題範囲を教えてください","講義資料は課題に関係ありますか","課題の参考になる講義の範囲はどこですか"], ["出題範囲", "講義資料","第10章","P250からP294"]),
    "enviroment": (["環境の指定はありますか","Pythonの環境のアップデートはどこまで必要ですか", "古いVerでも可能でしょうか","想定しているPythonの環境を教えてください"], ["Python", "推奨","環境","Ver.4.1.1"]),
    "font": (["フォントは何でもいいですか","字体に制限はありますか","文字のデザインは何が推奨されてますか","文字の大きさに指定があれば教えてください"], ["フォント", "Times New Roman","12pt"]),
}
# 根拠なし: FAQ に無いので needs_review=true が正解
UNGROUNDED = [
    "課題の配点はどうなっていますか", "講義の録画は公開されますか",
    "参考文献はありますか", "合格点はありますか","レポートは5段階評価ですか","英語でレポートを書いてもよいですか","レポートに図は使用してよいですか"
]

# test 専用の追加質問（train / valid には入れない）
TEST_EXTRA_GROUNDED = {
    "Teaching_assitants" : ["ティーチングアシスタントを教えてください","学生への指定は大丈夫ですか"],
    "AI permission" : ["生成AI使ったら減点されますか","GeminiやCopilotの使用可否を知りたいです"],
    "materials" : ["講義内容はレポートに役立ちますか","配布された資料の何ページがレポートに使えますか"],
    "enviroment" : ["Pythonがうまく動く環境はいくつですか","Pythonで事前にアップデートが必要なことはありますか"],
    "font" : ["文字の大きさやデザインは自由ですか","見やすいフォントがあれば教えてください"],
}
TEST_EXTRA_UNGROUNDED = [
    "早めに出せば高評価ですか","講義で習っていない数式は使ってよいですか","レポート作成するアプリケーションはwordが推奨されてますか","採点に重視されるポイントを教えてください","計算の途中経過は必要ですか",
]

【発展】 
 glossary_sft.jsonlのassistant の定義文が同じレコードを同じ用語の質問表現としてまとめ、各定義につき1件目を学習、2件目をテストに用いた。
train=58 test=58 gold=58 definitions=58

- 結果（比較表や数字）：
出力されたresult.jsonを記す
【基礎】
{
  "config": {
    "base_model": "Qwen/Qwen3.5-0.8B",
    "revision": "2fc06364715b967f1860aea9cf38778875588b17",
    "seed": 42,
    "num_train_epochs": 20,
    "warmup_steps": 6,
    "lr": 0.0002,
    "lora_r": 8,
    "lora_alpha": 32,
    "max_seq_len": 512,
    "max_new_tokens": 96,
    "gen": {
      "do_sample": false
    }
  },
  "versions": {
    "transformers": "5.18.0",
    "peft": "0.21.1",
    "trl": "1.14.2",
    "torch": "2.11.0+cu130"
  },
  "method": "LoRA（量子化なし）",
  "before": {
    "label": "before",
    "n": 21,
    "format_rate": 0.09523809523809523,
    "content_rate": 0.0,
    "both_rate": 0.0,
    "seconds": 21.4
  },
  "after": {
    "label": "after",
    "n": 21,
    "format_rate": 1.0,
    "content_rate": 0.9047619047619048,
    "both_rate": 0.9047619047619048,
    "seconds": 63.2
  },
  "regressed": [],
  "knowledge": [
    {
      "質問": "この講座の最終課題の締切はいつですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"9 月 30 日 23:59\"}",
      "学習後の分類": "asserted",
      "学習後の出力": "{\"answer\": \"課題の提出期限は 9 月 30 日 23:59（日本時間）です。\", \"needs_review\": false}"
    },
    {
      "質問": "担当教員の名前は何ですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"確認が必要\"}",
      "学習後の分類": "needs_review",
      "学習後の出力": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}"
    },
    {
      "質問": "次回の講義のテーマは何ですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"次回の講義のテーマは「学習ポータル」の「課題」欄で提出する PDF 1 ファイルを提出します。\"}",
      "学習後の分類": "needs_review",
      "学習後の出力": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}"
    },
    {
      "質問": "課題の提出期限はいつですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"9 月 30 日 23:59\"}",
      "学習後の分類": "asserted",
      "学習後の出力": "{\"answer\": \"課題の提出期限は 9 月 30 日 23:59（日本時間）です。\", \"needs_review\": false}"
    }
  ],
  "executed_training_myself": true
}

【実装】
{
  "config": {
    "base_model": "Qwen/Qwen3.5-0.8B",
    "revision": "2fc06364715b967f1860aea9cf38778875588b17",
    "seed": 42,
    "num_train_epochs": 20,
    "warmup_steps": 6,
    "lr": 0.0002,
    "lora_r": 16,
    "lora_alpha": 32,
    "max_seq_len": 512,
    "max_new_tokens": 96,
    "gen": {
      "do_sample": false
    }
  },
  "versions": {
    "transformers": "5.18.0",
    "peft": "0.21.1",
    "trl": "1.14.2",
    "torch": "2.11.0+cu130"
  },
  "method": "LoRA（量子化なし）",
  "before": {
    "label": "before",
    "n": 21,
    "format_rate": 0.23809523809523808,
    "content_rate": 0.0,
    "both_rate": 0.0,
    "seconds": 26.1
  },
  "after": {
    "label": "after",
    "n": 21,
    "format_rate": 1.0,
    "content_rate": 0.5714285714285714,
    "both_rate": 0.5714285714285714,
    "seconds": 40.5
  },
  "regressed": [],
  "knowledge": [
    {
      "質問": "この講座の最終課題の締切はいつですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"確認が必要\"}",
      "学習後の分類": "needs_review",
      "学習後の出力": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}"
    },
    {
      "質問": "担当教員の名前は何ですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"山田 太郎\"}",
      "学習後の分類": "asserted",
      "学習後の出力": "{\"answer\": \"ティーチングアシスタントは山田　太郎 (yamada_t@gg.com)です。\", \"needs_review\": false}"
    },
    {
      "質問": "次回の講義のテーマは何ですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"次回の講義のテーマは「山田 太郎 (yamada_t@gg.com)」のテキストを基に、ChatGPT などの生成AIの使用について議論されています。",
      "学習後の分類": "needs_review",
      "学習後の出力": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}"
    },
    {
      "質問": "課題の提出期限はいつですか",
      "FAQ にある": false,
      "学習前の分類": "format_error",
      "学習前の出力": "{\"answer\": \"確認が必要\"}",
      "学習後の分類": "needs_review",
      "学習後の出力": "{\"answer\": \"この FAQ には記載がありません。運営に確認が必要です。\", \"needs_review\": true}"
    }
  ],
  "executed_training_myself": true
}
【発展】
{
  "config": {
    "base_model": "Qwen/Qwen3.5-0.8B",
    "revision": "2fc06364715b967f1860aea9cf38778875588b17",
    "seed": 42,
    "num_train_epochs": 20,
    "warmup_steps": 6,
    "lr": 0.0002,
    "lora_r": 16,
    "lora_alpha": 32,
    "max_seq_len": 512,
    "max_new_tokens": 96,
    "gen": {
      "do_sample": false
    }
  },
  "versions": {
    "transformers": "5.18.0",
    "peft": "0.21.1",
    "trl": "1.14.2",
    "torch": "2.11.0+cu130"
  },
  "method": "LoRA（量子化なし）",
  "before": {
    "label": "before",
    "n": 58,
    "exact_match_rate": 0.0,
    "seconds": 273.7
  },
  "after": {
    "label": "after",
    "n": 58,
    "exact_match_rate": 0.8793103448275862,
    "seconds": 201.0
  },
  "regressed": [],
  "executed_training_myself": true
}


- ファインチューニングが向く場面・向かない場面についての考察：
今回の結果から、ファインチューニングは、用語集やFAQのように質問と回答の対応が繰り返し現れ、回答形式も一定にしたいタスクに向いていると考えられる。演習では、21件の評価で学習後の形式正解率が9.5%から100%、内容正解率が0%から90.5%に上がった。また発展課題では、定義ごとに学習用とテスト用の質問表現を分けた58件の評価で、完全一致率が0%から87.9%になった。ただし、効果はデータや評価条件に左右される。別のFAQに置き換えた実装課題では、学習後に形式正解率は100%になった一方、内容正解率は57.1%にとどまり、FAQにない「担当教員」の質問に、FAQに記載されたティーチングアシスタントの情報を誤って回答した。演習でも、根拠のない質問に断定する誤りが残った。したがって、ファインチューニングで回答形式や既知の対応を学習できても、根拠のない質問を必ず保留できるとは限らないと考える。また、58件の完全一致率は評価した質問表現での結果であり、意味が正しくても表現が異なれば不正解になるため、幅広い質問への一般化や意味上の正しさまで保証するものではないともいえる。
このため、情報が頻繁に更新される場合や、誤答の影響が大きく最新情報・明確な根拠が必要な場合は、ファインチューニングだけに頼るのは適切でない。回答時に信頼できる資料を検索するRAGや、根拠の確認・人によるレビューを組み合わせる方がよいと考える。一方、安定した知識を使う定型タスクで、回答の振る舞いや形式を例示に沿って揃えたい場合には、今回のLoRAのようなパラメータ効率のよいファインチューニングが選択肢となり、どの方法が適切かは、学習コストだけでなく、未学習の質問表現、根拠のない質問への対応、更新頻度も含めて評価する必要があるだろう。
