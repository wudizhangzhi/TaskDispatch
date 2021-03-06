#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/17 下午2:53
# @Author  : wudizhangzhi

from codecs import open  # To use a consistent encoding
from os import path

from setuptools import find_packages
from setuptools import setup

root_path = path.abspath(path.dirname(__file__))

with open(path.join(root_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='taskDispatch',
    version='1.0.0',
    description='task dispatch',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wudizhangzhi/django-params-validator',
    # Author details
    author='wudizhangzhi',
    author_email='yueyatianchong@qq.com',

    # Choose your license
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='redis, task',

    packages=find_packages(exclude=['tests']),
    install_requires=[]
)
