"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask --temperature 0.2 "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
conversation_history: list[tuple[str, str]] = []


def parse_temperature(value: str) -> float:
    try:
        temperature = float(value)
    except ValueError as e:
        raise argparse.ArgumentTypeError("temperature は数値で指定してください") from e
    if not 0.0 <= temperature <= 2.0:
        raise argparse.ArgumentTypeError("temperature は 0.0〜2.0 の範囲で指定してください")
    return temperature


def ask(question: str, temperature: float | None = None) -> str:
    client = genai.Client(api_key=get_api_key())
    started_at = time.perf_counter()
    config = (
        types.GenerateContentConfig(temperature=temperature)
        if temperature is not None
        else None
    )
    response = client.models.generate_content(
        model=MODEL, contents=question, config=config
    )
    response_time_ms = (time.perf_counter() - started_at) * 1000

    if response.usage_metadata:
        print(
            f"[usage] 入力トークン数: {response.usage_metadata.prompt_token_count}, "
            f"出力トークン数: {response.usage_metadata.candidates_token_count}"
        )
    print(f"[response time] {response_time_ms:.0f} ms")

    # 　　会話履歴を保持するための処理を追加する
    # 　　ここでは、単純なリストを使って会話履歴を保持する
    conversation_history.append((question, response.text))
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--temperature",
        type=parse_temperature,
        help="生成時のtemperature（0.0〜2.0、省略時はモデル既定値）",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    if args.temperature is not None:
        print(f"[temperature] {args.temperature}")
    print(f"[質問] {args.question}\n")
    try:
        print(ask(args.question, temperature=args.temperature))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
