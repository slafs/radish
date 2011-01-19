from distutils.core import setup
setup(name='radish',
	description='A set of common tools for testing django projects with lettuce',
	author='Red Interactive',
	author_email='geeks@ff0000.com',
	version='0.1',
	py_modules=['radish'],
		install_requires=['django', 'lettuce',],)
