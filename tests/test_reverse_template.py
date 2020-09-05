import pytest

from template_reverse import ReverseTemplate
from uuid import uuid4


def test_find_tokens():
    rt = ReverseTemplate("{t1}_{t2}-{t3}:{t4}")

    assert "t1" in rt.tokens
    assert "t2" in rt.tokens
    assert "t3" in rt.tokens
    assert "t4" in rt.tokens


def test_find_tokens_with_weird_template():

    rt = ReverseTemplate("x{t1}_}_{t2} {a_weird_but_valid-{token} {t3}.jpg")

    assert len(rt.tokens) == 4
    assert "t1" in rt.tokens
    assert "t2" in rt.tokens
    assert "t3" in rt.tokens
    assert "a_weird_but_valid-{token" in rt.tokens


def test_reverse_simple_value():

    rt = ReverseTemplate("{t1}_{t2}.png")

    expected_value = str(uuid4()) + ".sometesttrash"

    values = rt.reverse(f"{expected_value}_2020-02-02.png")

    assert values["t1"] == expected_value
    assert values["t2"] == "2020-02-02"


def test_value_with_prefix():
    rt = ReverseTemplate("_{t1}_{t2}a_more_complex_content{t3}.mp4")

    values = rt.reverse("_ayyyy_2020-02-02a_more_complex_content98.mp4")

    assert values["t1"] == "ayyyy"
    assert values["t2"] == "2020-02-02"
    assert values["t3"] == "98"


def test_value_with_separator_gets_unexpected_result():
    rt = ReverseTemplate("{id}-{image_start_date}")

    values = rt.reverse("a-y_y_y-2020-02-02.jpg")

    assert values["id"] == "a"
    assert values["image_start_date"] == "y_y_y-2020-02-02.jpg"


def test_template_is_only_one_token():
    rt = ReverseTemplate("{it_gets_everything}")

    values = rt.reverse("I_AM_EVERYTHING")

    assert "it_gets_everything" in rt.tokens
    assert values["it_gets_everything"] == "I_AM_EVERYTHING"


def test_static_then_end():
    rt = ReverseTemplate("blablalah3pdcsdwet{final}")

    values = rt.reverse("blablalah3pdcsdwetTHEEND")

    assert "final" in rt.tokens
    assert values["final"] == "THEEND"


def test_no_tokens():
    rt = ReverseTemplate("¯\\_(ツ)_/¯")

    values = rt.reverse("")

    assert not rt.tokens
    assert values == {}


def test_raise_if_duplicated_token():
    with pytest.raises(ValueError, match="dup"):
        ReverseTemplate("cry in {dup} {?} {dup} tears")
