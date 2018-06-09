import math
import typing
import numpy as np
from quive import *
from language import language, chinese

r = 3
max_width = 400
max_height = 350


class QualityChart(Widget):
    def __init__(self, *args):
        super().__init__(*args)

        self.label_x = ''
        self.label_y = ''
        self.setMinimumSize(300, 150)
        self.setMaximumSize(max_width, max_height)

        self.label = []
        self.x_value = []
        self.lines = []

        self.method = ''
        self.reversed_method = ''

        Shortcut('ctrl+w', self).excited.connect(self.close)
        self.background_color = Qt.white

    def add_line(self, label: typing.List[str], line: typing.List[float],
                 shape: str, is_dash: bool):
        self.label = label
        self.lines.append({
            'line': line,
            'shape': shape,
            'is_dash': is_dash
        })
        self.update()

    def process(self):
        if self.label[0].endswith('Hz'):
            self.x_value = range(10, 90, 10)
            self.label_x = language('频率 / MHz', 'Frequency (MHz)')
        elif self.label[0].startswith('ec') or self.label[0].startswith('lc'):
            self.x_value = range(32, 32 * 9, 32)
            self.label_x = language('阵元数目', 'Number of Elements')
            if len(self.label) == 7:
                self.x_value = range(64, 32 * 9, 32)
        elif self.label[0].startswith('rc'):
            self.x_value = range(512, 256 * 9, 256)
            self.label_x = language('图像行数', 'Number of Rows')
        else:
            pass

        self.update()

    @property
    def minimum(self):
        return min(map(lambda line: min(line['line']), self.lines))

    @property
    def maximum(self):
        return max(map(lambda line: max(line['line']), self.lines))

    def paint(self, painter: Painter):
        painter.setFont(QFont(language('SimSun', 'Times New Roman'), 12))

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
        y_min = math.floor(self.minimum / step) * step
        y_max = math.ceil(self.maximum / step) * step

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
            painter.drawLine(current_point, PointF(horizontal_x, vertical_max))

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
            painter.drawLine(current_point, PointF(horizontal_max, vertical_pos))

        for line in self.lines:
            previous_point = None
            nums = line['line']

            shape = line['shape']
            shape_func = getattr(self, 'draw_{}'.format(shape))
            l = Qt.DotLine if line['is_dash'] else Qt.SolidLine

            for x, y in zip(self.x_value, nums):
                percent_x = (x - x_min) / (x_max - x_min)
                percent_y = (y - y_min) / (y_max - y_min)
                horizontal_pos = horizontal_max * percent_x + horizontal_min * (1 - percent_x)
                vertical_pos = vertical_max * percent_y + vertical_min * (1 - percent_y)
                current_point = PointF(horizontal_pos, vertical_pos)

                shape_func(painter, current_point)
                if previous_point:
                    painter.setPen(Pen(QBrush(Qt.black), 1.5, l, Qt.RoundCap, Qt.RoundJoin))
                    painter.drawLine(previous_point, current_point)
                previous_point = current_point

        left_width = 17 + SizeF.text_size('{}-45mm'.format(self.method), painter.font()).w
        right_width = 17 + SizeF.text_size('{}-45mm'.format(self.reversed_method), painter.font()).w
        legend_width = 3 + left_width + 5 + right_width

        if 'mm' in self.label_y:
            left_top = PointF(horizontal_max, vertical_max) + SizeF(-(legend_width + 5), 5)
        else:
            left_top = PointF(horizontal_max, vertical_min) + SizeF(-(legend_width + 5), -40)

        painter.setBrush(Qt.white)
        painter.setPen(Pen(Qt.black, 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawRect(QRectF(left_top, SizeF(legend_width, 35)))

        current = left_top + SizeF(10, 10)
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_circle(painter, current)
        painter.draw_text_right(current, '{}-25mm'.format(self.method), margin=12)

        current += SizeF(0, 15)
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_square(painter, current)
        painter.draw_text_right(current, '{}-45mm'.format(self.method), margin=12)

        current = left_top + SizeF(left_width + 5 + 7, 10)
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_circle(painter, current)
        painter.draw_text_right(current, '{}-25mm'.format(self.reversed_method), margin=12)

        current += SizeF(0, 15)
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_square(painter, current)
        painter.draw_text_right(current, '{}-45mm'.format(self.reversed_method), margin=12)

        painter.end()

    @staticmethod
    def draw_circle(painter: Painter, point: PointF):
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawEllipse(QRectF(point - QSizeF(r, r), QSizeF(r * 2, r * 2)))

    @staticmethod
    def draw_triangle(painter: Painter, point: PointF):
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(Qt.transparent))

        a = r * 4.3 / 4
        b = r * 3.5 / 4
        painter.drawLine(point - SizeF(0, r), point + SizeF(+a, b))
        painter.drawLine(point - SizeF(0, r), point + SizeF(-a, b))
        painter.drawLine(point + SizeF(+a, b), point + SizeF(-a, b))

    @staticmethod
    def draw_square(painter: Painter, point: PointF):
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawRect(QRectF(point - SizeF(r, r), QSizeF(r * 2, r * 2)))
