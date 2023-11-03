from setuptools import setup, find_packages

setup(
    name='AnalysisToolBox',
    description='A collection tools in Python for data collection and processing, statisitics, analytics, and intelligence analysis.',
    version='0.1.0',
    author='Kyle Protho',
    author_email='kyletprotho@gmail.com',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'dotenv',
        'folium',
        'fuzzywuzzy',
        'geopandas',
        'io',
        'Jinja2',
        'json',
        'Levenshtein',
        'lida',
        'lifelines',
        'mapclassify',
        'math',
        'matplotlib',
        'mlxtend',
        'numpy',
        'openai',
        'os',
        'pandas',
        'pygris',
        'PyPDF2',
        'pywin32',
        're',
        'requests',
        'scipy',
        'seaborn',
        'scikit-learn',  # sklearn
        'statsmodels',
        'tableone',
        'textwrap',
        'zipfile',
    ],
    entry_points={
        'console_scripts': [
            'analyze-data=analysis_toolbox.cli:main',
        ],
    },
)
