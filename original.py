import image
import pathlib
import numpy as np
from widgets import SimulateWidget


def main():
    p = pathlib.Path('figure/quality')
    p.mkdir(exist_ok=True)
    p = pathlib.Path('figure/fetus')
    p.mkdir(exist_ok=True)

    w = SimulateWidget()
    w.u_image = image.UImage(np.zeros((128, 1024)), (39.0144, 40.0), 15)

    needs = [
        (25, True, 'figure/quality/original_lateral_25mm.pdf'),
        (45, True, 'figure/quality/original_lateral_45mm.pdf'),
        (25, False, 'figure/quality/original_contrast_25mm.pdf'),
        (45, False, 'figure/quality/original_contrast_45mm.pdf'),
    ]

    for depth, is_lateral, file_path in needs:
        w.depth = depth
        w.is_lateral = is_lateral
        w.update()
        w.export_to_pdf(file_path)

    w.is_fetus = True
    w.u_image = image.UImage(np.zeros((128, 1024)), (78.0288, 55.0), 20.0)
    w.resize(1000, 717)
    w.update()
    w.export_to_pdf('figure/fetus/original_fetus.pdf')


if __name__ == '__main__':
    main()
