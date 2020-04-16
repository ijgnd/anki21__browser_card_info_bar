# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html, Copyright: see __init__.py

import time
from types import SimpleNamespace

from aqt import mw

from .helper import due_day, is_early_review_then_return_percentage_interval


def cardstats(self,card):
    #from anki.stats.py
    (cnt, total) = mw.col.db.first(
            "select count(), sum(time)/1000 from revlog where cid = :id",
            id=card.id)
    first = mw.col.db.scalar(
        "select min(id) from revlog where cid = ?", card.id)
    last = mw.col.db.scalar(
        "select max(id) from revlog where cid = ?", card.id)

    def date(tm):
        return time.strftime("%Y-%m-%d", time.localtime(tm))

    o = dict()
    #Card Stats as seen in Browser
    o["Added"]        = date(card.id/1000)
    o["FirstReview"]  = date(first/1000) if first else ""
    o["LatestReview"] = date(last/1000)if last else ""
    o["Due"]          = due_day(card)
    o["Interval"]     = mw.col.backend.format_time_span(card.ivl * 86400) if card.queue == 2 else ""
    o["Ease"]         = "%d%%" % (card.factor/10.0)
    o["Reviews"]      = "%d" % card.reps
    o["Lapses"]       = "%d" % card.lapses
    o["AverageTime"]  = mw.col.backend.format_time_span(total / float(cnt)) if cnt else ""
    o["TotalTime"]    = mw.col.backend.format_time_span(total) if cnt else ""
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
