"""PDF Sphinx builder using ReportLab."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import _last_modified_time
from sphinx.writers.pdf import PDFTranslator, PDFWriter

if TYPE_CHECKING:
    from collections.abc import Iterator

    from docutils import nodes

    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


class PDFBuilder(Builder):
    """Builds PDF output using ReportLab."""

    name = 'pdf'
    format = 'pdf'
    epilog = __('The PDF files are in %(outdir)s.')

    out_suffix = '.pdf'
    allow_parallel = True
    default_translator_class = PDFTranslator

    supported_image_types = ['image/png', 'image/jpeg', 'image/gif']
    supported_remote_images = False

    current_docname: str | None = None

    def init(self) -> None:
        """Initialize builder."""
        # section numbers for headings in the currently visited document
        self.secnumbers: dict[str, tuple[int, ...]] = {}

    def get_outdated_docs(self) -> Iterator[str]:
        """Get outdated documents."""
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = self.outdir / (docname + self.out_suffix)
            try:
                targetmtime = _last_modified_time(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = _last_modified_time(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except OSError:
                # source doesn't exist anymore
                pass

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        """Get target URI for a document."""
        return ''

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        """Write a document to PDF."""
        self.current_docname = docname
        self.secnumbers = self.env.toc_secnumbers.get(docname, {})

        # Create writer and translator
        writer = PDFWriter(self)
        # Set document and process it
        writer.document = doctree
        writer.translate()

        # Log the output
        if writer.output:
            logger.info(__('PDF written to %s'), writer.output)

    def finish(self) -> None:
        """Finish build."""
        pass


def setup(app: Sphinx) -> ExtensionMetadata:
    """Setup the PDF builder."""
    app.add_builder(PDFBuilder)

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
