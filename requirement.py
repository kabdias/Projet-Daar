import subprocess
import sys

packages =['django','nltk','regex','pyvis','networkx','elasticsearch']

def install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#for p in packages:
#	install(p)
