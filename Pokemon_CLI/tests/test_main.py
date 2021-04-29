# coding: utf-8

"""
Tests for the Pokemon Script
"""

from main import get_poke_moves


class TestPokemonScript(object):

    def test_moves_result(self):
        res = get_poke_moves(1)
        assert "amnesia" in res

        res = get_poke_moves(5)
        assert "bide" in res

        res = get_poke_moves(0)
        assert res == 1