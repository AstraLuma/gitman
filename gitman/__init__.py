from flask import Flask, render_template, request
from .githelper import GitHelper
import configparser
import os.path

config = configparser.ConfigParser()
configfile = lambda n: os.path.join(os.path.dirname(__file__), '..', n)
config.read(map(configfile, ['default.ini', 'local.ini']))

# Map of README files and the parser to use
READMES = {
	'README': lambda s: s.decode('utf8'),
	'README.txt': lambda s: s.decode('utf8'),
	'README.md': lambda s: s.decode('utf8'),
	'README.rst': lambda s: s.decode('utf8'),
}

app = Flask(__name__)
git = GitHelper(config['git']['root'])

@app.route("/")
def index():
	return render_template('index.html', repos=sorted(git, key=lambda i: i.name), cloneroot=config['git']['clone_root'])

@app.route("/<path:repo>")
def showrepo(repo):
	g = git[repo]
	for fn, mapper in READMES.items():
		try:
			raw = g.file(fn)
		except Exception:
			continue
		else:
			readme = mapper(raw)
			break
	else:
		readme = None
	return render_template('repo.html', repo=g, readme=readme, cloneroot=config['git']['clone_root'])
