"""Display translation progress information for multilingual projects.

This extension adds notes to documents that contain untranslated content,
informing readers about incomplete translations and linking to contribution
opportunities.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from docutils import nodes

import sphinx
from sphinx.locale import __
from sphinx.transforms import SphinxTransform
from sphinx.util import logging

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


class TranslationProgressNotifier(SphinxTransform):
    """Add translation progress notes to documents with untranslated content."""

    default_priority = 950  # After translation classes are added

    def apply(self, **kwargs: Any) -> None:
        from sphinx.builders.gettext import MessageCatalogBuilder

        # Skip for gettext builder
        if issubclass(self.env._builder_cls, MessageCatalogBuilder):
            return

        # Skip if extension is disabled
        if not self.config.translation_progress_classes:
            return

        # Get translation progress data
        progress_data = self.document.get('translation_progress')
        if not progress_data:
            return

        total = progress_data['total']
        translated = progress_data['translated']

        # Skip fully translated documents or documents with no translatable content
        if total == 0 or translated == total:
            return

        # Calculate progress percentage
        progress_percent = int((translated / total) * 100) if total > 0 else 0

        # Create note content
        message = self.config.translation_progress_message or __(
            'This document is {progress}% translated. '
            'Some content may appear in the original language. '
            'Help us improve the translation!'
        )
        
        # Format the message with current progress
        # Note: 'total' and 'translated' now represent word counts
        formatted_message = message.format(
            progress=progress_percent,
            translated=translated,
            total=total
        )

        # Create the note admonition
        note_node = nodes.note()
        note_node += nodes.paragraph(text=formatted_message)

        # Insert at the beginning of the document, after title if present
        insert_position = 0
        for i, child in enumerate(self.document.children):
            if isinstance(child, nodes.title):
                insert_position = i + 1
                break
            elif isinstance(child, (nodes.section, nodes.paragraph)):
                insert_position = i
                break

        self.document.insert(insert_position, note_node)


def setup(app: Sphinx) -> ExtensionMetadata:
    """Setup the translation progress extension."""
    # translation_progress_classes is already a built-in config value
    app.add_config_value('translation_progress_message', None, 'env', types=frozenset({str, type(None)}))
    
    app.add_transform(TranslationProgressNotifier)

    return {
        'version': sphinx.__display_version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }