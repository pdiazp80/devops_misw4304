class ApiError(Exception):
    """
    Clase base para errores personalizados en la API.

    Atributos:
        code (int): Código de estado HTTP asociado al error. 
                    Por defecto, 422 (Unprocessable Entity).
        description (str): Mensaje de error predeterminado.

    Métodos:
        __init__(self, description=None, code=None):
            Inicializa una instancia de ApiError con un mensaje y un código opcional.
    """

    code = 422  # Código de estado HTTP predeterminado
    description = "Default message"  # Mensaje de error predeterminado

    def __init__(self, description=None, code=None):
        """
        Inicializa la instancia del error con un mensaje y código opcional.

        Parámetros:
            description (str, opcional): Mensaje de error personalizado. 
                                         Si no se proporciona, se usa el predeterminado.
            code (int, opcional): Código de estado HTTP personalizado. 
                                  Si no se proporciona, se usa el predeterminado.
        """
        if description:
            self.description = description
        if code:
            self.code = code

        super().__init__(self.description)
