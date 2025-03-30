import unittest
import os
from flask import Flask
from application import application
import json
from flask_sqlalchemy import SQLAlchemy

# Configuración de base de datos de prueba
os.environ['DATABASE'] = 'sqlite:///test_blacklists.db'

class TestBlacklistsOperations(unittest.TestCase):
    """
    Clase de pruebas unitarias para las operaciones de la lista negra en la API.

    Métodos:
        test_blacklists_add_without_token():
            Verifica que no se puede agregar un email a la blacklist sin un token de autorización.

        test_blacklists_add_email_success():
            Verifica que se puede agregar un email a la blacklist exitosamente con un token válido.

        test_blacklists_add_without_email():
            Verifica que no se puede agregar una entrada a la blacklist si no se proporciona un email.

        test_blacklists_add_without_app_uuid():
            Verifica que no se puede agregar una entrada a la blacklist si no se proporciona un app_uuid.

        test_blacklists_add_invalid_app_uuid():
            Verifica que no se puede agregar una entrada a la blacklist si el app_uuid no es válido.

        test_blacklists_add_invalid_blocked_reason():
            Verifica que no se puede agregar una entrada a la blacklist si el mensaje de bloqueo excede los 255 caracteres.

        test_blacklists_get_email_without_token():
            Verifica que no se puede consultar la blacklist sin un token de autorización.

        test_blacklists_get_email_success():
            Verifica que se puede consultar la blacklist correctamente cuando el email está bloqueado.

        test_blacklists_get_email_failed():
            Verifica que la respuesta indica correctamente cuando un email no está en la blacklist.
    """

    def test_blacklists_add_without_token(self):
        """
        Prueba que verifica que la API devuelve un error 401 (Unauthorized)
        cuando se intenta agregar un email a la blacklist sin un token de autorización.
        """
        with application.test_client() as test_client:
            response = test_client.post('/blacklists',
                                        json={
                                            "email": "laura@uniandes.edu.co",
                                            "app_uuid": "08043ed9-6823-426b-9900-e431e1d744f8",
                                            "blocked_reason": "This user is PEP"
                                        })

            assert response.status_code == 401
            assert response.get_json()['error'] == 'Unauthorized'

    def test_blacklists_add_email_success(self):
        """
        Prueba que verifica que se puede agregar un email a la blacklist exitosamente
        cuando se proporciona un token válido.
        """
        with application.test_client() as test_client:
            response = test_client.post('/blacklists',
                                        json={
                                            'email': 'laura@uniandes.edu.co',
                                            'app_uuid': '08043ed9-6823-426b-9900-e431e1d744f8',
                                            'blocked_reason': 'This user is PEP'
                                        },
                                        headers={'Authorization': f'Bearer {os.environ["TOKEN"]}'})

            assert response.status_code == 200
            assert response.get_json()['msg'] == 'Email agregado a la blacklist'

    def test_blacklists_add_without_email(self):
        """
        Prueba que verifica que la API devuelve un error 400 cuando no se proporciona un email.
        """
        with application.test_client() as test_client:
            response = test_client.post('/blacklists',
                                        headers={'Authorization': f'Bearer {os.environ["TOKEN"]}'},
                                        json={
                                            "app_uuid": "08043ed9-6823-426b-9900-e431e1d744f8",
                                            "blocked_reason": "This user is PEP"
                                        })

            assert response.status_code == 400
            assert response.get_json()['error'] == 'Email y app_uuid son obligatorios'

    def test_blacklists_add_without_app_uuid(self):
        """
        Prueba que verifica que la API devuelve un error 400 cuando no se proporciona un app_uuid.
        """
        with application.test_client() as test_client:
            response = test_client.post('/blacklists',
                                        headers={'Authorization': f'Bearer {os.environ["TOKEN"]}'},
                                        json={
                                            "email": "laura@uniandes.edu.co",
                                            "blocked_reason": "This user is PEP"
                                        })

            assert response.status_code == 400
            assert response.get_json()['error'] == 'Email y app_uuid son obligatorios'

    def test_blacklists_add_invalid_app_uuid(self):
        """
        Prueba que verifica que la API devuelve un error 400 cuando el app_uuid no es un UUID válido.
        """
        with application.test_client() as test_client:
            response = test_client.post('/blacklists',
                                        headers={'Authorization': f'Bearer {os.environ["TOKEN"]}'},
                                        json={
                                            "email": "laura@uniandes.edu.co",
                                            "app_uuid": "08",
                                            "blocked_reason": "This user is PEP"
                                        })

            assert response.status_code == 400
            assert response.get_json()['error'] == 'app_uuid no es un uuid válido'

    def test_blacklists_add_invalid_blocked_reason(self):
        """
        Prueba que verifica que la API devuelve un error 400 cuando el campo blocked_reason
        excede los 255 caracteres.
        """
        with application.test_client() as test_client:
            response = test_client.post('/blacklists',
                                        headers={'Authorization': f'Bearer {os.environ["TOKEN"]}'},
                                        json={
                                            "email": "juan@uniandes.edu.co",
                                            "app_uuid": "08043ed9-6823-426b-9900-e431e1d744f8",
                                            "blocked_reason": "Lorem Ipsum" * 100  # Excede 255 caracteres
                                        })

            assert response.status_code == 400
            assert response.get_json()['error'] == 'blocked_reason debe tener máximo 255 caracteres'

    def test_blacklists_get_email_without_token(self):
        """
        Prueba que verifica que la API devuelve un error 401 cuando se consulta un email en la blacklist sin un token de autorización.
        """
        with application.test_client() as test_client:
            response = test_client.get(f'/blacklists/j@hotmail.com')

            assert response.status_code == 401
            assert response.get_json()['error'] == 'Unauthorized'

    def test_blacklists_get_email_success(self):
        """
        Prueba que verifica que la API devuelve una respuesta exitosa cuando el email está en la blacklist.
        """
        with application.test_client() as test_client:
            responseAdd = test_client.post('/blacklists',
                                           headers={'Authorization': f'Bearer {os.environ["TOKEN"]}'},
                                           json={
                                               "email": "laura@uniandes.edu.co",
                                               "app_uuid": "08043ed9-6823-426b-9900-e431e1d744f8",
                                               "blocked_reason": "This user is PEP"
                                           })
            response_json = json.loads(responseAdd.data)

            response = test_client.get(f'/blacklists/{response_json["blacklist"]["email"]}',
                                       headers={'Authorization': f'Bearer {os.environ["TOKEN"]}'})

            assert response.status_code == 200
            assert response.get_json()['is_blacklisted'] == True

    def test_blacklists_get_email_failed(self):
        """
        Prueba que verifica que la API devuelve una respuesta indicando que el email no está en la blacklist.
        """
        with application.test_client() as test_client:
            response = test_client.get(f'/blacklists/j@hotmail.com',
                                       headers={'Authorization': f'Bearer token'})  # Token inválido

            assert response.status_code == 200
            assert response.get_json()['is_blacklisted'] == False
