import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestBibliotecaApp(unittest.TestCase):

    def setUp(self):
        # Configura el cliente de pruebas de Flask
        self.client = app.test_client()
        self.client.testing = True

    @patch('app.mysql.connector.connect')
    def test_inicio_devuelve_lista_de_libros(self, mock_connect):
        # Simula una conexión y un cursor con datos ficticios
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, 'Cien años de soledad', 'Gabriel García Márquez', 'Novela', 3),
            (2, '1984', 'George Orwell', 'Distopía', 5)
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cien a\xc3\xb1os de soledad', response.data)
        self.assertIn(b'1984', response.data)

    @patch('app.mysql.connector.connect')
    def test_agregar_libro_post_redirecciona(self, mock_connect):
        # Mocks para insertar libro
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/agregar', data={
            'titulo': 'Nuevo Libro',
            'autor': 'Autor Prueba',
            'categoria': 'Test',
            'cantidad': 10
        })

        self.assertEqual(response.status_code, 302)  # Redirecciona
        self.assertEqual(response.location, '/')

    def test_agregar_libro_get_muestra_formulario(self):
        response = self.client.get('/agregar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Agregar', response.data)

if __name__ == '__main__':
    unittest.main()
