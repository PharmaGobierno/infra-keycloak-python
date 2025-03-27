import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements_list = ["python-keycloak==3.9.1", "pytest==8.3.5", "pytest-mock==3.14.0"]

LIB_NAME: str = "pharmagob-keycloak"


setuptools.setup(
    name=LIB_NAME,
    version="1.0.0",
    author="Luis Gerardo Fosado Baños",
    author_email="luis.fosado@gruposid.com.mx",
    description="keycloak Manager Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/PharmaGobierno/{LIB_NAME}.git",
    include_package_data=True,
    keywords="infra, keycloak, library, python",
    packages=setuptools.find_packages(),
    package_data={"": ["*.json"]},
    namespace_packages=["infra"],
    install_requires=requirements_list,
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.11",
    zip_safe=True,
    test_suite="tests",
)
