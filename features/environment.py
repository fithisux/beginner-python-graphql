from werkzeug.serving import make_server
import flaskql 

import threading
import os
import tempfile

class MyServer :
    def  __init__(self):
        _, db_fname = tempfile.mkstemp()
        app = flaskql.create_app({
            'DATABASE': db_fname,
                'TESTING': True,
                'ENV' : 'development'})
        app.debug = False
        self.db_fname = db_fname
        self.srv = make_server('127.0.0.1', 5000, app)
 
        with app.app_context() as app_context:
            flaskql.db.init_db()
            app_context.push()
            
    def start(self):
        self.srv.serve_forever() 
           
    def shutdown(self):
        self.srv.shutdown()
        os.unlink(self.db_fname)
            
def thread_function(context):
    context.server.start()
    
def before_feature(context, feature):
    context.server = MyServer()
    context.testing_thread = threading.Thread(target=thread_function, args=(context,))
    context.testing_thread.start()

def after_feature(context, feature):
    context.server.shutdown()
    context.testing_thread.join()