from setuptools import setup
from setuptools import find_packages

setup(
	name='battery state notifier',
	version='1.0.0',
	author='Adrian Niewiadomski',
	packages=find_packages(exclude=('tests*',)),
	package_dir={'battery_state_notifier': 'battery_state_notifier'},
	package_data={'battery_state_notifier': ['icons/*.png']},
	entry_points={
		'console_scripts': [
			'battery_notifier = battery_state_notifier.main:main',
		],
	}
)
