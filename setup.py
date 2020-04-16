from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['appdirs', 'PyQt5', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Michael Andrec/Ukrainian History and Education Center",
    author_email='m.andrec@ukrhec.org',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="Alternative opinionated GUI for FADGI BWFMetaEdit",
    entry_points={
        'console_scripts': [
            'autoBWF=autoBWF.autoBWF:main',
            'autolame=autoBWF.autolame:main',
            'autosplice=autoBWF.autosplice:main',
            'bwf2pbcore=autoBWF.bwf2pbcore:main',
            'bwf2csv=autoBWF.bwf2csv:main'
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    name='autoBWF',
    packages=find_packages(include=['autoBWF']),
    setup_requires=setup_requirements,
    url='https://github.com/Ukrainian-History/autoBWF',
    version='3.5.2',
    zip_safe=False,
)
