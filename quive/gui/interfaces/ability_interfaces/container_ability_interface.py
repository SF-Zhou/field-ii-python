from .. import BaseInterface
from ... import run_deferred_function


class ContainerAbilityInterface(BaseInterface):
    def set_central_widget(self, w):
        return run_deferred_function('set_central_widget', self, w)

    def set_square_widget(self, w, spacing=0):
        return run_deferred_function('set_square_widget', self, w, spacing)

    def set_layout_spacing(self, spacing):
        return run_deferred_function('set_layout_spacing', self, spacing)

    def export_to_pdf(self, filename):
        return run_deferred_function('export_to_pdf', self, filename)

    def export_to_image(self, filename):
        return run_deferred_function('export_to_image', self, filename)
