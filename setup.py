# -*- coding: utf-8 -*-

import setuptools

from inventree_template_fix.version import PLUGIN_VERSION

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="inventree-template-fix",

    version=PLUGIN_VERSION,

    author="Jordan Bush",

    author_email="jordan@bush.ax",

    description="Retroactively apply parameters to Parts that were added before a category template was created",

    long_description=long_description,

    long_description_content_type='text/markdown',

    keywords="inventree template fix",

    url="https://github.com/MrARM/inventree-template-fix",

    license="MIT",

    packages=setuptools.find_packages(),

    install_requires=[
    ],

    setup_requires=[
        "wheel",
        "twine",
    ],

    python_requires=">=3.6",

    entry_points={
        "inventree_plugins": [
            "TemplateFixPlugin = inventree_template_fix.fix_plugin:TemplateFixPlugin"
        ]
    },
)
