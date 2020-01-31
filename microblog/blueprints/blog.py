import sys
sys.path.append('..')

from website import *

bp = Blueprint('blog', 'blog')


@bp.route('/', methods=['GET'])
def blog_index():
    blogs = db.session.query(Blog).all()
    blogs = [x for x in blogs[::-1]]

    return render_template('blog/index.html', blogs=blogs)



@bp.route('/article/<int:blog_id>/', methods=['GET'])
@bp.route('/article/<string:custom_url>/', methods=['GET'])
def show_article(blog_id=None, custom_url=None):
    if blog_id is not None:
        article = db.session.query(Blog).filter_by(id=blog_id).first()
    elif custom_url is not None:
        article = db.session.query(Blog).filter(
            func.lower(Blog.custom_url) == func.lower(custom_url)
        ).first()

    if article is None:
        abort(404)
    else:
        return render_template('blog/article.html', article=article)


@bp.route('/blog/create', methods=['GET','POST'])
@req_csrf
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
        print(text, title, url, author, visibility)
        new_post = Blog(author=author, title=title, text=text)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('blog.blog_index'))