from setuptools import setup, find_packages

setup(
    name='autoBWF',
    version='3.2',
    packages=find_packages("src"),
    install_requires=[
        'appdirs',
        'PyQT5',
    ],
    entry_points={
        'console_scripts': ['autoBWF=autoBWF.autoBWF:main',
                            'autolame=autoBWF.autolame:main'],
    }
)
