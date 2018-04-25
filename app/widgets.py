from flask_appbuilder.widgets import ListWidget

class MyListWidget(ListWidget):
     template = 'widgets/list.html'

class MySearchWidget(ListWidget):
     template = 'widgets/search.html'
