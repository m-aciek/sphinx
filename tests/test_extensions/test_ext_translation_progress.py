"""Test sphinx.ext.translation_progress extension."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx(
    'html',
    testroot='intl',
    freshenv=True,
    confoverrides={
        'extensions': ['sphinx.ext.translation_progress'],
        'language': 'xx',
        'locale_dirs': ['.'],
        'gettext_compact': False,
        'translation_progress_classes': True,
    },
    copy_test_root=True,
)
def test_translation_progress_note_added(app: SphinxTestApp) -> None:
    """Test that translation progress note is added to documents with untranslated content."""
    app.build(filenames=[app.srcdir / 'translation_progress.txt'])
    
    # Check the HTML output for the translation progress note
    content = (app.outdir / 'translation_progress.html').read_text(encoding='utf8')
    
    # Should contain a note about translation progress
    assert 'This document is' in content and 'translated' in content


@pytest.mark.sphinx(
    'html',
    testroot='intl',
    freshenv=True,
    confoverrides={
        'extensions': ['sphinx.ext.translation_progress'],
        'language': 'xx',
        'locale_dirs': ['.'],
        'gettext_compact': False,
        'translation_progress_classes': True,
        'translation_progress_message': 'Custom: {progress}% done ({translated}/{total})',
    },
    copy_test_root=True,
)
def test_translation_progress_custom_message(app: SphinxTestApp) -> None:
    """Test that custom translation progress message is used."""
    app.build(filenames=[app.srcdir / 'translation_progress.txt'])
    
    content = (app.outdir / 'translation_progress.html').read_text(encoding='utf8')
    
    # Should contain custom message format
    assert 'Custom:' in content and 'done' in content


@pytest.mark.sphinx(
    'html',
    testroot='intl',
    freshenv=True,
    confoverrides={
        'extensions': ['sphinx.ext.translation_progress'],
        'language': 'xx',
        'locale_dirs': ['.'],
        'gettext_compact': False,
        'translation_progress_classes': False,
    },
    copy_test_root=True,
)
def test_translation_progress_disabled(app: SphinxTestApp) -> None:
    """Test that no note is added when translation_progress_classes is disabled."""
    app.build(filenames=[app.srcdir / 'translation_progress.txt'])
    
    content = (app.outdir / 'translation_progress.html').read_text(encoding='utf8')
    
    # Should not contain translation progress note
    assert not ('This document is' in content and 'translated' in content)


@pytest.mark.sphinx(
    'gettext',
    testroot='intl',
    freshenv=True,
    confoverrides={
        'extensions': ['sphinx.ext.translation_progress'],
        'language': 'xx',
        'locale_dirs': ['.'],
        'gettext_compact': False,
        'translation_progress_classes': True,
    },
    copy_test_root=True,
)
def test_translation_progress_skipped_for_gettext(app: SphinxTestApp) -> None:
    """Test that no processing occurs for gettext builder."""
    app.build(filenames=[app.srcdir / 'translation_progress.txt'])
    
    # For gettext builder, no HTML output to check, but should build without error
    assert app.statuscode == 0


@pytest.mark.sphinx(
    'html',
    testroot='intl',
    freshenv=True,
    confoverrides={
        'extensions': ['sphinx.ext.translation_progress'],
        'language': 'xx',
        'locale_dirs': ['.'],
        'gettext_compact': False,
        'translation_progress_classes': True,
    },
    copy_test_root=True,
)
def test_translation_progress_fully_translated_skipped(app: SphinxTestApp) -> None:  
    """Test that no note is added to fully translated documents."""
    # Build a document that should be fully translated
    app.build(filenames=[app.srcdir / 'bom.txt'])
    
    content = (app.outdir / 'bom.html').read_text(encoding='utf8')
    
    # Should not contain translation progress note for fully translated documents
    assert not ('This document is' in content and 'translated' in content)