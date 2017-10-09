try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='mdlecture',
    version='0.0.2',
    description='Generate PDF lecture slides from markdown',
    long_description=readme,
    url='https://github.com/hjalti/mdlecture/',
    author='Hjalti Magnússon',
    author_email='hjaltmann@gmail.com',
    license='MIT',
    packages=['mdlecture'],
    package_data={
        'mdlecture' : ['template/*']
    },
    install_requires=[
        'watchdog==0.8.3',
    ],
    entry_points={
        'console_scripts': [
            'mdl=mdlecture:main',
        ],
    },
)
