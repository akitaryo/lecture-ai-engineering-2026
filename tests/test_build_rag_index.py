"""実SQLiteと固定ベクトルで、索引作成から検索までを確認する。APIは呼ばない。"""

import json
from unittest.mock import Mock

import pytest

from app import retrieval
from scripts.build_rag_index import build_index


@pytest.fixture
def materials(tmp_path):
    source = tmp_path / "lectures.json"
    source.write_text(json.dumps([
        {"id": f"lec{n:02d}-main", "title": f"講義{n}", "content": [
            {"section": "章", "content": [
                {"id": f"lec{n:02d}-main-p001", "title": f"ページ{n}",
                 "page": 1, "content": f"本文{n}"}]}]}
        for n in (1, 2, 5)
    ], ensure_ascii=False), encoding="utf-8")
    return source, tmp_path / "index.sqlite3"


def test_built_index_can_be_searched(materials, monkeypatch):
    source, database = materials
    texts = []

    def embed(text, task):
        assert task == "RETRIEVAL_DOCUMENT"
        texts.append(text)
        return [1, 0] if "本文1" in text else [0, 1]

    result = build_index(source, database, embedder=embed)
    assert result["pages"] == 2  # 第5回の資料は検索対象に含めない
    assert all("章" in text and "ページ" in text for text in texts)
    monkeypatch.setattr(retrieval, "RAG_DB", database)
    monkeypatch.setattr(retrieval, "embed_text", lambda *_: [1, 0])
    hits = retrieval.search("質問")
    assert [h["page_id"] for h in hits] == ["lec01-main-p001", "lec02-main-p001"]
    assert hits[0]["content"] == "本文1"
    assert hits[0]["distance"] == pytest.approx(0)


def test_existing_index_survives_failed_rebuild(materials):
    source, database = materials
    build_index(source, database, embedder=lambda *_: [1, 0])
    before = database.read_bytes()
    embed = Mock(side_effect=RuntimeError("埋め込みに失敗"))
    with pytest.raises(FileExistsError):
        build_index(source, database, embedder=embed)
    embed.assert_not_called()
    with pytest.raises(RuntimeError, match="埋め込みに失敗"):
        build_index(source, database, rebuild=True, embedder=embed)
    assert database.read_bytes() == before
    assert not list(database.parent.glob(".rag-build-*"))


def test_neighbor_context_stays_within_document_and_deduplicates():
    pages = {
        f"lec01-p{i:03d}": {
            "page_id": f"lec01-p{i:03d}",
            "document_id": "lec01-main",
            "page": i,
            "content": f"本文{i}",
        }
        for i in range(1, 4)
    }

    context = retrieval._neighbor_context("lec01-p002", "lec01-main", pages)

    assert [page["page_id"] for page in context] == [
        "lec01-p001", "lec01-p002", "lec01-p003",
    ]
    assert len(context) == len({page["page_id"] for page in context})
    assert retrieval._neighbor_context("lec01-p002", "lec02-main", pages) == []


def test_browse_tree_returns_breadcrumbs_candidates_and_section_neighbors(tmp_path, monkeypatch):
    tree = tmp_path / "tree.json"
    tree.write_text(json.dumps({
        "id": "root",
        "kind": "collection",
        "title": "資料",
        "children": [{
            "id": "lec01-main",
            "kind": "document",
            "title": "第1回",
            "children": [
                {
                    "id": "lec01-main-s001",
                    "kind": "section",
                    "title": "章1",
                    "children": [
                        {"id": "lec01-main-p001", "kind": "page", "title": "ページ1"},
                        {"id": "lec01-main-p002", "kind": "page", "title": "ページ2"},
                    ],
                },
                {
                    "id": "lec01-main-s003",
                    "kind": "section",
                    "title": "章2",
                    "children": [
                        {"id": "lec01-main-p003", "kind": "page", "title": "ページ3"},
                    ],
                },
            ],
        }],
    }, ensure_ascii=False), encoding="utf-8")
    source = tmp_path / "lectures.json"
    source.write_text(json.dumps([{
        "id": "lec01-main",
        "title": "第1回",
        "content": [{
            "section": "章",
            "content": [
                {"id": "lec01-main-p001", "title": "ページ1", "page": 1, "content": "文章一です。文章二です。本文は続きます。"},
                {"id": "lec01-main-p002", "title": "ページ2", "page": 2, "content": "文章三です。"},
                {"id": "lec01-main-p003", "title": "ページ3", "page": 3, "content": "章境界です。"},
            ],
        }],
    }], ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(retrieval, "RAG_TREE", tree)
    monkeypatch.setattr(retrieval, "RAG_SOURCE", source)

    root = retrieval.browse_tree()
    assert root["breadcrumb"][-1]["id"] == "root"
    assert root["children"][0]["id"] == "lec01-main"

    section = retrieval.browse_tree("lec01-main-s001")
    assert section["breadcrumb"][-1]["id"] == "lec01-main-s001"
    assert section["children"][0]["content"] == "文章一です。文章二です。"
    assert [item["id"] for item in section["neighbor_sections"]] == [
        "lec01-main-s001", "lec01-main-s003",
    ]

    page = retrieval.browse_tree("lec01-main-p002")
    assert page["node"]["content"].startswith("文章三です")
    assert [item["page_id"] for item in page["context"]] == [
        "lec01-main-p001", "lec01-main-p002", "lec01-main-p003",
    ]
