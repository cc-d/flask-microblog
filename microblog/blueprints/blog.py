import sys
sys.path.append('..')

from website import *

bp = Blueprint('blog', 'blog', url_prefix='/blog/')

@bp.route('/', methods=['GET'])
def blog_index():
    return render_template('blog/index.html')

@bp.route('/create', methods=['GET','POST'])
def create_post(title=None, text=None, url=None, author=None):
    if request.method == 'GET':
        return render_template('blog/create.html')
    else:
        pass
