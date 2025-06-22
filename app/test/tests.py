import unittest
from unittest.mock import patch, MagicMock
from app import app, obtener_conexion

class TestBibliotecaApp(unittest.TestCase):

    def setUp(self):
        # Configura el entorno de prueba
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.mysql.connector.connect')
    def test_obtener_conexion_exitoso(self, mock_connect):
        mock_connect.return_value = MagicMock()
        conexion = obtener_conexion()
        self.assertIsNotNone(conexion)
        mock_connect.assert_called_once()

    @patch('app.obtener_conexion')
    def test_inicio_ruta(self, mock_conexion):
        # Mockea cursor y fetchall()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("ID", "Libro 1", "Autor 1", "Categoría", 3)]
        mock_conexion.return_value.cursor.return_value = mock_cursor

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Libro 1", response.data)

    @patch('app.obtener_conexion')
    def test_agregar_post(self, mock_conexion):
        mock_cursor = MagicMock()
        mock_conexion.return_value.cursor.return_value = mock_cursor

        response = self.app.post('/agregar', data={
            'titulo': 'Test',
            'autor': 'Tester',
            'categoria': 'Pruebas',
            'cantidad': 1
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        mock_cursor.execute.assert_called()

if __name__ == '__main__':
    unittest.main()
