
class Instruction:

    def __init__(self) -> None:
        pass

    def no_internet_service(self):
        general_response = '''Descubre cómo restablecer la conexión a internet, realizando una serie de sencillos pasos.
            1. Verifica que estás conectado a la red de la ONT o módem
            Si tu conexión es por Wi-Fi, válida que efectivamente estés conectado a tu red y no a una red Wi-Fi distinta. En caso de estar conectado a otra red, conéctate a la red Wi-Fi de tu módem y revisa el servicio de internet. Si el problema persiste, continúa con el siguiente paso.
            Nota: En caso de que no encuentres tu red de Wi-Fi ingresa aquí para conocer como puedes restablecer tu Wi-Fi.
            Si estás conectado por cable de red o cable ethernet, asegúrate que el cable esté en buenas condiciones (no esté roto, doblado, no tenga rasgaduras, etc.). Si te es posible, cambia el cable de red.
            Si no tienes otro cable de red o cable ethernet, invierte la conexión de las puntas del cable, es decir, la punta que está conectada al módem ahora conéctala a tu dispositivo y viceversa. Posteriormente, revisa el servicio de internet. Si el problema persiste, continúa con el siguiente paso.
            2. Desconecta la ONT o módem de la alimentación eléctrica, espera 30 segundos, vuelve a conectar y una vez que todos los leds del equipo enciendan, comprueba que ya cuentes con servicio de internet, si el problema persiste, continúa con el siguiente paso.
            3. Por último, aplica un reinicio a valores de fábrica, a la ONT o al módem. Con la ayuda de un objeto con punta fina presiona el orificio que dice reset durante 30 segundos, el equipo se apagará y encenderá de forma automática. Comprueba que ya cuentes con servicio de internet. De continuar con el problema te pedimos contactar con soporte a clientes.'''
        
        return general_response