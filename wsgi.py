import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monte_platform.settings')

application = get_wsgi_application()
app = application  # For gunicorn compatibility