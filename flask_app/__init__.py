from flask import Flask, session
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
app.static_url_path = '/mywatchlist/static'
url_map = app.url_map
for rule in url_map.iter_rules('static'):
    url_map._rules.remove(rule)
app.add_url_rule(app.static_url_path + '/<path:filename>',endpoint='static', view_func=app.send_static_file)

