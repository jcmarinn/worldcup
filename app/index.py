from flask_appbuilder import IndexView
from flask_login import current_user


class JCIndexView(IndexView):
    index_template = 'index.html'
    extra_args = {'user':'JC'}
