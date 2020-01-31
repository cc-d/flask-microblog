import sys
sys.path.append('..')

from website import *

import os
import glob

bp = Blueprint('admin', 'admin')


def req_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' in session:
            if session['admin'] is True:
                return f(*args, **kwargs)
        return redirect(url_for('login'))
    return decorated_function


def get_file_urls():
    urls = glob.glob(app.config['UPLOAD_PATH'] + '/*')
    urls = [u.replace(app.config['UPLOAD_PATH'], '') for u in urls]
    urls = ['/static/uploads' + u for u in urls]

    # assosciate extension with each url
    urls = [(u, u.split('.')[-1]) for u in urls]

    return urls


@app.route('/admin/uploads/', methods=['GET'])
@req_admin
def view_files():
    return render_template('admin/uploads.html', file_urls=get_file_urls())


@app.route('/admin/upload', methods=['POST'])
@req_admin
def upload():
    if request.files:
        image = request.files['image']

        # generate unique server file name 
        # by appending -X 
        if os.path.exists(os.path.join(app.config['UPLOAD_PATH'], image.filename)):
            no_ext = '.'.join(image.filename.split('.')[:-1])
            copy_num = re.findall(r'.*-(\d+)$', no_ext)
            if len(copy_num) == 0:
                similar_files = len(glob.glob(app.config['UPLOAD_PATH'] + '/' + no_ext + '*'))

                image.filename = no_ext + '-' + str(similar_files) + '.' + image.filename.split('.')[-1]
            else:
                copy_num = int(copy_num[0]) + 1
                image.filename = no_ext + '-' + str(copy_num) + '.' + image.filename.split('.')[-1]
        image.save(os.path.join(app.config['UPLOAD_PATH'], image.filename))

        new_url = request.host + '/static/uploads/' + image.filename
        flash('uploaded file to %s' % new_url)
        return redirect(url_for('view_files'))


@app.route('/delete/upload', methods=['POST'])
@req_admin
def delete():
    pass