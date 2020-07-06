from flask import Blueprint, request, abort, render_template,redirect,url_for
from philblog.models import Article

search_dp = Blueprint('search', __name__)


#todo: we should use get or post ?? should use get i think , but the get would have the json body???
@search_dp.route('/_search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        return redirect(url_for('about.html'))
    try:
        request_body = request.json
        results, number = Article.search(request_body['search'], 1, 5)
        return {"number": number, "results": [{"title": item.title, "content": item.content} for item in results]}
    except KeyError or TypeError:
        abort(400, "the request content is not correct")


@search_dp.route('/search', methods=['GET','POST'])
def search_form():
    return render_template('search.html')