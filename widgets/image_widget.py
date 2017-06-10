import image
import numpy as np
from quive import *


class ImageWidget(Widget):
    gray_color_table = [qRgb(i, i, i) for i in range(256)]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_color = Qt.white
        self.qim = QImage()

        self.short_cut = Shortcut('ctrl+w', self)
        self.short_cut.excited.connect(self.close)

    @property
    def u_image(self) -> image.UImage:
        return self.attach(lambda: None)

    @u_image.setter
    def u_image(self, u_image: image.UImage):
        self.assign(u_image)

        im = u_image.pixel
        self.qim = QImage(im.flatten(), *im.T.shape, QImage.Format_Indexed8)
        self.qim.setColorTable(self.gray_color_table)

        self.update()

    def update_u_image(self, u_image: image.UImage):
        self.u_image = u_image

    def paint(self, painter: Painter):
        painter.setFont(QFont('Times New Roman'))
        if self.u_image is None:
            return

        w, h = self.size
        text_size = (45, 20)
        text_width, text_height = text_size
        image_width, image_height = self.u_image.size

        w -= text_width + 5
        h -= int(text_height * 1.5)
        painter.translate(*text_size)

        expected_h = int(w / image_width * image_height)
        if expected_h > h:
            expected_w = int(h / image_height * image_width)
            painter.translate((w - expected_w) // 2, 0)
            w = expected_w
        else:
            painter.translate(0, (h - expected_h) // 2)
            h = expected_h

        half_image_width = image_width / 2
        for x in np.arange(0, half_image_width + 1e-5, 10):
            percent = (half_image_width + x) / image_width

            painter.drawLine(PointF(w * percent, 0), PointF(w * percent, -4))
            painter.draw_text_top(PointF(w * percent, 0), "{} mm".format(int(x)),
                                  margin=5, background_color=Qt.white)

            percent = 1 - percent
            painter.drawLine(PointF(w * percent, 0), PointF(w * percent, -4))
            painter.draw_text_top(PointF(w * percent, 0), "{} mm".format(-int(x)),
                                  margin=5, background_color=Qt.white)

        z_start = self.u_image.z_start
        for y in np.arange(0, image_height + 1e-5, 10):
            percent = y / image_height

            painter.drawLine(PointF(0, h * percent), PointF(-4, h * percent))
            painter.draw_text_left(PointF(0, h * percent), "{} mm".format(int(y + z_start)),
                                   margin=8, background_color=Qt.white)

        painter.drawLine(PointF(0, 0), PointF(0, h))
        painter.drawLine(PointF(0, 0), PointF(w, 0))
        painter.drawImage(QRect(0, 0, w, h), self.qim)
