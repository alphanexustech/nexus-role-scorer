from app import app
import sys

from users.views import users
from tasks.views import tasks

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(tasks, url_prefix='/tasks')

# Sets the port, or defaults to 80
if (len(sys.argv) > 1):
    port = int(sys.argv[1])
else:
    port=80

app.run(debug=True, host='127.0.0.1', port=port)
