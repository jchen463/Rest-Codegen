from setuptools import setup

setup(
    setup_requires=['pbr>=1.9', 'setuptools>=17.1'],
    pbr=True,
    version='0.1dev',
    packages=['codegen', ],
    license='asdf',
    entry_points={
        'console_scripts': [
            'codegen=codegen.main:main',
        ],
    },
)
