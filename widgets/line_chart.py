import math
import typing
import numpy as np
from quive import *
from language import *

r = 3
max_width = 400
max_height = 350


class LineChart(Widget):
    def __init__(self, *args):
        super().__init__(*args)

        self.label_x = ''
        self.label_y = ''
        self.setMaximumSize(max_width, max_height)

        self.label = []
        self.x_value = []
        self.lines = [{
            'line': [0] * 8,
            'shape': 'none',
            'is_dash': False
        }]

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
        elif self.label[0].startswith('rc'):
            self.x_value = range(512, 256 * 9, 256)
            self.label_x = language('图像行数', 'Number of Rows')
        else:
            pass

        if self.maximum > 10000:
            for line in self.lines:
                line['line'] = [num / 1000 for num in line['line']]
            self.label_y = language('时间 / 秒', 'Time (s)')
        else:
            self.label_y = language('时间 / 毫秒', 'Time (ms)')

        self.update()

    @property
    def minimum(self):
        return min(map(lambda line: min(line['line']), self.lines))

    @property
    def maximum(self):
        return max(map(lambda line: max(line['line']), self.lines))

    def paint(self, painter: Painter):
        painter.setFont(QFont(language('SimSun', 'Times New Roman'), 12))

        w = self.width()
        h = self.height()
        text_width = int(30 * scaling.ratio)
        text_height = int(20 * scaling.ratio)

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

        y_min = math.floor(self.minimum / 100) * 100
        y_max = math.ceil(self.maximum / 100) * 100

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

        interval = (y_max - y_min) / 10
        vertical_labels = list(map(lambda v: '{:.0f}'.format(v), np.arange(y_min, y_max + 1, interval)))
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

        left_top = PointF(horizontal_min, vertical_max) + SizeF(5, 5)
        painter.setBrush(Qt.white)
        painter.setPen(Pen(Qt.black, 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawRect(QRectF(left_top, SizeF(162, 50)))

        current = left_top + SizeF(10, 10)
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_square(painter, current)
        painter.draw_text_right(current, '{}-{}'.format(self.method, language('设备1', 'i7')), margin=12)

        current += SizeF(0, 15)
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_triangle(painter, current)
        painter.draw_text_right(current, '{}-{}'.format(self.method, language('设备2', 'i5')), margin=12)

        current += SizeF(0, 15)
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_circle(painter, current)
        painter.draw_text_right(current, '{}-{}'.format(self.method, language('设备3', 'TX1')), margin=12)

        current = left_top + SizeF(90, 10)
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_square(painter, current)
        painter.draw_text_right(current, '{}-{}'.format(self.reversed_method, language('设备1', 'i7')), margin=12)

        current += SizeF(0, 15)
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_triangle(painter, current)
        painter.draw_text_right(current, '{}-{}'.format(self.reversed_method, language('设备2', 'i5')), margin=12)

        current += SizeF(0, 15)
        painter.setPen(Pen(QBrush(Qt.black), 1.5, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(current - SizeF(7, 0), current + SizeF(7, 0))
        self.draw_circle(painter, current)
        painter.draw_text_right(current, '{}-{}'.format(self.reversed_method, language('设备3', 'TX1')), margin=12)

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

    @staticmethod
    def draw_none(painter: Painter, point: PointF):
        pass


if __name__ == '__main__':
    w = LineChart()
    w.x_value = [1, 2, 3]
    w.lines = [{
        'line': [10, 20, 60],
        'shape': 'none',
        'is_dash': False
    }]
    w.label = ['1 Hz']
    w.process()
    w.method = 'DAS'
    w.reversed_method = 'RDAS'
    w.exec()
