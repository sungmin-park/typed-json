from setuptools import setup

setup(
    name='typed-json',
    version='0.0.1',
    packages=['typed_json'],
    install_requires=['typing-extensions>=3.7.4'],
    extras_require={'dev': ['pytest']}
)
