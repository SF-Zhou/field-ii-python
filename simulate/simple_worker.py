###########################################
# converted from Field II User Guide P.56 #
###########################################

import field
import param
import numpy as np


class SimpleWorker(field.MatlabWorker):
    def run(self, para: param.Parameter, *args):
        self.e.field_init()
        self.e.set_sampling(para.sampling_frequency)

        aperture = self.e.xdc_linear_array(para.element_count,
                                           para.element_width,
                                           para.element_height,
                                           para.kerf, 2, 3, para.focus)

        # Set the impulse response and excitation of the emit aperture
        ir = np.sin(2 * np.pi * para.transducer_frequency *
                    np.arange(0, 2 / para.transducer_frequency, 1 / para.sampling_frequency))
        impulse_response = ir * np.hanning(ir.size)

        self.e.xdc_impulse(aperture, impulse_response)
        self.e.xdc_excitation(aperture, ir)

        v, _ = self.e.calc_scat_multi(aperture, aperture,
                                      np.array([0, 0, 20]) / 1000,
                                      np.array([1]))
        # Free space for apertures
        self.e.xdc_free(aperture)

        return v
