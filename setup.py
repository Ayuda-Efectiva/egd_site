from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

from egd_site import __version__ as version

setup(
	name='egd_site',
	version=version,
	description='Effective Altruism Day Website',
	author='Fundación Ayuda Efectiva',
	author_email='info_ayudaefectiva_org',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
