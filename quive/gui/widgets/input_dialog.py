from .. import *


@ui_extension
class InputDialog(QInputDialog):
    @staticmethod
    def get_double(parent=None, title='Input Double Value', label='Value:',
                   default_value=None, decimals=1, minimum=1, maximum=1e9):
        input_dialog = QInputDialog(parent)
        input_dialog.setInputMode(InputDialog.DoubleInput)
        input_dialog.setWindowTitle(title)
        input_dialog.setLabelText(label)
        input_dialog.setOkButtonText("确定")
        input_dialog.setCancelButtonText("取消")
        input_dialog.setDoubleDecimals(decimals)
        input_dialog.setDoubleRange(minimum, maximum)
        input_dialog.setDoubleValue(default_value or minimum)
        input_dialog.setFont(parent.font())

        return default_value if not input_dialog.exec_() else input_dialog.doubleValue()

    @staticmethod
    def get_int(parent=None, title='Input Int Value', label='Value:',
                default_value=None, minimum=1, maximum=100):
        input_dialog = QInputDialog(parent)
        input_dialog.setInputMode(InputDialog.IntInput)
        input_dialog.setWindowTitle(title)
        input_dialog.setLabelText(label)
        input_dialog.setOkButtonText("确定")
        input_dialog.setCancelButtonText("取消")
        input_dialog.setIntRange(minimum, maximum)
        input_dialog.setIntValue(default_value or minimum)
        input_dialog.setFont(parent.font())

        return default_value if not input_dialog.exec_() else input_dialog.intValue()
