#######################################
# converted from das.m by Jinhui Chen #
#######################################

import field
import numpy as np
from . import Parameter


class MultiScatWorker(field.MatlabWorker):
    def run(self, para: Parameter, *args):
        self.e.field_init()
        self.e.set_sampling(para.sampling_frequency)

        emit_aperture = self.e.xdc_linear_array(para.element_count,
                                                para.element_width,
                                                para.element_height,
                                                para.kerf, 1, 5, para.focus)

        excitation = np.sin(2 * np.pi * para.transducer_frequency * np.arange(
            0, 1 / para.transducer_frequency, 1 / para.sampling_frequency))
        impulse_response = excitation * np.hanning(excitation.size)
        self.e.xdc_impulse(emit_aperture, impulse_response)
        self.e.xdc_excitation(emit_aperture, excitation)

        receive_aperture = self.e.xdc_linear_array(para.element_count,
                                                   para.element_width,
                                                   para.element_height,
                                                   para.kerf, 1, 5, para.focus)
        self.e.xdc_impulse(receive_aperture, impulse_response)
        self.e.xdc_focus_times(receive_aperture, [0], np.zeros(para.element_count))

        phantom_positions, phantom_amplitudes = para.phantom

        result = []
        for i in self.task:
            print("calculate line {}".format(i))
            x = (i - para.line_count / 2 + 1 / 2) * para.pixel_width

            # set the focus for this direction
            self.e.xdc_center_focus(emit_aperture, [x, 0, 0])
            self.e.xdc_focus(emit_aperture, [0], [x, 0, para.z_focus])

            # set the active elements using the apodization
            apo_vector = np.zeros(para.element_count)
            apo_vector[i:i + para.active_count] = np.hamming(para.active_count)

            self.e.xdc_apodization(emit_aperture, [0], apo_vector)
            rf_data = self.e.scat_multi(emit_aperture, receive_aperture,
                                        phantom_positions, phantom_amplitudes,
                                        para.sampling_frequency)
            result.append(rf_data)
        self.e.xdc_free(emit_aperture)
        self.e.xdc_free(receive_aperture)
        return result
