#!/usr/bin/env python3
"""
Script de prueba para la detección de similitudes en contraseñas
"""

import requests
import json

BASE_URL = "http://localhost:5000"
ENDPOINT = f"{BASE_URL}/api/v1/password/evaluate"

def test_similarity():
    """Prueba la detección de similitudes"""
    
    print("=" * 70)
    print("PRUEBAS DE DETECCIÓN DE SIMILITUDES EN CONTRASEÑAS")
    print("=" * 70)
    
    test_cases = [
        {
            "name": "Contraseña común exacta",
            "password": "password",
            "expected_similar": True
        },
        {
            "name": "Contraseña común con símbolo añadido",
            "password": "password!",
            "expected_similar": True
        },
        {
            "name": "Contraseña común con número añadido",
            "password": "password123",
            "expected_similar": True
        },
        {
            "name": "Contraseña común con símbolo quitado",
            "password": "saoiens",  # Si "saoiens@" está en el CSV
            "expected_similar": True
        },
        {
            "name": "Contraseña común con @ añadido",
            "password": "saoiens@",
            "expected_similar": True
        },
        {
            "name": "Contraseña segura única",
            "password": "MiContraseñaSegura2024!@#",
            "expected_similar": False
        },
        {
            "name": "123456 (muy común)",
            "password": "123456",
            "expected_similar": True
        },
        {
            "name": "123456 con símbolo",
            "password": "123456!",
            "expected_similar": True
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Contraseña: '{test_case['password']}'")
        
        try:
            response = requests.post(
                ENDPOINT,
                json={"password": test_case["password"]},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                strength = data['strength_evaluation']
                
                print(f"   ✅ Status: {response.status_code}")
                print(f"   Entropía: {data['entropy_bits']} bits")
                print(f"   Categoría: {strength['strength_category']}")
                print(f"   Nivel seguridad: {strength['security_level']}")
                print(f"   Es común: {strength['is_common_password']}")
                print(f"   Es similar: {strength['is_similar_password']}")
                
                if strength['similar_passwords_found']:
                    print(f"   🔍 Contraseñas similares encontradas:")
                    for similar in strength['similar_passwords_found']:
                        print(f"      • '{similar}'")
                
                print(f"   Tiempo crackeo: {strength['time_to_crack']}")
                print(f"   Recomendaciones:")
                for rec in strength['recommendations'][:3]:
                    print(f"      • {rec}")
                    
            else:
                print(f"   ❌ Error - Status: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error de conexión: {e}")
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
    
    print("\n" + "=" * 70)
    print("PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    print("Asegúrate de que la API esté ejecutándose en http://localhost:5000")
    print("Presiona Enter para continuar o Ctrl+C para cancelar...")
    input()
    
    test_similarity()

