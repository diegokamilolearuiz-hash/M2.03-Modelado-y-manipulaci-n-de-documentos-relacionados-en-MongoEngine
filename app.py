from mongoengine import Document, StringField, IntField, connect, DateTimeField, ReferenceField, ListField
from datetime import datetime

# Conexión CORREGIDA - usa tlsAllowInvalidCertificates
connection_string = "mongodb+srv://diegoolea:koki1505@cluster1.n6ei9ex.mongodb.net/articulos?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

try:
    connect(db="articulos", host=connection_string)
    print("✅ Conectado a MongoDB Atlas correctamente")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    exit(1)

# Modelo User
class User(Document):
    email = StringField(required=True, unique=True)
    nombre = StringField(required=True)
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'users'}

# Modelo Artículo
class Articulo(Document):
    nombre = StringField(required=True, max_length=100)
    descripcion = StringField(max_length=500)
    marca = StringField(max_length=50)
    usuario_modifico = ReferenceField(User, required=True)
    user = User
    tags = ListField(StringField(max_length=50))
    fecha_creacion = DateTimeField(default=datetime.utcnow)
    fecha_modificacion = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'articulos',
        'indexes': ['nombre', 'marca', 'tags']
    }

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

# Función para gestionar usuario
def obtener_o_crear_usuario(email="admin@empresa.com", nombre="Administrador"):
    try:
        usuario = User.objects(email=email).first()
        if usuario:
            print(f"✅ Usuario encontrado: {usuario.nombre}")
            return usuario
        else:
            nuevo_usuario = User(email=email, nombre=nombre)
            nuevo_usuario.save()
            print(f"✅ Nuevo usuario creado: {nuevo_usuario.nombre}")
            return nuevo_usuario
    except Exception as e:
        print(f"❌ Error con usuario: {e}")
        return None

# Función principal
def main():
    print("🚀 Iniciando aplicación de Gestión de Artículos")
    print("=" * 50)
    
    print("\n1. Verificando usuario...")
    usuario = obtener_o_crear_usuario(
        email="diego@empresa.com", 
        nombre="Diego Kamilo"
    )
    
    if not usuario:
        print("❌ No se pudo obtener/crear el usuario")
        return
    
    print("\n2. Creando artículo...")
    try:
        articulo = Articulo(
            nombre="Laptop Gaming ASUS",
            descripcion="Laptop para juegos de alta gama",
            marca="ASUS",
            usuario_modifico=usuario,
            tags=["tecnologia", "gaming", "computacion"]
        )
        articulo.save()
        print(f"✅ Artículo creado: {articulo.nombre}")
    except Exception as e:
        print(f"❌ Error creando artículo: {e}")
        return
    
    print("\n3. Consultando artículos...")
    articulos = Articulo.objects(usuario_modifico=usuario)
    
    print(f"\n📦 Artículos de {usuario.nombre}:")
    for art in articulos:
        print(f"   • {art.nombre} - {art.marca}")
        print(f"     Tags: {', '.join(art.tags)}")
        print(f"     Creado: {art.fecha_creacion.strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()