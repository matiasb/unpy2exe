from distutils.core import setup

setup(
    name='unpy2exe',
    version='0.3',
    description='Extract pyc files from py2exe executable.',
    keywords=['py2exe', 'pyc', 'extract'],
    author='Matias Bordese',
    author_email='mbordese@gmail.com',
    url='http://github.com/matiasb/unpy2exe',
    license='MIT',
    py_modules=['unpy2exe'],
    scripts=['unpy2exe'],
    install_requires=[
        'argparse',
        'pefile',
        'six',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
    ],
)
