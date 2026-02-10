from setuptools import setup, find_packages

setup(
    name="lh-instruments",
    version="0.1.0",
    description="Python control for Keithley, SR830, and Zurich Instruments",
    author="HiSenBerG1019",
    packages=find_packages(),
    install_requires=[
        "pyvisa>=1.13.0",
        "pyvisa-py>=0.7.0",
        "zhinst>=21.8.0",
        "numpy>=1.21.0",
    ],
    python_requires=">=3.7",
)
