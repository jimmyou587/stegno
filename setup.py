from setuptools import setup

with open('README.md') as readme:
    description = readme.read()

setup(
    name='Stego',
    version='0.0.1',
    description='Hide your secret',
    author='Linqiang Ouyang (Jimmy)',
    author_email='jimmyou587@gmail.com',
    packages=['stego'],
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    # What does your project relate to?
    keywords='python, steganography',
    install_requires=['pillow'],
    scripts=['bin/stege', 'bin/stegd'],
    test_suite='nose.collector',
    tests_require=['nose']
    )