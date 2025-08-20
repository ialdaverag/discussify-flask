# 🔔 Discussify Notification System

Sistema de notificaciones en tiempo real para Discussify Flask que combina WebSockets para entrega inmediata con almacenamiento persistente en base de datos.

## ✨ Características

- **🚀 Tiempo Real**: Notificaciones inmediatas via WebSockets
- **💾 Persistencia**: Almacenamiento en base de datos 
- **🔐 Seguridad**: Autenticación JWT
- **📱 API REST**: Endpoints completos para gestión
- **⚡ Eventos Automáticos**: Notificaciones automáticas para acciones de usuario

## 🎯 Tipos de Notificaciones

| Tipo | Descripción | Trigger |
|------|-------------|---------|
| `follow` | Usuario te sigue | Al crear Follow |
| `comment` | Comentario en tu post | Al crear Comment |
| `reply` | Respuesta a tu comentario | Al crear Comment reply |
| `community_join` | Usuario se une a tu comunidad | Al crear CommunitySubscriber |

## 🌐 API Endpoints

```http
GET    /notification/              # Obtener notificaciones paginadas
GET    /notification/unread-count  # Contador de no leídas
PATCH  /notification/{id}/read     # Marcar como leída
PATCH  /notification/mark-all-read # Marcar todas como leídas
DELETE /notification/{id}          # Eliminar notificación
```

## ⚡ Eventos WebSocket

```javascript
// Conexión con autenticación JWT
socket.auth = { token: 'your-jwt-token' };

// Escuchar nuevas notificaciones
socket.on('new_notification', (notification) => {
    console.log('Nueva notificación:', notification);
});
```

## 🚀 Uso Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
python run_with_notifications.py
```

### 3. Probar WebSockets

Abre `notification_demo.html` en tu navegador para probar la funcionalidad en tiempo real.

## 💻 Ejemplos de Código

### Crear Notificación Programática

```python
from app.managers.notification import NotificationManager

notification = NotificationManager.create_notification(
    title="Nueva Notificación",
    message="Este es un mensaje de prueba",
    notification_type='follow',
    user_id=123,  # destinatario
    sender_id=456  # quien la triggea
)
```

### Notificaciones Automáticas

```python
# Las notificaciones se crean automáticamente
from app.models.user import Follow

follow = Follow(follower_id=456, followed_id=123)
follow.save()  # Esto triggea automáticamente una notificación
```

### Cliente WebSocket

```javascript
const socket = io('http://localhost:5000');

socket.auth = { token: localStorage.getItem('jwt_token') };
socket.connect();

socket.on('new_notification', (notification) => {
    // Actualizar UI con nueva notificación
    showNotification(notification);
});
```

### Llamadas API

```bash
# Obtener notificaciones
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/notification/

# Marcar como leída
curl -X PATCH \
     -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/notification/123/read

# Contador de no leídas
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/notification/unread-count
```

## 💾 Esquema de Base de Datos

```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES users(id),
    sender_id INTEGER REFERENCES users(id),
    post_id INTEGER REFERENCES posts(id),
    comment_id INTEGER REFERENCES comments(id),
    community_id INTEGER REFERENCES communities(id)
);
```

## 🔧 Configuración

### Variables de Entorno

```bash
DATABASE_URI=sqlite:///discussify.db
FLASK_ENV=development
```

### Configuración CORS para WebSockets

```python
socketio = SocketIO(
    cors_allowed_origins="*",  # Configurar para producción
    async_mode='threading'
)
```

## 📋 Estructura del Proyecto

```
app/
├── models/
│   └── notification.py        # Modelo de notificaciones
├── managers/
│   └── notification.py        # Lógica de negocio
├── routes/
│   └── notification.py        # API endpoints
├── schemas/
│   └── notification.py        # Serialización
├── events/
│   └── socket_events.py       # Eventos WebSocket
└── extensions/
    └── socketio.py            # Configuración SocketIO
```

## 🧪 Testing

### Ejecutar Pruebas

```bash
python /tmp/notification_demo.py  # Demo del sistema
```

### Demo Interactivo

1. Inicia la aplicación: `python run_with_notifications.py`
2. Abre `notification_demo.html` en tu navegador
3. Obtén un token JWT haciendo login via API
4. Conecta y prueba las notificaciones

## 🔒 Seguridad

- **Autenticación JWT**: Todas las conexiones requieren token válido
- **Autorización**: Los usuarios solo ven sus propias notificaciones
- **Validación**: Todos los inputs son validados
- **Salas de Usuario**: WebSockets usan salas específicas por usuario

## 🚀 Próximos Pasos

1. **Migraciones**: Ejecutar migraciones para crear tabla de notificaciones
2. **Configuración**: Ajustar CORS y configuración para producción
3. **Preferencias**: Implementar configuración de notificaciones por usuario
4. **Push Notifications**: Integrar notificaciones push para móviles
5. **Analytics**: Métricas de entrega y engagement

## 📞 Soporte

El sistema está listo para usar y proporciona tanto entrega en tiempo real via WebSockets como almacenamiento persistente en base de datos.

**¡Disfruta del nuevo sistema de notificaciones! 🎉**