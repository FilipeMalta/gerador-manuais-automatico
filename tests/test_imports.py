"""Sanity check: verifica que src.gerador_manual importa sem erro."""

from src.gerador_manual import criar_manual


def test_importa_criar_manual():
    assert callable(criar_manual)
