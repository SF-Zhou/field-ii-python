import field
import param
import numpy as np


class SyntheticApertureWorker(field.MatlabWorker):
    def run(self, para: param.Parameter, *args):
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

        phantom_positions, phantom_amplitudes = para.phantom
        result = self.e.scat_all(emit_aperture, receive_aperture,
                                 phantom_positions, phantom_amplitudes,
                                 para.sampling_frequency, para.data_length)

        self.e.xdc_free(emit_aperture)
        self.e.xdc_free(receive_aperture)
        return result
