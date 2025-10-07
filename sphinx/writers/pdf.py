"""Custom docutils writer for PDF using ReportLab."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes, writers

from sphinx import addnodes
from sphinx.locale import _, admonitionlabels
from sphinx.util.docutils import SphinxTranslator

if TYPE_CHECKING:
    from typing import Any

    from docutils.nodes import Element

    from sphinx.builders.pdf import PDFBuilder


class PDFWriter(writers.Writer):
    """Writer for PDF output using ReportLab."""

    supported = ('pdf',)
    settings_spec = ('No options here.', '', ())
    settings_defaults: dict[str, Any] = {}

    output: str

    def __init__(self, builder: PDFBuilder) -> None:
        super().__init__()
        self.builder = builder

    def translate(self) -> None:
        visitor = self.builder.create_translator(self.document, self.builder)
        self.document.walkabout(visitor)
        self.output = visitor.body if visitor.body else ''


class PDFTranslator(SphinxTranslator):
    """Translator for PDF output using ReportLab."""

    def __init__(self, document: nodes.document, builder: PDFBuilder) -> None:
        super().__init__(document, builder)
        self.builder: PDFBuilder = builder
        self.body: str = ''
        self.elements: list[dict[str, Any]] = []
        self.section_level = 0

    def visit_document(self, node: Element) -> None:
        """Start of document."""
        pass

    def depart_document(self, node: Element) -> None:
        """End of document - generate PDF."""
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

        # Create PDF
        pdf_path = self.builder.outdir / (self.builder.current_docname + '.pdf')
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Get styles
        styles = getSampleStyleSheet()
        story = []

        # Process elements and build PDF
        for element in self.elements:
            element_type = element.get('type')
            content = element.get('content', '')

            if element_type == 'title':
                style = styles['Title']
                story.append(Paragraph(content, style))
                story.append(Spacer(1, 12))
            elif element_type == 'heading':
                level = element.get('level', 1)
                if level == 1:
                    style = styles['Heading1']
                elif level == 2:
                    style = styles['Heading2']
                else:
                    style = styles['Heading3']
                story.append(Paragraph(content, style))
                story.append(Spacer(1, 12))
            elif element_type == 'paragraph':
                style = styles['Normal']
                story.append(Paragraph(content, style))
                story.append(Spacer(1, 12))
            elif element_type == 'pagebreak':
                story.append(PageBreak())

        # Build PDF
        if story:
            doc.build(story)

        self.body = str(pdf_path)

    def visit_section(self, node: Element) -> None:
        """Enter a section."""
        self.section_level += 1

    def depart_section(self, node: Element) -> None:
        """Leave a section."""
        self.section_level -= 1

    def visit_title(self, node: Element) -> None:
        """Visit title node."""
        if isinstance(node.parent, nodes.document):
            # Document title
            self.elements.append({
                'type': 'title',
                'content': self.encode(node.astext()),
            })
        else:
            # Section heading
            self.elements.append({
                'type': 'heading',
                'level': self.section_level,
                'content': self.encode(node.astext()),
            })
        raise nodes.SkipNode

    def visit_paragraph(self, node: Element) -> None:
        """Visit paragraph node."""
        self.elements.append({
            'type': 'paragraph',
            'content': self.encode(node.astext()),
        })
        raise nodes.SkipNode

    def visit_Text(self, node: nodes.Text) -> None:
        """Visit text node."""
        pass

    def depart_Text(self, node: nodes.Text) -> None:
        """Depart text node."""
        pass

    def visit_literal_block(self, node: Element) -> None:
        """Visit literal block."""
        self.elements.append({
            'type': 'paragraph',
            'content': self.encode(node.astext()),
        })
        raise nodes.SkipNode

    def visit_bullet_list(self, node: Element) -> None:
        """Visit bullet list."""
        pass

    def depart_bullet_list(self, node: Element) -> None:
        """Depart bullet list."""
        pass

    def visit_list_item(self, node: Element) -> None:
        """Visit list item."""
        self.elements.append({
            'type': 'paragraph',
            'content': '• ' + self.encode(node.astext()),
        })
        raise nodes.SkipNode

    def visit_emphasis(self, node: Element) -> None:
        """Visit emphasis."""
        pass

    def depart_emphasis(self, node: Element) -> None:
        """Depart emphasis."""
        pass

    def visit_strong(self, node: Element) -> None:
        """Visit strong."""
        pass

    def depart_strong(self, node: Element) -> None:
        """Depart strong."""
        pass

    def unknown_visit(self, node: Element) -> None:
        """Handle unknown nodes."""
        pass

    def unknown_departure(self, node: Element) -> None:
        """Handle unknown node departures."""
        pass

    def encode(self, text: str) -> str:
        """Encode text for PDF."""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
