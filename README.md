# API de Evaluación de Contraseñas

## Materia: Seguridad de la Información

### Objetivo
Desarrollar y comprender los mecanismos de evaluación de la fuerza de una contraseña mediante el cálculo de la entropía.

### Concepto Clave: Entropía de una Contraseña

La entropía (E) en ciberseguridad es una medida de la imprevisibilidad o aleatoriedad de una contraseña, expresada en bits. Cuanto mayor es el valor de la entropía, mayor es la incertidumbre y, por lo tanto, más intentos de fuerza bruta se requieren para adivinarla.

**Fórmula:** E = L × log₂(N)

Donde:
- **L**: Longitud de la contraseña (número de caracteres)
- **N**: Tamaño del Alfabeto (keyspace) - suma de todos los tipos de caracteres únicos posibles
- **log₂**: Logaritmo en base 2

### Categorías de Fuerza

| Entropía (bits) | Fuerza Estimada |
|----------------|----------------|
| 0 a 60 bits    | Débil o Aceptable (crackeable en horas/días) |
| 60 a 80 bits   | Fuerte |
| 80+ bits       | Muy Fuerte (Estándar de seguridad moderna) |

## Instalación y Configuración

### Requisitos
- Python 3.7+
- pip

### Instalación
```bash
# Clonar o descargar el proyecto
cd "C2 - A3 - Evaluacion de contraseñas"

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

La API estará disponible en `http://localhost:5000`

## Endpoints

### 1. Evaluar Contraseña
**POST** `/api/v1/password/evaluate`

Evalúa la fuerza de una contraseña calculando su entropía y proporcionando recomendaciones.

#### Request Body
```json
{
    "password": "MiContraseña123!"
}
```

#### Response
```json
{
    "password_length": 16,
    "alphabet_size": 94,
    "entropia_bits": 105.36,
    "strength_evaluation": {
        "strength_category": "Muy Fuerte",
        "security_level": "Alta",
        "is_common_password": false,
        "entropia_after_penalties": 105.36,
        "time_to_crack": "4.01e+20 años",
        "recommendations": [
            "Excelente! Su contraseña cumple con los estándares de seguridad"
        ]
    }
}
```

### 2. Health Check
**GET** `/api/v1/health`

Verifica el estado de la API.

#### Response
```json
{
    "status": "healthy",
    "service": "Password Evaluation API",
    "version": "1.0.0"
}
```

### 3. Información General
**GET** `/`

Proporciona información básica sobre la API.

## Características Implementadas

### ✅ Funciones Base
- `calculate_L(password)`: Calcula la longitud de la contraseña
- `calculate_N(password)`: Calcula el tamaño del alfabeto basado en tipos de caracteres
- `calculate_entropy(password)`: Implementa la fórmula E = L × log₂(N)

### ✅ Evaluación de Calidad
- Categorización de fuerza basada en entropía
- Verificación contra diccionario de 1 millón de contraseñas comunes
- Cálculo del tiempo estimado de crackeo (asumiendo 10¹¹ intentos/segundo)
- Sistema de penalizaciones para contraseñas predecibles

### ✅ Seguridad
- **Cero Persistencia**: No se almacenan ni registran las contraseñas
- Validación de entrada robusta
- Manejo seguro de errores
- Logging sin exposición de datos sensibles

### ✅ Alfabeto Calculado
- **Minúsculas (a-z)**: 26 caracteres
- **Mayúsculas (A-Z)**: 26 caracteres  
- **Números (0-9)**: 10 caracteres
- **Símbolos**: 32 caracteres comunes (~!@#$%^&*()_+-=[]{}|;:,.<>?)

## Ejemplos de Uso

### Contraseña Débil
```bash
curl -X POST http://localhost:5000/api/v1/password/evaluate \
  -H "Content-Type: application/json" \
  -d '{"password": "123456"}'
```

### Contraseña Fuerte
```bash
curl -X POST http://localhost:5000/api/v1/password/evaluate \
  -H "Content-Type: application/json" \
  -d '{"password": "MiContraseña123!@#"}'
```

## Implementación Técnica

### Arquitectura
- **Framework**: Flask (Python)
- **CORS**: Habilitado para integración frontend
- **Logging**: Configurado sin exposición de contraseñas
- **Validación**: Entrada robusta con manejo de errores

### Algoritmo de Evaluación
1. **Cálculo de Longitud**: Conteo de caracteres
2. **Análisis de Alfabeto**: Detección de tipos de caracteres utilizados
3. **Cálculo de Entropía**: Aplicación de la fórmula matemática
4. **Verificación de Diccionario**: Comparación contra contraseñas comunes
5. **Evaluación Final**: Categorización y recomendaciones

### Base de Datos de Contraseñas Comunes
- Fuente: `1millionPasswords.csv`
- Extracción: Solo columna 2 (contraseñas)
- Formato: Set en memoria para búsqueda O(1)
- Penalización: Reducción de entropía a 10% para contraseñas comunes

## Consideraciones de Seguridad

1. **No Persistencia**: Las contraseñas nunca se almacenan
2. **No Logging**: Las contraseñas no aparecen en logs
3. **Validación**: Entrada validada y sanitizada
4. **Manejo de Errores**: Respuestas seguras sin exposición de información interna
5. **Rate Limiting**: Recomendado para producción (no implementado en esta versión)

## Desarrollo y Testing

### Estructura del Proyecto
```
C2 - A3 - Evaluacion de contraseñas/
├── app.py                    # Aplicación principal
├── requirements.txt          # Dependencias
├── README.md                # Documentación
├── 1millionPasswords.csv    # Base de datos de contraseñas comunes
└── test_api.py              # Script de pruebas (opcional)
```

### Variables de Entorno
- `PORT`: Puerto del servidor (default: 5000)
- `DEBUG`: Modo debug (default: False)

## Contribución

Este proyecto fue desarrollado como parte de la evaluación de la materia "Seguridad de la Información" para comprender los principios de entropía y evaluación de contraseñas.

---

**Nota**: Esta API es para fines educativos. Para aplicaciones de producción, considere implementar rate limiting, autenticación y otras medidas de seguridad adicionales.
