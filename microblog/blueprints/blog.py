import sys
sys.path.append('..')

from website import *

bp = Blueprint('blog', 'blog', url_prefix='/blog/')

@bp.route('/', methods=['GET'])
def blog_index():
    blogs = db.session.query(Blog).all()
    return render_template('blog/index.html', blogs=blogs)

@bp.route('/create', methods=['GET','POST'])
def create_post(title=None, text=None, url=None, author=None, visibility=None, api=False):
    if request.method == 'GET':
        return render_template('blog/create.html')
    elif api or request.method == 'POST':
        if not api:
            text = request.form.get('text') if text is None else text
            title = request.form.get('title') if title is None else title
            url = request.form.get('url') if url is None else url
            author = request.form.get('author') if author is None else author
            visibility = request.form.get('visibility') if visibility is None else visibility

        new_post = Blog(author=author, title=title, text=text)
        db.session.add(new_post)
        db.session.commit()

        print(str(vars(new_post)))

        return render_template('blog/index.html')