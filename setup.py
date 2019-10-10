from setuptools import setup
from os import path

base_dir = path.abspath(path.dirname(__file__))
with open(path.join(base_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='exacto',
    version='0.2.2',
    description='Python tools for splitting strings.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/arthexis/exacto',
    download_url='https://github.com/arthexis/exacto/archive/v0.2.2.tar.gz',
    author='Rafael Guillén',
    author_email='arthexis@gmail.com',
    license='MIT',
    keywords=["UTILS", "SPLIT", "STRING"],
    packages=['exacto'],
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    extras_require={
        'dev': [
            'pytest',
            'black',
            'pytest-cov'
        ]
    }
)
