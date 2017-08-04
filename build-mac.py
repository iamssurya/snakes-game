from setuptools import setup

APP = ['game.py']
DATA_FILES = [('',['images'])]
# OPTIONS = {'iconfile':'snake.png'}

setup(
    app = APP,
    data_files = DATA_FILES,
    setup_requires = ['py2app']
)
