import setuptools

setuptools.setup(
    name='wow-mod-fetch',
    version='2021.01.09',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
