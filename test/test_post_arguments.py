import unittest
from unittest.mock import patch, MagicMock
from src.post_arguments import PDF_MIME_TYPE, argument_prompt

class TestPostArguments(unittest.TestCase):

    def test_pdf_mime_type(self):
        self.assertEqual(PDF_MIME_TYPE, "application/pdf")

    def test_argument_prompt(self):
        expected_prompt = """Liste os argumentos do texto, com o nome do autor, um título para o argumento, uma síntese do argumento e a url do texto.
Deve sempre haver 4 colunas preenchidas: uma com o nome do autor, outra com o título do argumento, a terceira com a síntese do argumento e quarta com a url, mesmo que o autor seja repetido.
Use o separador | entre as colunas.
Se houver mais de um argumento, liste-os em linhas separadas.
Toda a linha deve ter a url, mesmo que repetida.
Se não for possível identificar o autor, considere que é "Luis Quissak".
Se não for possível identificar o argumento, coloque o texto "não encontrado" nas 3 primeiras colunas, mas mantenha a coluna com a url preenchida. Ela deve se repetir para todos os argumentos do mesmo texto.
Não repita linhas.
"""
        self.assertEqual(argument_prompt, expected_prompt)

if __name__ == '__main__':
    unittest.main()