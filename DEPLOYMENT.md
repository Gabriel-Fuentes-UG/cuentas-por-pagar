# 🚀 Guía de Deployment en Emergent

## Problema Detectado

Los endpoints devolvían 404 porque faltaba la configuración de la variable de entorno `REACT_APP_BACKEND_URL`.

## ✅ Solución Implementada

El código ahora usa un **fallback inteligente**:

```javascript
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || window.location.origin;
```

Esto significa que:
- ✅ Si existe `REACT_APP_BACKEND_URL`, la usa
- ✅ Si NO existe, usa `window.location.origin` (dominio actual)

## 📋 Configuración en Emergent

### Opción 1: Sin configurar variable de entorno (MÁS SIMPLE)

Si frontend y backend están en el mismo dominio (`porpagar.mx`):

1. ✅ **No necesitas configurar nada**
2. ✅ El código automáticamente usará `https://porpagar.mx`
3. ✅ Simplemente haz push a git y Emergent lo desplegará

### Opción 2: Configurar variable de entorno (EXPLÍCITO)

Si prefieres ser explícito o backend está en otro dominio:

1. Ve al panel de Emergent
2. Busca la sección **Environment Variables** o **Variables de Entorno**
3. Agrega:
   - **Nombre**: `REACT_APP_BACKEND_URL`
   - **Valor**: `https://porpagar.mx`
4. Guarda y redespliega

## 🔧 Variables de Entorno Requeridas

### Backend (.env)

```env
# MongoDB
MONGO_URL=mongodb://tu-mongodb-url
DB_NAME=cuentas_por_pagar

# Uploads
UPLOAD_DIR=/app/uploads

# JWT
JWT_SECRET_KEY=tu-clave-secreta-super-segura

# Google Gemini (para análisis de PDFs)
GOOGLE_API_KEY=tu-api-key-de-google
```

### Frontend (.env) - OPCIONAL

```env
# Solo si backend está en dominio diferente
REACT_APP_BACKEND_URL=https://porpagar.mx
```

## 📝 Pasos para Deployar

1. **Hacer commit de los cambios:**
   ```bash
   git add .
   git commit -m "Fix: Usar URL relativa como fallback en producción"
   git push origin main
   ```

2. **Emergent detectará el push** y automáticamente:
   - ✅ Clonará el repositorio
   - ✅ Instalará dependencias
   - ✅ Compilará el proyecto
   - ✅ Desplegará en `porpagar.mx`

3. **Verificar que funciona:**
   - Ir a https://porpagar.mx
   - Probar login
   - Verificar que los endpoints funcionen

## 🧪 Testing de Endpoints

Los siguientes endpoints ahora deberían funcionar:

✅ `GET /api/health` → 200 OK  
✅ `POST /api/auth/login` → 200 OK  
✅ `GET /api/empresas` → 200 OK  
✅ `GET /api/invoices/{empresa_id}` → 200 OK  
✅ `POST /api/upload-pdf/{empresa_id}` → 200 OK  
✅ `GET /api/invoices/{invoice_id}/download` → 200 OK  
✅ `GET /api/invoices/{invoice_id}/download-comprobante` → 200 OK  
✅ `GET /api/invoices/{invoice_id}/download-xml` → 200 OK  
✅ `GET /api/export/facturas-pendientes/{empresa_id}` → 200 OK  
✅ `GET /api/export/facturas-pagadas/{empresa_id}` → 200 OK  
✅ `GET /api/export/resumen-general/{empresa_id}` → 200 OK  

## 🔍 Debugging

Si sigues viendo errores:

1. **Abrir Chrome DevTools** (F12)
2. Ir a **Network** tab
3. Ver qué URL está llamando el frontend
4. Verificar la respuesta del servidor

### Comandos útiles para verificar:

```bash
# Verificar health endpoint
curl https://porpagar.mx/api/health

# Verificar con autenticación
curl -X POST https://porpagar.mx/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"MAURO","password":"Mauro123456"}'
```

## 📱 Usuarios de Prueba

- **Admin**: `MAURO` / `Mauro123456`
- **Admin**: `admin` / `admin123`
- **Solo lectura**: `contratos` / `SEDENA199156`

## 🆘 Soporte

Si el problema persiste:
1. Verifica los logs de Emergent
2. Confirma que las variables de entorno del backend están configuradas
3. Verifica que MongoDB esté accesible desde Emergent
