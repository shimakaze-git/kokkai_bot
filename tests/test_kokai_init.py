#!/usr/bin/env python

"""Tests for `kokai_kokkai_init` package."""

# import pytest

# from logics.kokai_bot import (
#     Kokkai, speechs_cleanning, text_parse,
#     get_meeting_records, get_list_counter, get_nouns_in_speechs
# )
from logics.kokai_bot import main


def test_comment_count_in_mouth():

    # comment = "DX"
    comment = ""
    speaker = ""

    # from_date = "2022-01-01"
    from_date = "2022-01-30"
    until_date = "2022-01-31"

    main(comment, speaker, from_date, until_date)
