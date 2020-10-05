from setuptools import setup
from io import open


def read(filename):
	with open(filename, encoding='utf-8') as file:
		return file.read()


setup(
	name='urlDB',
	version='0.1a',
	packages=['urldb'],
	url='https://github.com/WhiteApfel/urlDB',
	license='Mozilla Public License 2.0',
	author='WhiteApfel',
	author_email='white@pfel.ru',
	install_requires=read("requirements.txt").split("\n"),
	description='Tool for nice work with storing data in URL '
)
