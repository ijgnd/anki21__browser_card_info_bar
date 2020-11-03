# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html, Copyright: see __init__.py

import time
from types import SimpleNamespace

from aqt import mw
from anki.utils import pointVersion

from .helper import (
    due_day, 
    is_early_review_then_return_percentage_interval
)


def date(tm):
    # the argument tm will always be a float or int because the argument date gets is always the 
    # result of a division and division only works on floats or ints. Originally the argument
    # passed to this function was the result of a truediv (recently I changed to a floordiv).
    # But this shouldn't make a difference because for time.localtime according to 
    # https://docs.python.org/3/library/time.html: "Fractions of a second are ignored." 

    # issue 5 is about this function returning "OSError: [Errno 22] Invalid argument"
    # I'm not sure why this happens.
    # https://stackoverflow.com/a/41400321 talks about a 2038 problem in Windows
    # but this seems to be limited to 32 bit platforms, see https://docs.python.org/3/library/time.html
    # and I tested in Win10(64bit) with Anki 2.1.35 where I can process values like 9999999999
    # which returns 2286-11-20.
    # But there are still alternative 32builds for windows available.
    
    # datetime doesn't seem to help, https://docs.python.org/3/library/datetime.html
    # classmethod date.fromtimestamp(timestamp)
    #   Return the local date corresponding to the POSIX timestamp, such as is returned by time.time().
    #   This may raise OverflowError, if the timestamp is out of the range of values supported by 
    #   the platform C localtime() function, and OSError on localtime() failure. It’s common for 
    #   this to be restricted to years from 1970 through 2038. 

    if tm > 2147483647:  #  03:14:08 UTC on 19 January 2038
        # see https://en.wikipedia.org/wiki/Year_2038_problem
        return "2038 or later"   
    if tm < 0:
        # time.strftime("%Y-%m-%d", time.localtime(-1)) works differently depending on the OS:
        #    in Linux it returns "1970-01-01"
        #    in Windows I get OSError: [Errno 22] Invalid argument
        print(f'unexpected behavior in add-on "Card Info Bar": tm is int smaller than 0, its value is {str(tm)}')
        return ""
    else:
        return time.strftime("%Y-%m-%d", time.localtime(tm))


def format_time_helper(val):
    # before 2.1.22 it was fmtTimeSpan
    if pointVersion() > 28:
        out = mw.col.format_timespan(val)
    else:
        out = mw.col.backend.format_time_span(val)
    return out


def cardstats(self,card):
    #from anki.stats.py
    (cnt, total) = mw.col.db.first(
        "select count(), sum(time)/1000 from revlog where cid = ?", card.id)
    first = mw.col.db.scalar(
        "select min(id) from revlog where cid = ?", card.id)
    last = mw.col.db.scalar(
        "select max(id) from revlog where cid = ?", card.id)

    o = dict()
    #Card Stats as seen in Browser
    o["Added"]        = date(card.id//1000)
    o["FirstReview"]  = date(first//1000) if first else ""
    o["LatestReview"] = date(last//1000) if last else ""
    o["Due"]          = due_day(card)
    o["Interval"]     = format_time_helper(card.ivl * 86400) if card.queue == 2 else ""
    o["Ease"]         = "%d%%" % (card.factor/10.0)
    o["Reviews"]      = "%d" % card.reps
    o["Lapses"]       = "%d" % card.lapses
    o["AverageTime"]  = format_time_helper(total / float(cnt)) if cnt else ""
    o["TotalTime"]    = format_time_helper(total) if cnt else ""
    o["Position"]     = card.due if card.queue == 0 else ""
    o["CardType"]     = card.template()['name']
    o["NoteType"]     = card.model()['name']
    o["Deck"]         = mw.col.decks.name(card.did)
    o["NoteID"]       = card.nid
    o["CardID"]       = card.id
    o["CardOrd"]      = card.ord

    if card.odid:
        o["source_deck_name"] = mw.col.decks.get(card.odid)['name']
    else:
        o["source_deck_name"] = ""

    #other useful info
    o["dueday"]               = due_day(card)
    o["value_for_overdue"]    = mw.col.sched._daysLate(card)
    o["actual_ivl"]           = card.ivl + mw.col.sched._daysLate(card)
    o["is_early_review_then_percentage_interval"] = is_early_review_then_return_percentage_interval(card)
    
    for k,v in o.items():
        o[k] = str(v)
    return SimpleNamespace(**o)
