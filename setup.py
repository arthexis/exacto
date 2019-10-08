from setuptools import setup

setup(
    name='exacto',
    version='0.2.1',
    description='Python tools for splitting strings.',
    url='http://github.com/arthexis/exacto',
    download_url='https://github.com/arthexis/exacto/archive/v0.2.1.tar.gz',
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
