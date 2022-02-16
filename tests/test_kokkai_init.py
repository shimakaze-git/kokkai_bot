#!/usr/bin/env python

"""Tests for `kokai_kokkai_init` package."""

# import pytest

# from logics.kokai_bot import (
#     Kokkai, speechs_cleanning, text_parse,
#     get_meeting_records, get_list_counter, get_nouns_in_speechs
# )

# from logics.kokkai_bot import main
from logics.init import main, check_range_data, check_week_run_before


def test_comment_count_in_mouth():

    # comment = "DX"
    comment = ""
    speaker = ""

    from_date = "2022-01-01"
    # from_date = "2022-01-30"
    until_date = "2022-01-31"

    # main(comment, speaker, from_date, until_date)

def test_check_mouth():

    # comment = "DX"
    comment = ""
    speaker = ""

    from_date = "2022-01-01"
    # until_date = "2022-01-10"
    until_date = "2022-01-31"

    check = check_range_data(comment, speaker, from_date, until_date)
    print("check", check)

    print("---" * 30)

    date_day = "2022-02-06"
    # date_day = "2022-05-01"
    from_date, until_date = check_week_run_before(date_day)
    print("from_date, until_date", from_date, until_date)
    main(comment, speaker, from_date, until_date)