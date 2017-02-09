import os
import field
import viewer
import simulate

para = simulate.Parameter()
para.load(os.path.join(os.path.dirname(__file__), 'configs', 'linear_array_imaging.json'))

pool = field.MatlabPool(engine_count=4)
task = list(range(1, para.line_count + 1))

image_data = pool.parallel(simulate.LinearArrayImagingWorker, task=task, args=(para,))
print(para.element_width * para.element_count)
viewer.viewer(image_data,
              width=para.element_width * para.line_count * 1000,
              height=80, dynamic_range=40)
