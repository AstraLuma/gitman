import os
import subprocess

class Repo:
	fspath = None
	path = None
	name = None
	def __init__(self, **kws):
		vars(self).update(kws)

	def file(self, fn):
		return subprocess.check_output(['git', 'show', 'HEAD:{}'.format(fn)], cwd=self.fspath, stderr=subprocess.DEVNULL)

	def config(self, name):
		try:
			return subprocess.check_output(['git', 'config', name], cwd=self.fspath).decode('utf8').rstrip()
		except subprocess.CalledProcessError as err:
			print(err)
			if err.returncode == 1:
				return None # XXX: Raise? Default? idk
			else:
				raise

	def branches(self, pattern=None):
		pl = [pattern] if pattern else []
		out = subprocess.check_output(['git', 'branch', '--list', '--no-color']+pl, cwd=self.fspath)
		out = out.decode('utf8')
		for line in out.split('\n'):
			if not line: continue
			name = line.lstrip('*').strip()
			yield {'name': name, 'description': self.config('branch.{}.description'.format(name)) or ''}


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
