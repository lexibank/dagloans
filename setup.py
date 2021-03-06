from setuptools import setup
import json


with open('metadata.json') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_dagloans',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_dagloans'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'beidasinitic=lexibank_dagloans:Dataset',
        ]
    },
    install_requires=[
        'pylexibank>=1.1.1',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
