import os
from setuptools import find_packages, setup


VERSION = '1.0.0'
DESCRIPTION = 'A collection of utilities that makes working with Django and DRF easier.'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-custom-utils',
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author='Daniil Nizdolin',
    author_email='nizdolin@gmail.com',
    url='https://github.com/nizdolin/django-custom-utils',
    license='MIT License',
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'Django>=3.2',
        'django-filter>=22.1',
        'django-admin-list-filter-dropdown>=1.0.3',
        'djangorestframework>=3.9.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    project_urls={
        'Source': 'https://github.com/nizdolin/django-custom-utils',
    },
)
