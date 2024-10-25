from setuptools import setup, find_packages

setup(
    name='pyPrimeGenerator',
    version='1.0.0',
    description='A Prime Generator for Local and Distributed Computation',
    packages=find_packages(),
    install_requires=['sympy'],
    entry_points={
        'console_scripts': [
            'primegen-local=scripts.run_local:main',
            'primegen-distributed=scripts.run_distributed:main',
        ]
    },
)
