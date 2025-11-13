# Sistema de Gestión de Cuentas por Pagar

Sistema web para gestionar cuentas por pagar de múltiples empresas, con análisis automático de facturas XML y PDFs mediante IA.

## 🚀 Características

- ✅ **Multi-empresa**: Gestiona facturas de múltiples empresas desde un solo sistema
- ✅ **Carga de archivos**: PDF, XML y comprobantes de pago
- ✅ **Análisis automático**: Extracción de datos de facturas XML (CFDI México)
- ✅ **IA para comprobantes**: Análisis automático de PDFs de comprobantes usando Google Gemini
- ✅ **Control de pagos**: Estados pendiente/pagado con seguimiento
- ✅ **Reportes Excel**: Exportación de facturas y resúmenes
- ✅ **Autenticación**: JWT con roles (admin/readonly)
- ✅ **Multi-proveedor**: Agrupa y resume por proveedor

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** (Python 3.8+)
- **MongoDB** (Base de datos NoSQL)
- **Google Gemini AI** (Análisis de PDFs)
- **JWT** (Autenticación)

### Frontend
- **React** 18
- **Tailwind CSS** + **shadcn/ui**
- **Axios** (HTTP client)
- **React Router** (Navegación)

## 📋 Requisitos Previos

- Python 3.8 o superior
- Node.js 16+ y npm/yarn
- MongoDB (local o Atlas)
- Cuenta de Google Cloud con API de Gemini habilitada

## 🔧 Instalación y Desarrollo Local

### 1. Backend

```powershell
# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# o
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales

# Iniciar servidor de desarrollo
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend

```powershell
# En otra terminal, navegar a frontend
cd frontend

# Instalar dependencias
npm install
# o
yarn install

# Configurar variables de entorno (OPCIONAL)
copy .env.example .env

# Iniciar servidor de desarrollo
npm start
# o
yarn start
```

### 3. Acceder a la aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/api/health

## 🔑 Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `MAURO` | `Mauro123456` | Admin |
| `admin` | `admin123` | Admin |
| `contratos` | `SEDENA199156` | Solo lectura |

## 🌐 Deployment en Producción

Ver [DEPLOYMENT.md](./DEPLOYMENT.md) para instrucciones detalladas de deployment en Emergent u otras plataformas.

### Variables de Entorno Requeridas

#### Backend (.env)
```env
MONGO_URL=mongodb://tu-mongodb-url
DB_NAME=cuentas_por_pagar
UPLOAD_DIR=/app/uploads
JWT_SECRET_KEY=tu-clave-secreta-super-segura
GOOGLE_API_KEY=tu-google-gemini-api-key
```

#### Frontend (.env) - OPCIONAL
```env
# Solo necesario si backend está en dominio diferente
REACT_APP_BACKEND_URL=https://tu-dominio.com
```

## 🧪 Testing

### Verificar todos los endpoints:
```bash
# Instalar requests si no lo tienes
pip install requests

# Ejecutar script de verificación
python verify_endpoints.py https://porpagar.mx
```

### Tests unitarios:
```bash
# Backend
pytest

# Tests específicos incluidos en el repo:
python backend_test.py
python test_comprobante_workflow.py
```

## 📁 Estructura del Proyecto

```
cuentas-por-pagar/
├── backend/
│   ├── server.py              # API principal
│   ├── export_utils.py        # Utilidades para Excel
│   ├── requirements.txt       # Dependencias Python
│   └── .env                   # Variables de entorno (no en git)
├── frontend/
│   ├── src/
│   │   ├── App.js            # Componente principal
│   │   ├── components/       # Componentes UI
│   │   ├── contexts/         # Context API (Auth)
│   │   └── hooks/            # Hooks personalizados
│   ├── package.json
│   └── .env                  # Variables de entorno (no en git)
├── uploads/                  # Archivos subidos (PDF, XML)
├── tests/                    # Tests automatizados
├── DEPLOYMENT.md            # Guía de deployment
└── verify_endpoints.py      # Script de verificación
```

## 📚 Documentación API

La documentación completa de la API está disponible en:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints Principales

#### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Información del usuario actual
- `POST /api/auth/logout` - Cerrar sesión

#### Empresas
- `GET /api/empresas` - Listar empresas
- `POST /api/empresas` - Crear empresa
- `PUT /api/empresas/{id}` - Actualizar empresa
- `DELETE /api/empresas/{id}` - Eliminar empresa

#### Facturas
- `GET /api/invoices/{empresa_id}` - Listar facturas de una empresa
- `POST /api/upload-pdf/{empresa_id}` - Subir factura PDF
- `PUT /api/invoices/{invoice_id}` - Actualizar estado de pago
- `DELETE /api/invoices/{invoice_id}` - Eliminar factura

#### Descargas
- `GET /api/invoices/{invoice_id}/download` - Descargar PDF
- `GET /api/invoices/{invoice_id}/download-xml` - Descargar XML
- `GET /api/invoices/{invoice_id}/download-comprobante` - Descargar comprobante

#### Reportes
- `GET /api/resumen/{empresa_id}` - Resumen general
- `GET /api/estado-cuenta-pagadas/{empresa_id}` - Estado de cuenta pagadas
- `GET /api/export/facturas-pendientes/{empresa_id}` - Exportar pendientes (Excel)
- `GET /api/export/facturas-pagadas/{empresa_id}` - Exportar pagadas (Excel)
- `GET /api/export/resumen-general/{empresa_id}` - Exportar resumen (Excel)

## 🐛 Troubleshooting

### Backend no inicia
- Verifica que MongoDB esté corriendo
- Verifica las variables de entorno en `.env`
- Verifica que el puerto 8000 esté disponible

### Frontend no se conecta al backend
- Verifica que `REACT_APP_BACKEND_URL` esté configurado correctamente
- En desarrollo: debe ser `http://localhost:8000`
- En producción: debe ser tu dominio o vacío para usar URL relativa

### Errores 404 en producción
- Asegúrate de hacer commit y push de los últimos cambios
- Verifica que Emergent haya desplegado correctamente
- Ejecuta `python verify_endpoints.py https://tu-dominio.com`

### Problemas con uploads
- Verifica que la carpeta `uploads/` tenga permisos de escritura
- En producción, asegúrate de que `UPLOAD_DIR` esté configurado correctamente

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es privado y propietario.

## 📞 Soporte

Para soporte, contacta al equipo de desarrollo o abre un issue en el repositorio.
