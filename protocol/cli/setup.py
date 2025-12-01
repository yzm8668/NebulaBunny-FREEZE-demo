from setuptools import setup

setup(
    name="nb-freeze",
    version="0.1.0",
    description="NebulaBunny FREEZE protocol CLI (protocol layer only)",
    author="NebulaBunny",
    packages=["nb_freeze"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "nb-freeze-generate-a=nb_freeze.generate_a:main",
            "nb-freeze-validate-a=nb_freeze.validate_a:main",
            "nb-freeze-validate-b=nb_freeze.validate_b:main",
        ]
    },
)
