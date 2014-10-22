from flask import Flask, render_template
from .githelper import GitHelper

# Config
REPO_ROOT = '/srv/code'

# Map of README files and the parser to use
READMES = {
	'README': None,
	'README.txt': None,
	'README.md': None,
	'README.rst': None,
}

app = Flask(__name__)
git = GitHelper(REPO_ROOT)

@app.route("/")
def index():
	return render_template('index.html', repos=sorted(git, key=lambda i: i.name))

@app.route("/<path:repo>")
def showrepo(repo):
	g = git[repo]
	for fn, _ in READMES.items():
		try:
			readme = g.file(fn)
		except Exception:
			continue
	else:
		readme = None
	return render_template('repo.html', repo=g, readme=readme)
