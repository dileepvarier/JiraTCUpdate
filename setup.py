from distutils.core import setup

setup(
    name='EasyTestAPI',
    version='V1.0.0',
    description='Plugin to execute REST API Automation testing',
    author='Dileep P B',
    author_email='dileep.pulinkavuvariath.balasubramannian@sap.com',
    install_requires=["requests >= 2.28.2", "pandas >= 1.5.3","openpyxl>=3.1.2","pip"],
    packages=[''],
    include_package_data=True
)