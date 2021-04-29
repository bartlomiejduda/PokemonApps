# coding: utf-8

"""
Tests for the Pokemon Service
"""

from nameko_main import PokemonService


class TestPokemon(object):

    def test_moves_result(self, container_factory, web_config, web_session):
        container = container_factory(PokemonService, web_config)
        container.start()

        res = web_session.get("/get/1")
        assert res.status_code == 200
        assert "amnesia" in res.text

        res = web_session.get("/get/5")
        assert res.status_code == 200
        assert "bide" in res.text

        res = web_session.get("/get/0")
        assert "Error" in res.text