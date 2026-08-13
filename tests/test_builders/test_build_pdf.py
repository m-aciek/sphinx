"""Test the build process with PDF builder with the test root."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Any

    from sphinx.testing.util import SphinxTestApp


def with_pdf_app(*args: Any, **kw: Any) -> pytest.MarkDecorator:
    return pytest.mark.sphinx(*args, buildername='pdf', testroot='build-pdf', **kw)


@with_pdf_app()
def test_basic_pdf_build(app: SphinxTestApp) -> None:
    """Test that PDF builder can build a basic document."""
    app.build()
    
    # Check that PDF file was created
    pdf_file = app.outdir / 'index.pdf'
    assert pdf_file.exists()
    assert pdf_file.stat().st_size > 0


@with_pdf_app()
def test_pdf_content(app: SphinxTestApp) -> None:
    """Test that PDF contains expected content."""
    app.build()
    
    pdf_file = app.outdir / 'index.pdf'
    assert pdf_file.exists()
    
    # Try to verify PDF content using pypdf if available
    try:
        from pypdf import PdfReader
        
        with open(pdf_file, 'rb') as f:
            pdf = PdfReader(f)
            assert len(pdf.pages) > 0
            
            # Extract text from first page
            text = pdf.pages[0].extract_text()
            
            # Check that some expected content is present
            assert 'Test PDF Document' in text
            assert 'Section 1' in text
    except ImportError:
        # If pypdf is not available, just check file exists and has size
        pytest.skip("pypdf not available for content verification")
