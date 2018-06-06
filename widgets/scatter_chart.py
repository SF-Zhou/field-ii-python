import math
import numpy as np
from quive import *

r = 4


class ScatterChart(Widget):
    def __init__(self, *args):
        super().__init__(*args)

        self.label_x = ''
        self.label_y = ''
        self.setMinimumSize(300, 150)
        # self.setMaximumSize(480, 360)

        self.label = []
        self.x_value = []
        self.points = []
        self.horizontal_threshold = 50.0
        self.vertical_threshold = 0.0

        self.horizontal_like = -1
        self.vertical_like = -1

        self.method = ''
        self.reversed_method = ''

        Shortcut('ctrl+w', self).excited.connect(self.close)
        self.background_color = Qt.white

    def add_points(self, points: list):
        self.points += points
        self.update()

    def process(self):
        self.x_value = list(range(0, 101, 10))
        self.label_x = '时间 / ms'

        self.update()

    @property
    def minimum(self):
        return min(map(lambda point: point[1], self.points))

    @property
    def maximum(self):
        return max(map(lambda point: point[1], self.points))

    def paint(self, painter: Painter):
        painter.setFont(QFont('SimSun', 12))

        sub = self.maximum - self.minimum
        if sub < 0.15:
            step = 0.01
        elif sub < 0.25:
            step = 0.02
        elif sub < 0.55:
            step = 0.04
        elif sub < 1.5:
            step = 0.1
        elif sub < 2.5:
            step = 0.2
        else:
            step = 0.3

        w = self.width()
        h = self.height()

        if step < 0.1:
            text_width = int(35 * scaling.ratio)
        else:
            text_width = int(30 * scaling.ratio)
        text_height = int(20 * scaling.ratio)

        # painter.drawText(QRect(0, 0, w, text_height), Qt.AlignCenter, self.title)
        painter.drawText(QRect(0, h - text_height, w, text_height), Qt.AlignCenter, self.label_x)
        # translate and rotate for paint vertical text
        painter.save()
        painter.translate(0, h)
        painter.rotate(-90)
        painter.drawText(QRect(0, 0, h, text_height), Qt.AlignCenter, self.label_y)
        painter.restore()

        # calculate min and max values #
        x_min = min(self.x_value)
        x_max = max(self.x_value)
        y_min = math.floor(self.minimum / step - 0.5) * step
        y_max = math.ceil(self.maximum / step + 0.5) * step

        horizontal_min = text_height + text_width
        horizontal_max = w - text_width / 2
        vertical_min = h - text_height * 2
        vertical_max = text_height

        # draw text on axis #
        horizontal_labels = list(map(str, self.x_value))
        horizontal_values = list(np.linspace(horizontal_min, horizontal_max, len(horizontal_labels)))
        for horizontal_x, label in zip(horizontal_values, horizontal_labels):
            if label == horizontal_labels[0] or label == horizontal_labels[-1]:
                painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                painter.setPen(Pen(QBrush(Qt.black), 0.8, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))

            current_point = PointF(horizontal_x, vertical_min)
            painter.draw_text_bottom(current_point, label, margin=2)

            if self.horizontal_threshold != float(label):
                painter.drawLine(current_point, PointF(horizontal_x, vertical_max))

        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin))
        percent_x = (self.horizontal_threshold - x_min) / (x_max - x_min)
        horizontal_threshold_pos = horizontal_max * percent_x + horizontal_min * (1 - percent_x)
        painter.drawLine(
            PointF(horizontal_threshold_pos, vertical_min),
            PointF(horizontal_threshold_pos, vertical_max)
        )

        format_str = '{:.2f}' if step < 0.1 else '{:.1f}'
        vertical_labels = list(map(lambda v: format_str.format(v), np.arange(y_min, y_max + 1e-5, step)))
        vertical_values = list(np.linspace(vertical_min, vertical_max, len(vertical_labels)))
        for vertical_pos, label in zip(vertical_values, vertical_labels):
            if label == vertical_labels[0] or label == vertical_labels[-1]:
                painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                painter.setPen(Pen(QBrush(Qt.black), 0.8, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))

            current_point = PointF(horizontal_min, vertical_pos)

            if label != vertical_labels[0]:
                painter.draw_text_left(current_point, label)

            if self.vertical_threshold != float(label):
                painter.drawLine(current_point, PointF(horizontal_max, vertical_pos))

        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin))
        percent_y = (self.vertical_threshold - y_min) / (y_max - y_min)
        vertical_threshold_pos = vertical_max * percent_y + vertical_min * (1 - percent_y)
        painter.drawLine(
            PointF(horizontal_min, vertical_threshold_pos),
            PointF(horizontal_max, vertical_threshold_pos)
        )

        if True:
            if self.horizontal_like == -1:
                block_horizontal_min = horizontal_min
                block_horizontal_max = horizontal_threshold_pos
            else:
                block_horizontal_min = horizontal_threshold_pos
                block_horizontal_max = horizontal_max

            if self.vertical_like == -1:
                block_vertical_min = vertical_min
                block_vertical_max = vertical_threshold_pos
            else:
                block_vertical_min = vertical_threshold_pos
                block_vertical_max = vertical_max

            painter.setPen(Pen(Qt.transparent))
            painter.setBrush(QBrush(QColor(200, 200, 200, 100)))
            painter.drawRoundedRect(QRectF(
                PointF(block_horizontal_min, block_vertical_min),
                PointF(block_horizontal_max, block_vertical_max)
            ), 0.0, 0.0)

        for point in self.points:
            x, y, label = point

            percent_x = (x - x_min) / (x_max - x_min)
            percent_y = (y - y_min) / (y_max - y_min)
            horizontal_pos = horizontal_max * percent_x + horizontal_min * (1 - percent_x)
            vertical_pos = vertical_max * percent_y + vertical_min * (1 - percent_y)
            current_point = PointF(horizontal_pos, vertical_pos)

            self.draw_label(painter, current_point, label)

        left_top = PointF(horizontal_max, vertical_max) + SizeF(-80, 5)

        painter.setBrush(Qt.white)
        painter.setPen(Pen(Qt.black, 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawRect(QRectF(left_top, SizeF(75, 185)))

        current = left_top + SizeF(10, 10) - SizeF(0, 15)
        labels = [
            'DAS-CPU', 'RDAS-CPU',
            'DAS-ARM', 'RDAS-ARM',
            'DAS-FPGA', 'RDAS-FPGA',
            'SA-CPU', 'RSA-CPU',
            'SA-ARM', 'RSA-ARM',
            'SA-FPGA', 'RSA-FPGA',
        ]

        for label in labels:
            current = current + SizeF(0, 15)
            self.draw_label(painter, current, label)
            painter.draw_text_right(current, label, margin=12)

        painter.end()

    @staticmethod
    def draw_circle(painter: Painter, point: PointF, line_style=Qt.SolidLine):
        painter.setPen(Pen(QBrush(Qt.black), 1.5, line_style, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawEllipse(QRectF(point - QSizeF(r, r), QSizeF(r * 2, r * 2)))

    @staticmethod
    def draw_triangle(painter: Painter, point: PointF, line_style=Qt.SolidLine):
        painter.setPen(Pen(QBrush(Qt.black), 1.5, line_style, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(Qt.transparent))

        a = r * 4.3 / 4
        b = r * 3.5 / 4
        painter.drawLine(point - SizeF(0, r), point + SizeF(+a, b))
        painter.drawLine(point - SizeF(0, r), point + SizeF(-a, b))
        painter.drawLine(point + SizeF(+a, b), point + SizeF(-a, b))

    @staticmethod
    def draw_square(painter: Painter, point: PointF, line_style=Qt.SolidLine):
        painter.setPen(Pen(QBrush(Qt.black), 1.5, line_style, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawRect(QRectF(point - SizeF(r, r), QSizeF(r * 2, r * 2)))

    def draw_label(self, painter: Painter, point: PointF, label: str):
        label = label.lower().replace('_', '-')
        if label.startswith('das') or label.startswith('rdas'):
            shape = 'square'
        else:
            shape = 'circle'
        shape_func = getattr(self, 'draw_{}'.format(shape))
        line_style = Qt.DotLine if label.startswith('r') else Qt.SolidLine
        device = label.split('-')[1][0].upper()

        shape_func(painter, point, line_style)
        painter.setFont(QFont('SimSum', 7))
        painter.draw_text_bottom(point, device, margin=-5.5)
        painter.setFont(QFont('SimSun', 12))
