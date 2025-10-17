#!/usr/bin/env python3
"""
Script de pruebas para la API de Evaluación de Contraseñas
"""

import requests
import json
import time

# Configuración
BASE_URL = "http://localhost:5000"
ENDPOINT = f"{BASE_URL}/api/v1/password/evaluate"

def test_password_evaluation():
    """Prueba la evaluación de diferentes tipos de contraseñas"""
    
    test_cases = [
        {
            "name": "Contraseña muy débil (común)",
            "password": "123456",
            "expected_weak": True
        },
        {
            "name": "Contraseña débil (corta)",
            "password": "abc",
            "expected_weak": True
        },
        {
            "name": "Contraseña débil (solo números)",
            "password": "12345678",
            "expected_weak": True
        },
        {
            "name": "Contraseña débil (solo letras)",
            "password": "password",
            "expected_weak": True
        },
        {
            "name": "Contraseña media",
            "password": "MiPassword123",
            "expected_weak": False
        },
        {
            "name": "Contraseña fuerte",
            "password": "MiContraseña123!",
            "expected_weak": False
        },
        {
            "name": "Contraseña muy fuerte",
            "password": "MiContraseña123!@#$%^&*()",
            "expected_weak": False
        },
        {
            "name": "Contraseña vacía",
            "password": "",
            "expected_weak": True
        }
    ]
    
    print("=" * 60)
    print("PRUEBAS DE EVALUACIÓN DE CONTRASEÑAS")
    print("=" * 60)
    
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
                print(f"   ✅ Éxito - Status: {response.status_code}")
                print(f"   Longitud: {data['password_length']}")
                print(f"   Tamaño alfabeto: {data['alphabet_size']}")
                print(f"   Entropía: {data['entropy_bits']} bits")
                print(f"   Categoría: {data['strength_evaluation']['strength_category']}")
                print(f"   Nivel seguridad: {data['strength_evaluation']['security_level']}")
                print(f"   Es común: {data['strength_evaluation']['is_common_password']}")
                print(f"   Tiempo crackeo: {data['strength_evaluation']['time_to_crack']}")
                print(f"   Recomendaciones: {', '.join(data['strength_evaluation']['recommendations'][:2])}")
            else:
                print(f"   ❌ Error - Status: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error de conexión: {e}")
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")

def test_health_check():
    """Prueba el endpoint de health check"""
    print("\n" + "=" * 60)
    print("PRUEBA DE HEALTH CHECK")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check exitoso")
            print(f"   Status: {data['status']}")
            print(f"   Servicio: {data['service']}")
            print(f"   Versión: {data['version']}")
        else:
            print(f"❌ Health Check falló - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en Health Check: {e}")

def test_error_cases():
    """Prueba casos de error"""
    print("\n" + "=" * 60)
    print("PRUEBAS DE CASOS DE ERROR")
    print("=" * 60)
    
    error_cases = [
        {
            "name": "Sin campo password",
            "data": {},
            "expected_status": 400
        },
        {
            "name": "Campo password vacío",
            "data": {"password": ""},
            "expected_status": 200  # Debe funcionar pero con entropía 0
        },
        {
            "name": "Campo password no es string",
            "data": {"password": 123},
            "expected_status": 400
        },
        {
            "name": "Content-Type incorrecto",
            "data": "invalid json",
            "expected_status": 400
        }
    ]
    
    for i, test_case in enumerate(error_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        
        try:
            if test_case['name'] == "Content-Type incorrecto":
                response = requests.post(
                    ENDPOINT,
                    data=test_case['data'],
                    headers={"Content-Type": "text/plain"},
                    timeout=5
                )
            else:
                response = requests.post(
                    ENDPOINT,
                    json=test_case['data'],
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
            
            if response.status_code == test_case['expected_status']:
                print(f"   ✅ Status esperado: {response.status_code}")
            else:
                print(f"   ❌ Status inesperado: {response.status_code} (esperado: {test_case['expected_status']})")
            
            print(f"   Respuesta: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_performance():
    """Prueba básica de rendimiento"""
    print("\n" + "=" * 60)
    print("PRUEBA DE RENDIMIENTO")
    print("=" * 60)
    
    test_password = "MiContraseña123!@#$%^&*()"
    num_requests = 10
    
    print(f"Enviando {num_requests} requests con contraseña: '{test_password}'")
    
    start_time = time.time()
    successful_requests = 0
    
    for i in range(num_requests):
        try:
            response = requests.post(
                ENDPOINT,
                json={"password": test_password},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if response.status_code == 200:
                successful_requests += 1
        except:
            pass
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / num_requests if num_requests > 0 else 0
    
    print(f"✅ Requests exitosos: {successful_requests}/{num_requests}")
    print(f"   Tiempo total: {total_time:.2f} segundos")
    print(f"   Tiempo promedio: {avg_time:.3f} segundos por request")
    print(f"   Requests por segundo: {successful_requests/total_time:.2f}")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("Iniciando pruebas de la API de Evaluación de Contraseñas...")
    print("Asegúrese de que la API esté ejecutándose en http://localhost:5000")
    print("\nPresione Enter para continuar o Ctrl+C para cancelar...")
    input()
    
    try:
        # Ejecutar todas las pruebas
        test_health_check()
        test_password_evaluation()
        test_error_cases()
        test_performance()
        
        print("\n" + "=" * 60)
        print("TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nPruebas canceladas por el usuario.")
    except Exception as e:
        print(f"\n\nError durante las pruebas: {e}")

if __name__ == "__main__":
    main()
