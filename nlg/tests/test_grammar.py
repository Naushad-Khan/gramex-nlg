#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Tests for the nlg.grammar module.
"""
import unittest
import nlg.grammar as G


class TestGrammar(unittest.TestCase):
    def test_concatenate_items(self):
        self.assertEqual(G.concatenate_items("abc"), "a, b and c")
        self.assertEqual(G.concatenate_items([1, 2, 3], sep=""), "123")
        self.assertFalse(G.concatenate_items([]))

    def test_pluralize(self):
        self.assertEqual(G.plural("language"), "languages")
        self.assertEqual(G.plural("languages"), "languages")
        self.assertEqual(G.plural("bacterium"), "bacteria")
        self.assertEqual(G.plural("goose"), "geese")

    def test_singular(self):
        self.assertEqual(G.singular("languages"), "language")
        self.assertEqual(G.singular("language"), "language")
        self.assertEqual(G.singular("bacteria"), "bacterium")
        self.assertEqual(G.singular("geese"), "goose")

    def test_pluralize_by_seq(self):
        self.assertEqual(G.pluralize_by_seq("language", [1, 2]), "languages")
        self.assertEqual(G.pluralize_by_seq("languages", [1]), "language")
        self.assertEqual(G.pluralize_by_seq("language", []), "language")