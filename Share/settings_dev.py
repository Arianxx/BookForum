"""
这个设置文件从环境中读取敏感变量。同时，如果本地有.env文件，它会读取其中的键值
"""
import os

import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
envpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')

if os.path.exists(envpath):
    # 将.env文件中的键值对读取到环境变量中
    dotenv.load_dotenv(envpath, override=True)

SECRET_KEY = os.environ.get('SECRET_KEY', '=wnuc_z8@9lv#suqysee^rubs4n6fp&eis_5e(3zy^mdf%&#i^')

DEBUG = os.environ.get('DEBUG', 'True') == str(True)

# DEGUB关闭下，支持的域名
ALLOWED_HOSTS = eval(os.environ.get('ALLOWED_HOSTS', 'False')) or ['127.0.0.1', ]

# 数据库配置
DATABASES = eval(os.environ.get('DATABASES', 'False')) or {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.qq.com')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', None)
EMAIL_USE_TLS = True
EMAIL_FROM = os.environ.get('EMAIL_FROM', None)
