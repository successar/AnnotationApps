import setuptools

setuptools.setup(
    name="Annotation-Apps",
    version="0.1",
    author="Sarthak Jain",
    author_email="successar@gmail.com",
    description="",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8",
    install_requires=[
        "streamlit >= 0.71",
        "sqlalchemy"
    ],
)