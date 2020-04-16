#https://github.com/ijgnd/anki__reviewer_deck_and_card_info_sidebar/blob/master/src/deck_and_card_info_during_review/helper_functions.py

import time

from aqt import mw


def due_day(card):
    if card.queue <= 0:
        return ""
    else:
        if card.queue in (2,3):
            if card.odue:
                myvalue = card.odue
            else:
                myvalue = card.due
            mydue = time.time()+((myvalue - mw.col.sched.today)*86400)
        else:
            if card.odue:
                mydue = card.odue
            else:
                mydue = card.due
    try:
        out = time.strftime("%Y-%m-%d", time.localtime(mydue)) 
    except:
        out = ""
    return out


def is_early_review_then_return_percentage_interval(card):
    due = card.odue if card.odid else card.due
    if not due > mw.col.sched.today:
        return False
    else:
        if card.queue == 1:  #learn
            return False
        elif card.queue == 0 and card.type == 0:   #new
            return False
        else:
            try:
                lastRev = due - card.ivl
                elapsed = mw.col.sched.today - lastRev
                p = elapsed/float(card.ivl) * 100
                pf = "{0:.2f}".format(p) + " %"
                return pf
            except ZeroDivisionError:
                return False
