import unittest
from unittest.mock import patch

import sistema


class SistemaTestCase(unittest.TestCase):
    def test_rolar_rejeita_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            sistema.rolar(0)
        with self.assertRaises(ValueError):
            sistema.rolar(-1)

    def test_regras_considera_um_falha_critica_em_qualquer_dificuldade(self):
        resultado = sistema.regras(1, 1)

        self.assertTrue(resultado['fracasso'])
        self.assertTrue(resultado['falha'])
        self.assertFalse(resultado['sucesso'])
        self.assertEqual(resultado['emoji'], sistema.Emojis.fcritica)

    def test_regras_rejeita_valores_fora_do_intervalo(self):
        with self.assertRaises(ValueError):
            sistema.regras(0)
        with self.assertRaises(ValueError):
            sistema.regras(11)
        with self.assertRaises(ValueError):
            sistema.regras(6, 10)

    def test_alterar_dificuldade_recalcula_sem_nova_rolagem(self):
        with patch('sistema.random.randint') as randint:
            resultado = sistema.alterar_dificuldade([1, 6, 10], 7)

        randint.assert_not_called()
        self.assertEqual(resultado['resultados'], [10, 6, 1])
        self.assertEqual(resultado['fracassos'], 1)
        self.assertEqual(resultado['criticos'], 1)
        self.assertEqual(resultado['sucessos'], 1)
        self.assertEqual(resultado['resultado_final'], 1)

    def test_alterar_dificuldade_rejeita_valores_invalidos(self):
        with self.assertRaises(ValueError):
            sistema.alterar_dificuldade([], 6)
        with self.assertRaises(ValueError):
            sistema.alterar_dificuldade([0, 6], 6)
        with self.assertRaises(ValueError):
            sistema.alterar_dificuldade([6], 0)


if __name__ == '__main__':
    unittest.main()
