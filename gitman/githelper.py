import os

class Repo:
	fspath = None
	path = None
	name = None
	def __init__(self, **kws):
		vars(self).update(kws)

	def file(self, fn):
		pass

class GitHelper:
	def __init__(self, root):
		self.root = os.path.abspath(root)

	def __iter__(self):
		CHECK_FILES = ['config', 'HEAD'] # If these files exist, assume it's a git repo
		for dirpath, dirnames, filenames in os.walk(self.root):
			if all(cf in filenames for cf in CHECK_FILES):
				dirnames.clear()
				fn = dirpath[len(self.root)+1:]
				yield Repo(fspath=dirpath, path=fn, name=fn)

	def __getitem__(self, fn):
		dirpath = os.path.join(self.root, fn)
		return Repo(fspath=dirpath, path=fn, name=fn)
