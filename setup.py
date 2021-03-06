from setuptools import find_packages, setup

setup(
    name='norilog',
    version='1.0.0',
    package=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    entry_points="""
        [console_scripts]
        norilog = norilog:main
    """,
)
