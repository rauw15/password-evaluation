#!/usr/bin/env python3
"""
Script de inicio para la API de Evaluación de Contraseñas
"""

import sys
import os
import argparse
from app import app, load_common_passwords

def main():
    """Función principal de inicio"""
    parser = argparse.ArgumentParser(description='API de Evaluación de Contraseñas')
    parser.add_argument('--host', default='0.0.0.0', help='Host para el servidor (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Puerto para el servidor (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Ejecutar en modo debug')
    parser.add_argument('--demo', action='store_true', help='Ejecutar demostración de cálculo de entropía')
    parser.add_argument('--test', action='store_true', help='Ejecutar pruebas de la API')
    
    args = parser.parse_args()
    
    if args.demo:
        print("Ejecutando demostración de cálculo de entropía...")
        os.system('python demo.py')
        return
    
    if args.test:
        print("Ejecutando pruebas de la API...")
        print("Asegúrese de que la API esté ejecutándose primero con: python run.py")
        os.system('python test_api.py')
        return
    
    print("=" * 60)
    print("API DE EVALUACIÓN DE CONTRASEÑAS")
    print("=" * 60)
    print("Materia: Seguridad de la Información")
    print("Objetivo: Evaluar fuerza de contraseñas mediante entropía")
    print("")
    print("Iniciando servidor...")
    print(f"Host: {args.host}")
    print(f"Puerto: {args.port}")
    print(f"Debug: {args.debug}")
    print("")
    
    # Verificar que existe el archivo de contraseñas comunes
    if not os.path.exists('1millionPasswords.csv'):
        print("⚠️  ADVERTENCIA: No se encontró el archivo '1millionPasswords.csv'")
        print("   La verificación contra contraseñas comunes no estará disponible")
        print("")
    
    # Cargar contraseñas comunes
    print("Cargando contraseñas comunes...")
    load_common_passwords()
    
    print("Servidor iniciado exitosamente!")
    print("")
    print("ENDPOINTS DISPONIBLES:")
    print(f"  • POST http://{args.host}:{args.port}/api/v1/password/evaluate")
    print(f"  • GET  http://{args.host}:{args.port}/api/v1/health")
    print(f"  • GET  http://{args.host}:{args.port}/")
    print("")
    print("EJEMPLO DE USO:")
    print("curl -X POST http://localhost:5000/api/v1/password/evaluate \\")
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"password": "MiContraseña123!"}\'')
    print("")
    print("Presione Ctrl+C para detener el servidor")
    print("=" * 60)
    
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
    except Exception as e:
        print(f"\nError al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
