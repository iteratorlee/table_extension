from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import os
import time

def formatSize(_bytes):
    '''
    return file size (an integer)
    '''
    try:
        _bytes = float(_bytes)
        kb = _bytes / 1024
    except:
        print("Bad format")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            G = int(G)
            return "%dG" % (G)
        else:
            M = int(M)
            return "%dM" % (M)
    else:
        if kb >= 1:
            kb = int(kb)
            return "%dK" % (kb)
        else:
            _bytes = int(_bytes)
            return "%dB" % _bytes

class HelloWorldHandler(IPythonHandler):
    def get(self):
        self.finish('Hello, world!')

class FileSizeHandler(IPythonHandler):
    def get(self, _filepath):
        file_path = _filepath
        if not os.path.exists(file_path):
            self.write("File does not exist")
            return
        size = os.path.getsize(file_path)
        format_size = formatSize(size)
        self.write(format_size)

class FileDateHandler(IPythonHandler):
    def get(self, _filepath):
        file_path = _filepath
        if not os.path.exists(file_path):
            self.write("File does not exist")
            return
        statinfo = os.stat(file_path)
        st_mtime = statinfo.st_mtime
        format_date = time.localtime(st_mtime)
        self.write(format_date)

class ViewTableHandler(IPythonHandler):
    def get(self, _filepath):
        self.write()

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    print(web_app.settings['base_url'])

    #route patterns
    route_pattern = url_path_join(web_app.settings['base_url'], '/hello')
    file_size_pattern = url_path_join(web_app.settings['base_url'], '/filesize/(.+$)')
    print(file_size_pattern)
    file_date_pattern = url_path_join(web_app.settings['base_url'], '/filedate/(.+$)')
    #file path regx
    _file_path = r'.*$'
    web_app.add_handlers(host_pattern, [
                (route_pattern, HelloWorldHandler),
                (file_size_pattern, FileSizeHandler),
                (file_date_pattern, FileDateHandler)
                ])