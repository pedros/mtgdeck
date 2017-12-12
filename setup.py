from setuptools import setup

setup(
    name='mtgdeck',
    packages=['mtgdeck'],
    version='0.0.6',
    description='MTG deck list decoder and encoder library and application',
    author='Pedro Silva',
    author_email='psilva+git@pedrosilva.pt',
    url='https://github.com/pedros/mtgdeck',
    download_url='https://github.com/pedros/mtgdeck/archive/0.0.6.tar.gz',
    keywords=[
        'magic-the-gathering',
        'parser',
        'encoder-decoder',
        'command-line-app',
        'library python3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Utilities'
    ],
    long_description=open('README.rst').read(),
    install_requires=['pyparsing'],
    tests_require=['pytest', 'pytest-cov', 'coverage', 'codecov'],
    entry_points={
        'console_scripts': [
            'mtgdeck=mtgdeck.__main__:main',
        ],
    },
)
