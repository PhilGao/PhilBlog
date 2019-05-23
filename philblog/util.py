import os
from flask import current_app,url_for

upload_folder=os.path.join('upload')
static_res_folder = os.path.join('static','res','image')


def render_upload_file(filename,type):
    if type == 'show_window':
        return os.path.join(current_app.root_path,static_res_folder,filename)
    if type == 'upload':
        return os.path.join(current_app.root_path,upload_folder,filename)
    return None