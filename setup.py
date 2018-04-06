from setuptools import setup


with open('README.md') as f:
    long_description = f.read()


setup(
    name='unpy2exe',
    version='0.4',
    description='Extract pyc files from py2exe executable.',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
