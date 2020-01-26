import sys
sys.path.append('..')

from website import *

bp = Blueprint('blog', 'blog', url_prefix='/blog/')

@bp.route('/', methods=['GET'])
def blog_index():
    return render_template('blog/index.html')