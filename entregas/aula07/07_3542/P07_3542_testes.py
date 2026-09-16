import unittest
from P07_3542_labirinto import Labirinto


class TesteLabirinto(unittest.TestCase):
    def setUp(self):
        self.lab = Labirinto(11, 11)
        self.lab.gerar_dfs_iterativo()

    def test_inicio_e_queijo_posicionados(self):
        self.assertEqual(self.lab.grid[1][1], "P")
        self.assertEqual(self.lab.grid[self.lab.altura - 2][self.lab.largura - 2], "Q")

    def test_existencia_caminho(self):
        caminho = self.lab.encontrar_caminho()
        self.assertTrue(len(caminho) > 0)
        self.assertEqual(caminho[0], (1, 1))
        self.assertEqual(caminho[-1], (self.lab.largura - 2, self.lab.altura - 2))

    def test_continuidade_caminho(self):
        caminho = self.lab.encontrar_caminho()
        for i in range(len(caminho) - 1):
            x1, y1 = caminho[i]
            x2, y2 = caminho[i + 1]
            distancia = abs(x1 - x2) + abs(y1 - y2)
            self.assertEqual(distancia, 1)


if __name__ == "__main__":
    unittest.main()