import unittest
from unittest.mock import patch, MagicMock
from app import create_app

class BibliotecaUnitTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    @patch('app.routes.obtener_conexion')
    def test_inicio_sin_bd(self, mock_conexion):
        # Simula resultados falsos de la base de datos
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "El Principito", "Antoine de Saint-Exupéry", "Fábula", 3)
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_conexion.return_value = mock_conn

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'El Principito', response.data)

    @patch('app.routes.obtener_conexion')
    def test_agregar_get(self, mock_conexion):
        response = self.app.get('/agregar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Agregar Nuevo Libro', response.data)

