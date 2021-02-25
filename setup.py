from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sqlalchemy-sugar',
    version='0.1.0',
    description='select/delete wrapper for SQLAlchemy Asyncio',
    long_description=readme,
    author='Akira Yoshiyama',
    author_email='akirayoshiyama@gmail.com',
    url='https://github.com/yosshy/sqlalchemy-sugar',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)

