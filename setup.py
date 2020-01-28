from setuptools import setup

setup(
    name='typed-json',
    version='0.0.1',
    packages=['typed_json'],
    install_requires=['stringcase==1.2.0'],
    extras_require={'dev': ['pytest']}
)
