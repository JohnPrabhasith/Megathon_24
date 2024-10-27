# config.py
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Required environment variables
REQUIRED_ENV_VARS = ['MONGODB_URI', 'GROQ_API_KEY']

# Check for required environment variables
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

# MongoDB configuration
MONGODB_URI = os.getenv('MONGODB_URI')

# API Keys
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Model Configuration
MODEL_CONFIG = {
    'polarity': {
        'model': 'llama-3.1-70b-versatile',
        'temperature': 0.1,
        'max_tokens': 100,
        'timeout': 30  # Added timeout
    },
    'concern': {
        'model': 'mixtral-8x7b-32768',
        'temperature': 0.1,
        'max_tokens': 200,
        'timeout': 30
    },
    'intensity': {
        'model': 'llama-3.1-8b-instant',
        'temperature': 0.1,
        'max_tokens': 100,
        'timeout': 30
    }
}

# Logging Configuration
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  # Added to prevent disabling other loggers
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',  # Changed to RotatingFileHandler
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'level': 'DEBUG',
            'formatter': 'detailed'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Categories for mental health concerns (updated to match classifier.py)
CONCERN_CATEGORIES = {
    'Anxiety',
    'Depression',
    'Stress',
    'Insomnia',
    'Eating Disorder',
    'Health Anxiety',
    'Positive Outlook'
}

# Intensity levels with numerical ranges
INTENSITY_LEVELS = {
    'mild': (1, 3),
    'moderate': (4, 7),
    'severe': (8, 10)
}