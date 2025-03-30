from dataclasses import fields
from datetime import timezone,datetime 
from flask_sqlalchemy import SQLAlchemy
import uuid
from marshmallow import fields, Schema 


# Inicialización de la base de datos con SQLAlchemy
db = SQLAlchemy()

class Blacklist(db.Model):
    """
    Modelo de base de datos que representa la lista negra de correos electrónicos.

    Atributos:
        id (str): Identificador único del registro en formato UUID.
        email (str): Dirección de correo electrónico bloqueada.
        app_uuid (str): Identificador de la aplicación que bloqueó el correo.
        blocked_reason (str, opcional): Razón por la cual el correo fue bloqueado.
        request_ip (str, opcional): Dirección IP desde la cual se realizó la solicitud.
        createdAt (datetime): Fecha y hora en que se creó el registro.
        updatedAt (datetime): Fecha y hora en que se actualizó el registro.
    """
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(), nullable=False)
    app_uuid = db.Column(db.String(), nullable=False)
    blocked_reason = db.Column(db.String(), nullable=True)
    request_ip = db.Column(db.String(), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def to_dict(self):
        """
        Convierte la instancia de Blacklist en un diccionario.

        Returns:
            dict: Representación en diccionario del objeto Blacklist.
        """
        return {
            'id': self.id,
            'email': self.email,
            'app_uuid': self.app_uuid,
            'blocked_reason': self.blocked_reason,
            'request_ip': self.request_ip,
            'createdAt': self.createdAt.isoformat(),
            'updatedAt': self.updatedAt.isoformat()
        }

class BlacklistJsonSchema(Schema):
    """
    Esquema de serialización para el modelo Blacklist usando Marshmallow.
    
    Define la estructura de datos para convertir instancias de Blacklist a formato JSON.
    """
    id = fields.Str()
    email = fields.Str()
    app_uuid = fields.Str()
    blocked_reason = fields.Str()
    request_ip = fields.Str()
    createdAt = fields.DateTime()
    updatedAt = fields.DateTime()
    
    def get_size(self, obj):
        """
        Método auxiliar para obtener el tamaño del objeto si existe.
        
        Args:
            obj: Instancia del objeto que contiene el atributo 'size'.
        
        Returns:
            str: Nombre del tamaño si el objeto tiene el atributo 'size', de lo contrario None.
        """
        return obj.size.name if obj.size else None