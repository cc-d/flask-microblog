import sys
sys.path.append('..')

from website import *

bp = Blueprint('user', 'user', url_prefix='/user')

@bp.route('/<username>/', methods=['GET'])
def profile(username=None):
    return render_template('profile.html')

@bp.route('/<username>/invite_links/', methods=['GET', 'POST'])
def invite_links():
    return is_admin()
