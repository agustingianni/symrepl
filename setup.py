from setuptools import setup

setup(
    name="symrepl",
    version="1.0",
    url="https://github.com/agustingianni/symrepl",
    author="Agustin Gianni",
    author_email="agustin.gianni@gmail.com",
    description=("Symbol inspection REPL interface"),
    license="MIT",
    keywords="symbol repl",
    py_modules=["symrepl"],
    install_requires=[
        "prompt_toolkit",
        "pygments"
    ],
    entry_points="""
        [console_scripts]
        symrepl=symrepl:main
    """
)