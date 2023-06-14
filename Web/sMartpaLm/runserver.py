from waitress import serve
from config.wsgi import application
import config.settings as st

if __name__=='__main__':
    serve(application, host='localhost', port='8000')
    print(st.BASE_DIR)