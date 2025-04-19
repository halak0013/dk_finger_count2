import collections
import typing
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QSlider,
    QSpinBox,
)

from PyQt6.QtCore import pyqtBoundSignal, Qt

PYQT_SLOT = typing.Union[collections.abc.Callable[..., typing.Any], pyqtBoundSignal]


class CustomSlider(QWidget):
    def __init__(
        self,
        label,
        min_value,
        max_value,
        default_value,
        step_size,
        slot: "PYQT_SLOT",
    ):
        super().__init__()
        self.text = label
        self.label = QLabel(self.text + ": " + str(default_value))
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Orientation.Horizontal)  # Qt::Horizontal
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setValue(default_value)
        self.slider.setSingleStep(step_size)
        self.slot = slot
        self.slider.valueChanged.connect(self.value_changed)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        self.setLayout(layout)

    def value_changed(self, value):
        self.label.setText(self.text + ": " + str(value))
        self.slot(value)

class CustomSpiner(QWidget):
    def __init__(
        self,
        label,
        min_value,
        max_value,
        default_value,
        step_size,
        slot: "PYQT_SLOT",
    ):
        super().__init__()
        self.text = label
        self.label = QLabel(self.text)
        self.spiner = QSpinBox()
        self.spiner.setMinimum(min_value)
        self.spiner.setMaximum(max_value)
        self.spiner.setValue(default_value)
        self.spiner.setSingleStep(step_size)
        self.slot = slot
        self.spiner.valueChanged.connect(self.value_changed)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.spiner)
        self.setLayout(layout)

    def value_changed(self, value):
        self.label.setText(self.text)
        self.slot(value)