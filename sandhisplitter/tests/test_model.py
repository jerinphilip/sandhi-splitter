# -*- coding: utf-8 -*-
from sandhisplitter.model import Model
from testtools import TestCase
from sandhisplitter.util import extract


class TestModel(TestCase):
    def setUp(self):
        super(TestModel, self).setUp()
        self.testModel = Model(depth=3, skip=1)

    def test_load(self):
        entries = [
                u'വിഡ്‌ഢിയുണ്ടെങ്കില്‍=വിഡ്‌ഢി+ഉണ്ട്+എങ്കില്‍|7,11',
                u'അകല്‍ച്ചയുടെസ്ഥാനത്തു്=അകല്‍ച്ചയുടെ+സ്ഥാനത്തു്|10',
                u'അകലെയാണ്=അകലെ+ആണ്|4',
                u'അകലെയുമല്ലാതെ=അകലെയും+അല്ലാതെ|6',
                u'അകലെയുമാ​യിരുന്നു=അകലെയും+ആയിരുന്നു|6',
                u'അകലെയുള്ള=അകലെ+ഉള്ള|4',
                u'അകാരണമായി=അകാരണം+ആയി |5',
                u'അക്കമിട്ടുപറയുന്നുണ്ട്=അക്കമിട്ടു+പറയുന്നുണ്ട് |9',
                u'അക്കരക്കാരെന്നൊരു=അക്കരക്കാര്‍+എന്നൊരു|9',
                u'അക്കരെയിക്കരെ=അക്കരെ+ഇക്കരെ|6',
                u'അക്കാദമിക്കാണ്=അക്കാദമിക്+ആണ്|10',
                u'അക്കൗണ്ടിലാക്കാന്‍=അക്കൗണ്ടിൽ+ആക്കാന്‍ |9',
                u'അക്കൗണ്ടിലാക്കാന്‍=അക്കൗണ്ടില്‍+ആക്കാന്‍ |9',
                u'അക്ഷയപാത്രശാലയായി=അക്ഷയപാത്രശാല+ആയി |13',
                u'അക്ഷരജ്ഞാനംപോലും=അക്ഷരജ്ഞാനം+പോലും|10',
                u'അഗ്നിസാക്ഷിയായിത്തന്നെ=അഗ്നിസാക്ഷി+ആയി+തന്നെ|11,16',
                u'അങ്ങട്ടുമിങ്ങട്ടുമോടിച്ചു=അങ്ങട്ടും+ഇങ്ങട്ടും+ഓടിച്ചു |8,17',
                u'അങ്ങനെയാണ്=അങ്ങനെ+ആണ് |6',
                u'അങ്ങനെയാണെങ്കില്‍=അങ്ങനെ+ആണ്+എങ്കിൽ|6,8',
                u'അങ്ങനെയാണെങ്കില്‍=അങ്ങനെ+ആണ്+എങ്കില്‍|6,8',
                ]
        for line in entries:
            (word, splits, locs) = extract(line)
            self.testModel.add_entry(word, splits, locs)
