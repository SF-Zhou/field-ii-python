from . import *
from .. import QPainter, QColor, QPen, QRectF, Qt


class Painter(QPainter):
    def draw_text(self, text_rect: QRectF, text: str,
                  color: QColor=None,
                  background_color: QColor=None,
                  background_round_size: int=2):
        current_pen = self.pen()

        self.setPen(Qt.transparent)
        if background_color:
            self.setBrush(background_color)
            self.drawRoundedRect(text_rect, background_round_size, background_round_size)

        if color:
            self.setPen(QPen(color))
        else:
            self.setPen(current_pen)
        self.drawText(text_rect, Qt.AlignCenter, text)

        if color:
            self.setPen(current_pen)

    def draw_text_top(self, position: PointF, text: str,
                      margin: int=3,
                      color: QColor=None,
                      background_color: QColor=None,
                      background_color_round_size: int=2):
        text_size = SizeF.text_size(text, self.font())
        text_rect = text_size.to_rect(position - text_size.half_width().height_add(margin * scaling.ratio))

        self.draw_text(text_rect, text, color, background_color, background_color_round_size)

    def draw_text_bottom(self, position: PointF, text: str,
                         margin: int=3,
                         color: QColor=None,
                         background_color: QColor=None,
                         background_color_round_size: int=2):
        text_size = SizeF.text_size(text, self.font())
        text_rect = text_size.to_rect(position - text_size.half_width().height_set(-margin * scaling.ratio))

        self.draw_text(text_rect, text, color, background_color, background_color_round_size)

    def draw_text_left(self, position: PointF, text: str,
                       margin: int=3,
                       color: QColor=None,
                       background_color: QColor=None,
                       background_color_round_size: int=2):
        text_size = SizeF.text_size(text, self.font())
        text_rect = text_size.to_rect(position - text_size.half_height().width_add(margin * scaling.ratio))

        self.draw_text(text_rect, text, color, background_color, background_color_round_size)

    def draw_text_right(self, position: PointF, text: str,
                        margin: int=3,
                        color: QColor=None,
                        background_color: QColor=None,
                        background_color_round_size: int=2):
        text_size = SizeF.text_size(text, self.font())
        text_rect = text_size.to_rect(position - text_size.half_height().width_set(-margin * scaling.ratio))

        self.draw_text(text_rect, text, color, background_color, background_color_round_size)

    def draw_text_bottom_left(self, position: PointF, text: str,
                              margin: int=3,
                              color: QColor=None,
                              background_color: QColor=None,
                              background_color_round_size: int=2):
        text_size = SizeF.text_size(text, self.font())
        text_rect = text_size.to_rect(position - text_size.width_add(margin).height_set(-margin * scaling.ratio))

        self.draw_text(text_rect, text, color, background_color, background_color_round_size)

    def draw_text_bottom_right(self, position: PointF, text: str,
                               margin: int=3,
                               color: QColor=None,
                               background_color: QColor=None,
                               background_color_round_size: int=2):
        text_size = SizeF.text_size(text, self.font())
        text_rect = text_size.to_rect(position.x_add(margin).y_add(margin * scaling.ratio))

        self.draw_text(text_rect, text, color, background_color, background_color_round_size)
