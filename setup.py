from setuptools import setup, find_packages

setup(
    name="owain_app",  # Replace with your own project name
    version="0.1.0",
    author="Your Name",  # Replace with your name
    author_email="your.email@example.com",  # Replace with your email
    description="A project to investigate LLM's rule articulation in classification tasks",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="http://github.com/yourusername/owain_app",  # Replace with your repository URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # List your project dependencies here
        "pydantic",
        "openai",
        "itertools",
        "json",
        "argparse",
        "os",
        "sklearn",
        "pytest",
        "poetry"
    ],
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

