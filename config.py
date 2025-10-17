"""
Configuración para la API de Evaluación de Contraseñas
"""

import os

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5000))
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    # Configuración de seguridad
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    PASSWORD_MAX_LENGTH = 256
    
    # Archivos
    COMMON_PASSWORDS_FILE = os.environ.get('COMMON_PASSWORDS_FILE', '1millionPasswords.csv')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Tasa de ataque para cálculo de tiempo de crackeo
    ATTACK_RATE_PER_SECOND = int(os.environ.get('ATTACK_RATE', '100000000000'))  # 10^11 por defecto

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'ERROR'

# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
