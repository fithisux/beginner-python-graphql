from werkzeug.serving import make_server
import flaskql 
import time   

import threading
import os
import tempfile

def create_server():
    global db_fname
    
    _, db_fname = tempfile.mkstemp()
    app = flaskql.create_app({
        'DATABASE': db_fname,
            'TESTING': True,
            'ENV' : 'development'
            
            })
    app.debug = False
    global srv
    srv = make_server('127.0.0.1', 5000, app)

    with app.app_context() as app_context:
        flaskql.db.init_db()
        app_context.push()
            

def thread_function():
    global srv
    srv.serve_forever()
    
     
def before_feature(context, feature):
    create_server()
    context.testing_thread = threading.Thread(target=thread_function)
    context.testing_thread.start()
    time.sleep(2)
    
    

def after_feature(context, feature):
    global srv
    srv.shutdown()
    context.testing_thread.join()
    
    global db_fname
    os.unlink(db_fname)