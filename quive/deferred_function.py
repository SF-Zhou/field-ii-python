from . import *
from PyQt5.QtPrintSupport import QPrinter


@deferred_define
def set_central_widget(self: Widget, widget):
    if isinstance(widget, WidgetController):
        widget = widget.w
    if not isinstance(widget, QWidget):
        raise TypeError('Only Support Widget or WidgetController')

    if isinstance(self, QMainWindow):
        self.setCentralWidget(widget)
    elif isinstance(self, QDockWidget):
        self.setWidget(widget)
    else:
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        self.setLayout(layout)
    self.center_widget = widget


@deferred_define
def set_square_widget(self: Widget, widget: Widget, spacing=0):
    if isinstance(widget, WidgetController):
        widget = widget.w
    if not isinstance(widget, QWidget):
        raise TypeError('Only Support Widget or WidgetController')

    layout = SquareLayout()
    layout.setSpacing(spacing)
    layout.addWidget(widget)
    self.setLayout(layout)
    self.center_widget = widget


@deferred_define
def set_layout_spacing(self: Widget, spacing):
    layout = self.layout()
    assert isinstance(layout, SquareLayout)
    layout.setSpacing(spacing)
    layout.update()


@deferred_define
def export_to_pdf(self: Widget, filename: str):
    p = QPicture()
    painter = QPainter(p)
    self.render(painter, QPoint(0, 0))
    painter.end()

    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(filename)

    painter = QPainter()
    ok = painter.begin(printer)
    if ok:
        painter.drawPicture(0, 0, p)
        ok = painter.end()
    return ok


@deferred_define
def export_to_image(self: Widget, filename: str):
    if filename.endswith('pdf'):
        return export_to_pdf(self, filename)

    p = QPixmap(*self.size)
    painter = QPainter(p)
    self.render(painter, QPoint(0, 0))
    painter.end()

    return p.save(filename)
