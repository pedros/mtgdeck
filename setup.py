from setuptools import setup, find_packages

setup(
    name='mtgdeck',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version='0.0.7',
    description='MTG deck list decoder and encoder library and application',
    long_description=open('README.rst').read(),
    author='Pedro Silva',
    author_email='psilva+git@pedrosilva.pt',
    license='GPLv3',
    url='https://github.com/pedros/mtgdeck',
    download_url='https://github.com/pedros/mtgdeck/archive/0.0.7.tar.gz',
    keywords=[
        'magic-the-gathering',
        'parser',
        'encoder-decoder',
        'command-line-app',
        'library python3'
    ],
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Utilities'
    ],
    install_requires=['pyparsing', 'defusedxml'],
    tests_require=['codecov',
                   'coverage',
                   'pytest-cov',
                   'pytest-pep8',
                   'pytest'],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'mtgdeck=mtgdeck.__main__:main',
        ],
    },
)
