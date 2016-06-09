from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='Stego',
    version='0.0.5',
    description=readme,
    author='Linqiang Ouyang (Jimmy)',
    author_email='jimmyou587@gmail.com',
    packages=['stego'],
    license='MIT',
    url='https://github.com/jimmyou587/stegno',
    classifiers=[
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
    keywords='python, steganography, image processing, security',
    install_requires=['pillow'],
    scripts=['bin/stege', 'bin/stegd'],
    test_suite='nose.collector',
    tests_require=['nose']
    )