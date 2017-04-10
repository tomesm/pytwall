from setuptools import setup, find_packages


with open('README') as f:
    long_description = ''.join(f.readlines())

NAME = 'pytwall'

setup(
    name=NAME,
    version='0.1',
    description='Python Twiter Wall',
    long_description='An application using the Twitter REST API and OAuth showing tweets based on a given query.',
    author='Martin Tomes',
    author_email='tomesm@gmail.com',
    keywords='twitter, wall',
    license='Public Domain',
    url='https://github.com/tomesm/pytwall',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        ],
    zip_safe=False,
    install_requires=['Flask', 'jinja2', 'click>=6', 'requests'],
    package_data={
        NAME:['templates/*.html'],
    },
    entry_points={
        'console_scripts':[
            'pytwall_demo = pytwall:run',
        ],
    },
)
