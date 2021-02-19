from setuptools import find_packages, setup
setup(
    name='quart_discord_oauth',
    packages=find_packages(),
    version='1.0.0',
    description='Discord OAuth Quart extension for APIs',
    author='Tert0',
    license='MIT',
    install_requires=[
        'quart',
        'cachetools',
        'requests'
    ],
)
