import sys
import setuptools

from mimic.openstack.common import setup

requires = setup.parse_requirements()
depend_links = setup.parse_dependency_links()


setuptools.setup(
    name="mimic",
    version="0.1",
    description="OpenStack Load Balancer Server",
    long_description="OpenStack Load Balancer Server",
    url='https://github.com/jiangwt100/mimic',
    license='Apache',
    author='Jim Jiang',
    author_email='jiangwt100@gmail.com',
    packages=setuptools.find_packages(exclude=['bin', 'tests', 'tools']),
    dependency_links=depend_links,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=requires,
    scripts=[
        'bin/mimic-server',
    ],
)
