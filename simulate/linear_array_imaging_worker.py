###########################################
# converted from Field II User Guide P.61 #
###########################################

import field
import numpy as np
from . import Parameter


class LinearArrayImagingWorker(field.MatlabWorker):
    def run(self, para: Parameter, *args):
        self.e.field_init()
        self.e.set_sampling(para.sampling_frequency)

        emit_aperture = self.e.xdc_linear_array(para.element_count,
                                                para.element_width,
                                                para.element_height,
                                                para.kerf, 1, 5, para.focus)

        ir = np.sin(2 * np.pi * para.transducer_frequency *
                    np.arange(0, 2 / para.transducer_frequency, 1 / para.sampling_frequency))
        impulse_response = ir * np.hanning(ir.size)

        self.e.xdc_impulse(emit_aperture, impulse_response)
        self.e.xdc_excitation(emit_aperture, ir)

        receive_aperture = self.e.xdc_linear_array(para.element_count,
                                                   para.element_width,
                                                   para.element_height,
                                                   para.kerf, 1, 5, para.focus)
        self.e.xdc_impulse(receive_aperture, impulse_response)
        phantom_positions, phantom_amplitudes = para.phantom

        result = []
        for i in self.task:
            print("calculate line {}".format(i))

            # find position for imaging
            x = (i - 1 - para.line_count / 2) * para.element_width

            # set the focus for this direction
            self.e.xdc_center_focus(emit_aperture, [x, 0, 0])
            self.e.xdc_focus(emit_aperture, [0], [x, 0, para.z_focus])
            self.e.xdc_center_focus(receive_aperture, [x, 0, 0])
            self.e.xdc_focus(receive_aperture, [0], [x, 0, para.z_focus])

            # set the active elements using the apodization
            apo_vector = np.r_[np.zeros(i - 1),
                               np.hamming(para.active_count),
                               np.zeros(para.element_count - para.active_count - i + 1)]
            self.e.xdc_apodization(emit_aperture, [0], apo_vector)
            self.e.xdc_apodization(receive_aperture, [0], apo_vector)
            rf_data = self.e.scat(emit_aperture, receive_aperture,
                                  phantom_positions, phantom_amplitudes,
                                  para.sampling_frequency)
            result.append(rf_data)
        self.e.xdc_free(emit_aperture)
        self.e.xdc_free(receive_aperture)
        return result
