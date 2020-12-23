import pytest

from s3pypi.index import Index


@pytest.fixture(
    scope="function",
    params=[
        (
            "s3pypi",
            {
                f"s3pypi-{version}{suffix}"
                for version in (
                    "0",
                    "0!0",
                    "0+local",
                    "0.0",
                    "0.1.1",
                    "0.1.2",
                    "0.dev0",
                    "0.post0",
                    "0a0",
                    "0rc0",
                )
                for suffix in (
                    ".tar.gz",
                    "-py2-none-any.whl",
                )
            },
        )
    ],
)
def index_html(request, data_dir):
    index_name, filenames = request.param
    with open(data_dir / "index" / f"{index_name}.html") as f:
        html = f.read().strip()
        yield html, filenames


def test_parse_index(index_html):
    html, expected_filenames = index_html
    index = Index.parse(html)
    assert index.filenames == expected_filenames


def test_render_index(index_html):
    expected_html, filenames = index_html
    html = Index(filenames).to_html()
    assert html == expected_html
