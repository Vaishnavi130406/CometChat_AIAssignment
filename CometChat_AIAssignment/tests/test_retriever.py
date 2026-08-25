from app.retriever import KnowledgeRetriever


def test_retriever_finds_shipping_information():
    retriever = KnowledgeRetriever()

    results = retriever.search(
        "Do you offer international shipping?"
    )

    assert len(results) > 0

    sources = [result["source"] for result in results]

    assert "06-international-shipping.md" in sources


def test_retriever_returns_source_metadata():
    retriever = KnowledgeRetriever()

    results = retriever.search("return policy")

    assert len(results) > 0

    assert "source" in results[0]
    assert "content" in results[0]
    assert "score" in results[0]