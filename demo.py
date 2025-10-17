#!/usr/bin/env python3
"""
Script de demostración para la API de Evaluación de Contraseñas
Muestra ejemplos de uso y cálculos de entropía
"""

import math
import re

def calculate_L(password):
    """Calcula la longitud de la contraseña"""
    return len(password)

def calculate_N(password):
    """Calcula el tamaño del alfabeto"""
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digits = bool(re.search(r'[0-9]', password))
    has_symbols = bool(re.search(r'[^a-zA-Z0-9]', password))
    
    alphabet_size = 0
    if has_lowercase:
        alphabet_size += 26
    if has_uppercase:
        alphabet_size += 26
    if has_digits:
        alphabet_size += 10
    if has_symbols:
        alphabet_size += 32
    
    return alphabet_size

def calculate_entropy(password):
    """Calcula la entropía usando E = L × log2(N)"""
    if not password:
        return 0.0
    
    L = calculate_L(password)
    N = calculate_N(password)
    
    if N == 0:
        return 0.0
    
    entropy = L * math.log2(N)
    return round(entropy, 2)

def analyze_password(password):
    """Analiza una contraseña y muestra información detallada"""
    print(f"Contraseña: '{password}'")
    print("-" * 50)
    
    L = calculate_L(password)
    N = calculate_N(password)
    entropy = calculate_entropy(password)
    
    print(f"Longitud (L): {L} caracteres")
    print(f"Tamaño del alfabeto (N): {N}")
    print(f"Entropía (E = L × log₂(N)): {entropy} bits")
    
    # Análisis de tipos de caracteres
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))
    
    print(f"\nTipos de caracteres utilizados:")
    print(f"  Minúsculas (a-z): {'✓' if has_lower else '✗'} (26 caracteres)")
    print(f"  Mayúsculas (A-Z): {'✓' if has_upper else '✗'} (26 caracteres)")
    print(f"  Números (0-9): {'✓' if has_digit else '✗'} (10 caracteres)")
    print(f"  Símbolos: {'✓' if has_symbol else '✗'} (32 caracteres)")
    
    # Categorización
    if entropy < 60:
        category = "Débil o Aceptable"
    elif entropy < 80:
        category = "Fuerte"
    else:
        category = "Muy Fuerte"
    
    print(f"\nCategoría de fuerza: {category}")
    
    # Tiempo estimado de crackeo (10^11 intentos/segundo)
    attack_rate = 10**11
    total_combinations = 2**entropy
    time_to_crack_seconds = total_combinations / attack_rate
    
    if time_to_crack_seconds < 1:
        time_str = "< 1 segundo"
    elif time_to_crack_seconds < 60:
        time_str = f"{time_to_crack_seconds:.2f} segundos"
    elif time_to_crack_seconds < 3600:
        time_str = f"{time_to_crack_seconds/60:.2f} minutos"
    elif time_to_crack_seconds < 86400:
        time_str = f"{time_to_crack_seconds/3600:.2f} horas"
    elif time_to_crack_seconds < 31536000:
        time_str = f"{time_to_crack_seconds/86400:.2f} días"
    else:
        time_str = f"{time_to_crack_seconds/31536000:.2f} años"
    
    print(f"Tiempo estimado de crackeo: {time_str}")
    
    # Recomendaciones
    recommendations = []
    if entropy < 60:
        recommendations.append("Aumente la longitud")
        recommendations.append("Use más tipos de caracteres")
    if len(password) < 12:
        recommendations.append("Use al menos 12 caracteres")
    if not has_lower:
        recommendations.append("Incluya letras minúsculas")
    if not has_upper:
        recommendations.append("Incluya letras mayúsculas")
    if not has_digit:
        recommendations.append("Incluya números")
    if not has_symbol:
        recommendations.append("Incluya símbolos especiales")
    
    if recommendations:
        print(f"\nRecomendaciones:")
        for rec in recommendations:
            print(f"  • {rec}")
    else:
        print(f"\n✓ Excelente! Su contraseña cumple con los estándares de seguridad")
    
    print("\n" + "=" * 60)

def main():
    """Función principal de demostración"""
    print("DEMOSTRACIÓN DE CÁLCULO DE ENTROPÍA DE CONTRASEÑAS")
    print("=" * 60)
    print("Materia: Seguridad de la Información")
    print("Fórmula: E = L × log₂(N)")
    print("Donde:")
    print("  L = Longitud de la contraseña")
    print("  N = Tamaño del alfabeto (keyspace)")
    print("  log₂ = Logaritmo en base 2")
    print("\nCategorías:")
    print("  • 0-60 bits: Débil o Aceptable")
    print("  • 60-80 bits: Fuerte")
    print("  • 80+ bits: Muy Fuerte")
    print("\n" + "=" * 60)
    
    # Ejemplos de contraseñas
    examples = [
        "123456",
        "password",
        "abc",
        "Password123",
        "MiContraseña123",
        "MiContraseña123!",
        "MiContraseña123!@#$%^&*()",
        "¡EstaEsUnaContraseñaMuySegura123!@#",
        "",
        "a"
    ]
    
    for i, password in enumerate(examples, 1):
        print(f"\nEJEMPLO {i}:")
        analyze_password(password)
    
    print("\nDEMOSTRACIÓN COMPLETADA")
    print("Para usar la API REST, ejecute: python app.py")
    print("Luego use el endpoint: POST /api/v1/password/evaluate")

if __name__ == "__main__":
    main()
