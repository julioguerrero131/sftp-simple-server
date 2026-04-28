import asyncio
import asyncssh

# python main.py

# 1. Configuración de autenticación
class ServidorSSHLocal(asyncssh.SSHServer):
    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        # Aquí defines tus credenciales locales
        return username == 'admin' and password == '1234'

async def iniciar_servidor():
    # 2. Generamos una clave RSA temporal para el servidor
    server_key = asyncssh.generate_private_key('ssh-rsa')
    
    puerto = 8022
    host = '127.0.0.1'

    print(f"🚀 Iniciando servidor SFTP local...")
    print(f"👉 Conéctate a: sftp://{host}:{puerto}")
    print(f"👤 Usuario: admin")
    print(f"🔑 Contraseña: 1234")
    print(f"Presiona Ctrl+C para detener el servidor.\n")

    # 3. Levantamos el servidor
    await asyncssh.listen(
        host=host,
        port=puerto,
        server_host_keys=[server_key],
        server_factory=ServidorSSHLocal,
        sftp_factory=asyncssh.SFTPServer # Esto habilita el subsistema SFTP
    )
    
    # Mantiene el servidor corriendo indefinidamente
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(iniciar_servidor())
    except (OSError, asyncssh.Error) as exc:
        print(f"Error al iniciar el servidor: {exc}")
    except KeyboardInterrupt:
        print("\nServidor detenido.")