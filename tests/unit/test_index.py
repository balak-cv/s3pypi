from pathlib import Path

import pytest

from s3pypi.exceptions import S3PyPiError
from s3pypi.index import Index, Package

foo = Path("foo")
bar = Path("bar")


def test_parse_index(index_html):
    html, expected_packages = index_html
    assert Index.parse(html).packages == expected_packages


def test_render_index(index_html):
    expected_html, packages = index_html
    assert Index(packages).to_html() == expected_html


def test_add_package():
    pkg1 = Package("test", "0.0.1", {foo})
    pkg2 = Package("test", "0.0.2", {bar})

    index = Index({pkg1})
    index.add_package(pkg2)
    assert index.packages == {pkg1, pkg2}


def test_add_package_exists():
    pkg1 = Package("test", "0.0.1", {foo})
    pkg2 = Package("test", "0.0.1", {bar})

    index = Index({pkg1})
    with pytest.raises(S3PyPiError):
        index.add_package(pkg2)


def test_add_package_force():
    pkg1 = Package("test", "0.0.1", {foo})
    pkg2 = Package("test", "0.0.1", {bar})

    index = Index({pkg1})
    index.add_package(pkg2, force=True)

    assert len(index.packages) == 1
    assert next(iter(index.packages)).files == {foo, bar}


def test_directory_normalize_package_name():
    pkg = Package("company.test", "0.0.1", {foo})
    assert pkg.directory == "company-test"
