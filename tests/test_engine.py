from friday.engine import FridayBrain, KnowledgeShard


def test_response_contains_question_mark():
    brain = FridayBrain(seed=123)
    reply = brain.respond("Friday, pomóż z projektem.")
    assert "?" in reply


def test_response_uses_matching_shard():
    shard = KnowledgeShard(
        topic="test",
        keywords=("specjalny",),
        connection="Specjalny miks danych, bo Friday lubi customowe sprawy.",
    )
    brain = FridayBrain(seed=7, shards=(shard,))
    reply = brain.respond("Mam specjalny projekt w chmurze.")
    assert "Specjalny miks" in reply
    assert "test" in reply
