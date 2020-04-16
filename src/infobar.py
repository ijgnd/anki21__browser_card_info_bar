# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html, Copyright: see __init__.py

from anki.sched import Scheduler
from anki.utils import ids2str, intTime
from anki.hooks import addHook, wrap

from aqt import mw
from aqt.qt import *
from aqt.forms.browser import Ui_Dialog
from aqt.browser import Browser

from .card_properties import cardstats


def gc(arg,fail=False):
    return mw.addonManager.getConfig(__name__).get(arg,fail)


def editor_by_the_side(self):
    # better compatibility with "browser side-by-side (horizontal split)"
    # https://ankiweb.net/shared/info/831846358
    try:
        if self.side_by_side:
            return True
        else:
            return False
    except:
        return False
Browser.editor_by_the_side = editor_by_the_side


def addInfoBar(self):
    if self.editor_by_the_side() and gc("narrow info bar when editor by the side"):
        self.addInfoBar_narrow()
    else:
        self.addInfoBar_default()
Browser.addInfoBar = addInfoBar


def addInfoBar_narrow(self):
    a = ["dates", "dueIvlEase", "RvsLpsAvtime", "cidNid", "cardtypeOrd", "noteType", "Deck"]
    for i in a:
        setattr(self,"il_" + i, QLabel(self))
        setattr(self,"i_" + i, QLabel(self))

    g = [
        #       0                1            2  3  4  5      6                7   8  9 10 11
        [self.il_dates,       'Ad/FR/LR: ',   0, 0, 1, 1, self.i_dates,        "", 0, 1, 1, 1],
        [self.il_dueIvlEase,  'Du/Iv/Es: ',   1, 0, 1, 1, self.i_dueIvlEase,   "", 1, 1, 1, 1],
        [self.il_RvsLpsAvtime,'Rv/Lp/AvTi: ', 2, 0, 1, 1, self.i_RvsLpsAvtime, "", 2, 1, 1, 1],
        [self.il_cidNid,      'cid/nid: ',    3, 0, 1, 1, self.i_cidNid,       "", 3, 1, 1, 1],
        [self.il_cardtypeOrd, 'Ctyp/Tmpl: ',  4, 0, 1, 1, self.i_cardtypeOrd,  "", 4, 1, 1, 1],
        [self.il_noteType,    'Notetype: ',   5, 0, 1, 1, self.i_noteType,     "", 5, 1, 1, 1],
        [self.il_Deck,        'Deck: ',       6, 0, 1, 1, self.i_Deck,         "", 6, 1, 1, 1],
    ]

    while self.form.infogrid.count():
        item = self.form.infogrid.takeAt(0)
        widget = item.widget()
        widget.deleteLater()

    for l in g:
        t = "<b>" + l[1] + "</b>"  # increases height noticeably
        l[0].setText(t) 
        #l[0].setStyleSheet('background-color: rgb(100, 10, 1);')
        l[6].setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.form.infogrid.addWidget(l[0], l[2], l[3], l[4], l[5])
        self.form.infogrid.addWidget(l[6], l[8], l[9], l[10], l[11])
Browser.addInfoBar_narrow = addInfoBar_narrow


def addInfoBar_default(self):
    a = ["added","fr","lr","due","ivl","ease","revs","laps","avTime",
            "cardType","noteType","Deck", "nid", "cid"] 
    for i in a:
        setattr(self,"il_" + i, QLabel(self))
        setattr(self,"i_" + i, QLabel(self))

    g = [
        #      0                1           2  3  4  5      6            7   8  9 10 11
        [self.il_added,    'Added:     ',   0, 0, 1, 1, self.i_added,    "", 0, 1, 1, 1],
        [self.il_fr,       'FirstRev:  ',   1, 0, 1, 1, self.i_fr,       "", 1, 1, 1, 1],
        [self.il_lr,       'LatestRev: ',   2, 0, 1, 1, self.i_lr,       "", 2, 1, 1, 1],
        [self.il_due,      'Due:  ',        0, 2, 1, 1, self.i_due,      "", 0, 3, 1, 1],
        [self.il_ivl,      'Ivl:  ',        1, 2, 1, 1, self.i_ivl,      "", 1, 3, 1, 1],
        [self.il_ease,     'Ease: ',        2, 2, 1, 1, self.i_ease,     "", 2, 3, 1, 1],
        [self.il_revs,     'Rvs/Lps: ',     0, 4, 1, 1, self.i_revs,     "", 0, 5, 1, 1],
        [self.il_nid,      'Note ID: ',     1, 4, 1, 1, self.i_nid ,     "", 1, 5, 1, 1],
        [self.il_cid,      'Card ID: ',     2, 4, 1, 1, self.i_cid,      "", 2, 5, 1, 1],
        [self.il_cardType, 'Card Type: ',   0, 6, 1, 1, self.i_cardType, "", 0, 7, 1, 1],
        [self.il_noteType, 'Note Type: ',   1, 6, 1, 1, self.i_noteType, "", 1, 7, 1, 2],
        [self.il_Deck,     'Deck:      ',   2, 6, 1, 1, self.i_Deck,     "", 2, 7, 1, 2],
        [self.il_avTime,   'AvgTime: ',     0, 8, 1, 1, self.i_avTime,   "", 0, 9, 1, 1],
    ]

    while self.form.infogrid.count():
        item = self.form.infogrid.takeAt(0)
        widget = item.widget()
        widget.deleteLater()

    for l in g:
        t = "<b>" + l[1] + "</b>"  # increaes height noticeable
        l[0].setText(t) 
        #l[0].setStyleSheet('background-color: rgb(100, 10, 1);')
        l[6].setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.form.infogrid.addWidget(l[0], l[2], l[3], l[4], l[5])
        self.form.infogrid.addWidget(l[6], l[8], l[9], l[10], l[11])
    
    self.form.infogrid.setColumnStretch(0,1)
    self.form.infogrid.setColumnStretch(1,2)
    self.form.infogrid.setColumnStretch(2,1)
    self.form.infogrid.setColumnStretch(3,2)
    self.form.infogrid.setColumnStretch(4,1)
    self.form.infogrid.setColumnStretch(5,2)
    self.form.infogrid.setColumnStretch(6,1)
    self.form.infogrid.setColumnStretch(7,4)
    self.form.infogrid.setColumnStretch(8,1)
    self.form.infogrid.setColumnStretch(9,2)
Browser.addInfoBar_default = addInfoBar_default


def updateInfoBar(self):
    if self.editor_by_the_side() and gc("narrow info bar when editor by the side"):
        updateInfoBar_narrow(self)
    else:
        updateInfoBar_default(self)
Browser.updateInfoBar = updateInfoBar


def updateInfoBar_narrow(self):
    if self.card:
        p = self.cardstats(self.card)
        try:
            self.i_dates.setText("{}/{}/{}".format(p.Added, p.FirstReview, p.LatestReview))  # Added/FirRev/LatRev
            self.i_dueIvlEase.setText("{}/{}/{}".format(p.Due, p.Interval, p.Ease))  # Due/Ivl/Ease
            self.i_RvsLpsAvtime.setText("{}/{}/{}".format(p.Reviews, p.Lapses, p.AverageTime))  # Rvs/Lps/AvgTime
            self.i_cidNid.setText("{}/{}".format(p.CardID, p.NoteID))  # cid/nid
            self.i_cardtypeOrd.setText("{}/{}".format(p.CardType, p.CardOrd))  # CardType/TmplNo
            self.i_noteType.setText(p.NoteType)   # NoteType
            self.i_Deck.setText(p.Deck)  # Deck
        except:
            pass


def updateInfoBar_default(self):
    if self.card:
        p = self.cardstats(self.card)
        try:
            self.i_added.setText(p.Added) 
            self.i_fr.setText(p.FirstReview) 
            self.i_lr.setText(p.LatestReview)
            self.i_due.setText(p.Due)
            self.i_ivl.setText(p.Interval)
            self.i_ease.setText(p.Ease)
            self.i_revs.setText(p.Reviews + " / " + p.Lapses)
            self.i_avTime.setText(p.AverageTime)
            self.i_cardType.setText(p.CardType)
            self.i_noteType.setText(p.NoteType)
            self.i_Deck.setText(p.Deck)
            self.i_nid.setText(p.NoteID)
            self.i_cid.setText(p.CardID)
        except:
            pass


def setupUi(self, Dialog):
    self.verticalLayout_2.removeWidget(self.tableView)
    self.infogrid = QGridLayout()
    self.infowidget = QWidget()
    self.infowidget.setLayout(self.infogrid)
    if not gc("enable by default"):
        self.infowidget.setVisible(False)
    self.verticalLayout_2.addWidget(self.infowidget)    
    self.verticalLayout_2.addWidget(self.tableView)


Ui_Dialog.setupUi = wrap(Ui_Dialog.setupUi, setupUi)
#addHook("browser.setupMenus", addInfoBar)
addHook("browser.rowChanged", updateInfoBar)
Browser.cardstats = cardstats


def toggle_infobox(self):
    if not self.form.infowidget.isVisible():
        self.form.infowidget.setVisible(True)
        self.addInfoBar()
        self.updateInfoBar()
    else:
        self.form.infowidget.setVisible(False)
Browser.toggle_infobox = toggle_infobox


def onSetupMenus(self):
    try:
        m = self.menuView
    except:
        self.menuView = QMenu("&View")
        action = self.menuBar().insertMenu(
            self.mw.form.menuTools.menuAction(), self.menuView)
        m = self.menuView

    # a = m.addAction('toggle infobox')
    # a.triggered.connect(self.toggle_infobox)
    a = m.addAction('show infobox')
    a.setCheckable(True)
    a.setChecked(gc("enable by default"))
    a.toggled.connect(self.toggle_infobox) 
    cut = gc("show_infobox")
    if cut:
        a.setShortcut(QKeySequence(cut))
addHook("browser.setupMenus", onSetupMenus)


