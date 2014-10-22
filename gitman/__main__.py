# Because __main__ is treated as the start script, so python first looks in its directory instead of where the package started
import sys, os
sys.path[0] = os.path.dirname(os.path.dirname(__file__))

from gitman import app  # Asked #python: "Don't use relative imports"

if __debug__:
	app.debug = True

app.run()