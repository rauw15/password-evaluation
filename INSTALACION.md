# Instalación Rápida - API de Evaluación de Contraseñas

## Requisitos Previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación en 3 Pasos

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la API
```bash
python run.py
```

### 3. Probar la API
```bash
# En otra terminal
python test_api.py
```

## Comandos Útiles

### Iniciar con opciones personalizadas
```bash
# Modo debug
python run.py --debug

# Puerto personalizado
python run.py --port 8000

# Ver demostración
python run.py --demo

# Ejecutar pruebas
python run.py --test
```

### Probar manualmente con curl
```bash
# Evaluar contraseña
curl -X POST http://localhost:5000/api/v1/password/evaluate \
  -H "Content-Type: application/json" \
  -d '{"password": "MiContraseña123!"}'

# Health check
curl http://localhost:5000/api/v1/health
```

## Estructura del Proyecto
```
C2 - A3 - Evaluacion de contraseñas/
├── app.py                    # Aplicación principal
├── run.py                    # Script de inicio
├── config.py                 # Configuración
├── demo.py                   # Demostración de cálculo
├── test_api.py              # Pruebas automáticas
├── requirements.txt         # Dependencias
├── README.md               # Documentación completa
├── INSTALACION.md          # Este archivo
└── 1millionPasswords.csv   # Base de datos de contraseñas comunes
```

## Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "No se encontró el archivo '1millionPasswords.csv'"
- Verifique que el archivo esté en el directorio raíz del proyecto
- La API funcionará sin él, pero no verificará contraseñas comunes

### Puerto ya en uso
```bash
python run.py --port 8000
```

### Problemas de permisos en Windows
```bash
# Ejecutar PowerShell como administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Verificación de Instalación

1. **Iniciar la API:**
   ```bash
   python run.py
   ```

2. **Verificar que responde:**
   - Abrir navegador en `http://localhost:5000`
   - Debe mostrar información de la API

3. **Ejecutar pruebas:**
   ```bash
   python test_api.py
   ```

## Siguiente Paso
Lea el `README.md` para documentación completa y ejemplos de uso avanzado.
