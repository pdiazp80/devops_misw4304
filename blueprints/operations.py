from flask import request, jsonify, Response, Blueprint
from models.model import db,Blacklist, BlacklistJsonSchema
from uuid import UUID
from dotenv import load_dotenv
import os


# Cargar variables de entorno
load_dotenv()

# Crear un blueprint para las operaciones relacionadas con la blacklist
operations_blueprint = Blueprint('operations', __name__)

# Token de autenticación desde las variables de entorno
AUTH_TOKEN = os.environ['TOKEN']

@operations_blueprint.route('/blacklists/ping', methods=['GET'])
def health_check():
    """
    Verifica que el servicio esté activo.
    
    Returns:
        Response: 'pong' con código de estado 200.
    """
    return Response('pong', status=200)


def verify_token():
    """
    Verifica que el token de autenticación proporcionado en el header 'Authorization' sea válido.
    
    Returns:
        bool: True si el token es válido, False en caso contrario.
    """
    token = request.headers.get('Authorization')
    if token is not None:
        token = token.split(" ")[-1]  # Extraer el token real eliminando el prefijo "Bearer"
        if token == AUTH_TOKEN:
            return True
    return False


@operations_blueprint.route('/blacklists/<string:email>', methods=['GET'])
def blacklist_by_id(email):
    """
    Verifica si un email está en la lista negra.
    
    Args:
        email (str): Dirección de correo electrónico a verificar.
    
    Returns:
        Response: JSON con la información de si el email está en la lista negra o no.
    """
    if not verify_token():
        return jsonify({"error": "Unauthorized"}), 401

    blacklist = db.session.query(Blacklist).filter_by(email=email).first()
    if not blacklist:
        return jsonify({"is_blacklisted": False}), 200

    return jsonify({"is_blacklisted": True, "blocked_reason": blacklist.blocked_reason}), 200



@operations_blueprint.route('/blacklists', methods=['POST'])
def blacklist():
    """
    Agrega un email a la lista negra (blacklist).
    
    Returns:
        Response: JSON con el resultado de la operación.
    """
    if not verify_token():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    email = data.get('email')
    app_uuid = data.get('app_uuid')
    blocked_reason = data.get('blocked_reason')
    request_ip = request.remote_addr  # Obtener la IP del usuario

    # Validaciones de los datos
    if not email or not app_uuid:
        return jsonify({"error": "Email y app_uuid son obligatorios"}), 400

    if not is_valid_uuid(app_uuid):
        return jsonify({"error": "app_uuid no es un uuid válido"}), 400

    if blocked_reason and len(blocked_reason) > 255:
        return jsonify({"error": "blocked_reason debe tener máximo 255 caracteres"}), 400

    try:
        # Crear y almacenar el nuevo registro en la base de datos
        new_post = Blacklist(email=email, app_uuid=app_uuid, blocked_reason=blocked_reason, request_ip=request_ip)
        db.session.add(new_post)
        db.session.commit()
        return {"msg": "Email agregado a la blacklist", "blacklist": BlacklistJsonSchema().dump(new_post)}, 200
    except Exception as error:
        return jsonify({"error": "Error agregando email a blacklist", "details": str(error)}), 400




def is_valid_uuid(uuid_str):
    """
    Verifica si una cadena de texto es un UUID válido versión 4.
    
    Args:
        uuid_str (str): La cadena que se desea validar.
    
    Returns:
        bool: True si la cadena es un UUID válido, False en caso contrario.
    """
    try:
        UUID(uuid_str, version=4)
        return True
    except ValueError:
        return False