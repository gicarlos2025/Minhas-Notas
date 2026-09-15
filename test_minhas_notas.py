import os
import tempfile
import unittest

import tkinter as tk

from MinhasNotas import EstatisticasTexto, RepositorioArquivosTexto


class EstatisticasTextoTests(unittest.TestCase):
    def test_calcula_estatisticas_do_texto(self):
        estatisticas = EstatisticasTexto.calcular("Olá mundo\nTeste de texto")

        self.assertEqual(estatisticas["linhas"], 2)
        self.assertEqual(estatisticas["palavras"], 5)
        self.assertEqual(estatisticas["caracteres"], 24)

    def test_calcula_estatisticas_para_texto_vazio(self):
        estatisticas = EstatisticasTexto.calcular("")

        self.assertEqual(estatisticas["linhas"], 1)
        self.assertEqual(estatisticas["palavras"], 0)
        self.assertEqual(estatisticas["caracteres"], 0)


class RepositorioArquivosTextoTests(unittest.TestCase):
    def test_salva_e_ler_arquivo_de_texto(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = os.path.join(diretorio, "arquivo.txt")
            conteudo = "Linha 1\nLinha 2"

            RepositorioArquivosTexto.salvar(caminho, conteudo)
            texto_lido = RepositorioArquivosTexto.ler(caminho)

            self.assertEqual(texto_lido, conteudo)


if __name__ == "__main__":
    unittest.main()
