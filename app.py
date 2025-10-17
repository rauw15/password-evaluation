#!/usr/bin/env python3
"""
API RESTful para Evaluación de Contraseñas
Materia: Seguridad de la Información
Objetivo: Implementar cálculo de entropía y evaluación de calidad de contraseñas
"""

import csv
import math
import re
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from difflib import SequenceMatcher

# Configurar logging sin exponer contraseñas
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Cargar diccionario de contraseñas comunes
COMMON_PASSWORDS = set()

def load_common_passwords():
    """Carga las contraseñas comunes desde el archivo CSV (solo columna 2)"""
    global COMMON_PASSWORDS
    try:
        with open('1millionPasswords.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Saltar header
            for row in csv_reader:
                if len(row) >= 2:
                    COMMON_PASSWORDS.add(row[1].strip().lower())
        logger.info(f"Cargadas {len(COMMON_PASSWORDS)} contraseñas comunes")
    except FileNotFoundError:
        logger.warning("Archivo 1millionPasswords.csv no encontrado")
    except Exception as e:
        logger.error(f"Error cargando contraseñas comunes: {e}")

def calculate_L(password):
    """
    Calcula la longitud de la contraseña (L)
    
    Args:
        password (str): Contraseña a evaluar
        
    Returns:
        int: Longitud de la contraseña
    """
    return len(password)

def calculate_N(password):
    """
    Calcula el tamaño del alfabeto (N) basado en los tipos de caracteres utilizados
    
    Args:
        password (str): Contraseña a evaluar
        
    Returns:
        int: Tamaño del alfabeto (keyspace)
    """
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digits = bool(re.search(r'[0-9]', password))
    has_symbols = bool(re.search(r'[^a-zA-Z0-9]', password))
    
    alphabet_size = 0
    if has_lowercase:
        alphabet_size += 26  # a-z
    if has_uppercase:
        alphabet_size += 26  # A-Z
    if has_digits:
        alphabet_size += 10  # 0-9
    if has_symbols:
        alphabet_size += 32  # símbolos comunes (~!@#$%^&*()_+-=[]{}|;:,.<>?)
    
    return alphabet_size

def calculate_entropy(password):
    """
    Calcula la entropía de la contraseña usando la fórmula E = L × log2(N)
    
    Args:
        password (str): Contraseña a evaluar
        
    Returns:
        float: Entropía en bits
    """
    if not password:
        return 0.0
    
    L = calculate_L(password)
    N = calculate_N(password)
    
    if N == 0:
        return 0.0
    
    entropy = L * math.log2(N)
    return round(entropy, 2)

def calculate_similarity(str1, str2):
    """
    Calcula la similitud entre dos strings usando SequenceMatcher
    
    Args:
        str1 (str): Primer string
        str2 (str): Segundo string
        
    Returns:
        float: Similitud entre 0.0 y 1.0 (1.0 = idénticos)
    """
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_similar_passwords(password, threshold=0.8):
    """
    Encuentra contraseñas similares en el diccionario
    
    Args:
        password (str): Contraseña a evaluar
        threshold (float): Umbral de similitud (0.0 a 1.0)
        
    Returns:
        list: Lista de contraseñas similares encontradas
    """
    similar_passwords = []
    password_lower = password.lower()
    

    if password_lower in COMMON_PASSWORDS:
        return [password_lower]
    


    symbols = ['!', '@', '#', '$', '%', '&', '*', '?', '.', '1', '2', '3', '123']
    for symbol in symbols:
        without_symbol = password_lower.rstrip(symbol)
        if without_symbol in COMMON_PASSWORDS and without_symbol != password_lower:
            similar_passwords.append(without_symbol)
        
        with_symbol = password_lower + symbol
        if with_symbol in COMMON_PASSWORDS:
            similar_passwords.append(with_symbol)
    
    for i in range(10):
        without_number = password_lower.rstrip(str(i))
        if without_number in COMMON_PASSWORDS and without_number != password_lower:
            similar_passwords.append(without_number)
        
        with_number = password_lower + str(i)
        if with_number in COMMON_PASSWORDS:
            similar_passwords.append(with_number)
    
    if not similar_passwords:
        for common_pass in COMMON_PASSWORDS:
            similarity = calculate_similarity(password_lower, common_pass)
            if similarity >= threshold:
                similar_passwords.append(common_pass)
                if len(similar_passwords) >= 3:
                    break
    
    return list(set(similar_passwords))  

def check_password_strength(password, entropy):
    """
    Evalúa la fuerza de la contraseña basada en entropía y otros factores
    
    Args:
        password (str): Contraseña a evaluar
        entropy (float): Entropía calculada
        
    Returns:
        dict: Información completa sobre la fuerza de la contraseña
    """
    # Categoría basada en entropía
    if entropy < 60:
        strength_category = "Débil o Aceptable"
        security_level = "Baja"
    elif entropy < 80:
        strength_category = "Fuerte"
        security_level = "Media"
    else:
        strength_category = "Muy Fuerte"
        security_level = "Alta"
    
    # Verificación contra diccionario de contraseñas comunes y similares
    similar_passwords = find_similar_passwords(password)
    is_common = password.lower() in COMMON_PASSWORDS
    is_similar = len(similar_passwords) > 0
    
    # Penalización por contraseña común o similar
    if is_common:
        strength_category = "Muy Débil"
        security_level = "Muy Baja"
        entropy_penalized = entropy * 0.1
    elif is_similar:
        strength_category = "Débil"
        security_level = "Muy Baja"
        entropy_penalized = entropy * 0.3
    else:
        entropy_penalized = entropy
    
    # Tiempo estimado de crackeo (asumiendo 10^11 intentos/segundo)
    attack_rate = 10**11
    total_combinations = 2**entropy_penalized
    time_to_crack_seconds = total_combinations / attack_rate
    
    # Convertir a unidades más legibles
    if time_to_crack_seconds < 1:
        time_to_crack = "< 1 segundo"
    elif time_to_crack_seconds < 60:
        time_to_crack = f"{time_to_crack_seconds:.2f} segundos"
    elif time_to_crack_seconds < 3600:
        time_to_crack = f"{time_to_crack_seconds/60:.2f} minutos"
    elif time_to_crack_seconds < 86400:
        time_to_crack = f"{time_to_crack_seconds/3600:.2f} horas"
    elif time_to_crack_seconds < 31536000:
        time_to_crack = f"{time_to_crack_seconds/86400:.2f} días"
    else:
        time_to_crack = f"{time_to_crack_seconds/31536000:.2f} años"
    
    return {
        "strength_category": strength_category,
        "security_level": security_level,
        "is_common_password": is_common,
        "is_similar_password": is_similar,
        "similar_passwords_found": similar_passwords[:3],  # Máximo 3 para no sobrecargar
        "entropy_bits": entropy,
        "entropy_after_penalties": round(entropy_penalized, 2),
        "time_to_crack": time_to_crack,
        "recommendations": _get_recommendations(entropy, is_common, is_similar, password)
    }

def _get_recommendations(entropy, is_common, is_similar, password):
    """
    Genera recomendaciones para mejorar la contraseña
    
    Args:
        entropy (float): Entropía de la contraseña
        is_common (bool): Si es una contraseña común
        is_similar (bool): Si es similar a una contraseña común
        password (str): La contraseña original
        
    Returns:
        list: Lista de recomendaciones
    """
    recommendations = []
    
    if is_common:
        recommendations.append("Esta contraseña está en el diccionario de contraseñas comunes")
        recommendations.append("Evite usar contraseñas comunes del diccionario")
    
    if is_similar:
        recommendations.append("Esta contraseña es similar a contraseñas comunes")
        recommendations.append("No basta con añadir/quitar símbolos o números a contraseñas débiles")
        recommendations.append("Use palabras aleatorias o frases únicas")
    
    if entropy < 60:
        recommendations.append("Aumente la longitud de la contraseña")
        recommendations.append("Use una combinación de letras mayúsculas, minúsculas, números y símbolos")
    
    if len(password) < 12:
        recommendations.append("Use al menos 12 caracteres")
    
    if not re.search(r'[a-z]', password):
        recommendations.append("Incluya letras minúsculas")
    
    if not re.search(r'[A-Z]', password):
        recommendations.append("Incluya letras mayúsculas")
    
    if not re.search(r'[0-9]', password):
        recommendations.append("Incluya números")
    
    if not re.search(r'[^a-zA-Z0-9]', password):
        recommendations.append("Incluya símbolos especiales")
    
    if len(recommendations) == 0:
        recommendations.append("✅ Excelente! Su contraseña cumple con los estándares de seguridad")
    
    return recommendations

@app.route('/api/v1/password/evaluate', methods=['POST'])
def evaluate_password():
    """
    Endpoint para evaluar la fuerza de una contraseña
    
    Body:
        {
            "password": "string"
        }
    
    Returns:
        {
            "password_length": int,
            "alphabet_size": int,
            "entropy_bits": float,
            "strength_evaluation": {
                "strength_category": "string",
                "security_level": "string",
                "is_common_password": bool,
                "is_similar_password": bool,
                "similar_passwords_found": ["string"],
                "entropy_after_penalties": float,
                "time_to_crack": "string",
                "recommendations": ["string"]
            }
        }
    """
    try:
        # Validar entrada
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), 400
        
        data = request.get_json()
        if not data or 'password' not in data:
            return jsonify({"error": "Campo 'password' es requerido"}), 400
        
        password = data['password']
        
        # Validar tipo de dato
        if not isinstance(password, str):
            return jsonify({"error": "El campo 'password' debe ser una cadena de texto"}), 400
        
        # Calcular métricas
        password_length = calculate_L(password)
        alphabet_size = calculate_N(password)
        entropy = calculate_entropy(password)
        strength_evaluation = check_password_strength(password, entropy)
        
        # Respuesta (sin incluir la contraseña original por seguridad)
        response = {
            "password_length": password_length,
            "alphabet_size": alphabet_size,
            "entropy_bits": entropy,
            "strength_evaluation": strength_evaluation
        }
        
        # Log de la evaluación (sin la contraseña)
        logger.info(f"Evaluación completada - Longitud: {password_length}, Entropía: {entropy}")
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error en evaluación de contraseña: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que la API esté funcionando"""
    return jsonify({
        "status": "healthy",
        "service": "Password Evaluation API",
        "version": "1.0.0"
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Endpoint raíz con información básica"""
    return jsonify({
        "message": "API de Evaluación de Contraseñas",
        "version": "1.0.0",
        "endpoints": {
            "evaluate": "/api/v1/password/evaluate (POST)",
            "health": "/api/v1/health (GET)"
        },
        "documentation": "Ver README.md para más información"
    }), 200

if __name__ == '__main__':
    # Cargar contraseñas comunes al iniciar
    load_common_passwords()
    
    # Configurar servidor
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Iniciando servidor en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=debug, threaded=True)
