# -*- coding: iso-8859-1 -*-
"""test error checking"""
# Copyright (C) 2004  Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import unittest

import linkcheck.ftests
import linkcheck.url


class TestError (linkcheck.ftests.StandardTest):
    """test unrecognized or syntactically wrong links"""

    def test_unrecognized (self):
        """unrecognized scheme test"""
        url = "hutzli:"
        nurl = linkcheck.url.url_norm(url)
        resultlines = [
            "url %r" % url,
            "cache key None",
            "real url %s" % nurl,
            "error",
        ]
        self.direct(url, resultlines)

    def test_leading_whitespace (self):
        """leading whitespace test"""
        url = " http://www.heise.de/"
        nurl = linkcheck.url.url_norm(url)
        resultlines = [
            "url %r" % url,
            "cache key None",
            "real url %s" % nurl,
            "error",
        ]
        self.direct(url, resultlines)
        url = "\nhttp://www.heise.de/"
        nurl = linkcheck.url.url_norm(url)
        resultlines = [
            "url %r" % url,
            "cache key None",
            "real url %s" % nurl,
            "error",
        ]
        self.direct(url, resultlines)

    def test_trailing_whitespace (self):
        """trailing whitespace test"""
        url = "http://www.heise.de/ "
        nurl = linkcheck.url.url_norm(url)
        resultlines = [
            "url %r" % url,
            "cache key %s" % nurl,
            "real url %s" % nurl,
            "warning Base URL is not properly normed. Normed url is %r." % nurl,
            "error",
        ]
        self.direct(url, resultlines)
        url = "http://www.heise.de/\n"
        nurl = linkcheck.url.url_norm(url)
        resultlines = [
            "url %r" % url,
            "cache key %s" % nurl,
            "real url %s" % nurl,
            "warning Base URL is not properly normed. Normed url is %r." % nurl,
            "error",
        ]
        self.direct(url, resultlines)

    def test_invalid (self):
        """invalid syntax test"""
        # invalid scheme chars
        url = "���?:"
        nurl = linkcheck.url.url_norm(url)
        resultlines = [
            "url %r" % url,
            "cache key None",
            "real url %s" % nurl,
            "error",
        ]
        self.direct(url, resultlines)
        # missing scheme alltogether
        url = "?���?"
        nurl = linkcheck.url.url_norm(url)
        resultlines = [
            "url %r" % url,
            "cache key None",
            "real url %s" % nurl,
            "error",
        ]
        self.direct(url, resultlines)
        # really fucked up
        url = "@���][� �@] ��"
        nurl = linkcheck.url.url_norm(url)
        resultlines = [
            "url %r" % url,
            "cache key None",
            "real url %s" % nurl,
            "error",
        ]
        self.direct(url, resultlines)


def test_suite ():
    """build and return a TestSuite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestError))
    return suite


if __name__ == '__main__':
    unittest.main()
