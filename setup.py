from setuptools import find_packages, setup
setup(
    name='quart_discord_oauth',
    packages=find_packages(),
    version='1.0.1',
    description='Discord OAuth Quart extension for APIs',
    author='Tert0',
    license='MIT',
    install_requires=[
        'quart',
        'cachetools',
        'requests'
    ],
    url='https://github.com/Tert0/Quart-Discord-OAuth',
)
