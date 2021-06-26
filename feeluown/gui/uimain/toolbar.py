from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QStackedWidget

from feeluown.gui.widgets.magicbox import MagicBox
from feeluown.gui.widgets.statusline import StatusLine, StatusLineItem
from feeluown.gui.widgets.statusline_items import PluginStatus, NotifyStatus


class ToolbarButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)


class BottomPanel(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app

        self._layout = QHBoxLayout(self)
        self.back_btn = ToolbarButton('⇦', self)
        self.forward_btn = ToolbarButton('⇨', self)
        self.magicbox = MagicBox(self._app)

        self._stack_switch = ToolbarButton('⁐', self)
        self._stacked_widget = QStackedWidget(self)
        self._stacked_widget.addWidget(self.magicbox)
        self._stack_switch.hide()

        self.status_line = StatusLine(self._app)

        # initialize widgets
        self.status_line.add_item(StatusLineItem('plugin', PluginStatus(self._app)))
        self.status_line.add_item(StatusLineItem('notify', NotifyStatus(self._app)))
        self.back_btn.setEnabled(False)
        self.forward_btn.setEnabled(False)

        self.back_btn.clicked.connect(self._app.browser.back)
        self.forward_btn.clicked.connect(self._app.browser.forward)

        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName('bottom_panel')

        self._layout.addWidget(self.back_btn)
        self._layout.addWidget(self.forward_btn)
        self._layout.addSpacing(80)
        self._layout.addWidget(self._stacked_widget)
        self._layout.addSpacing(5)
        self._layout.addWidget(self._stack_switch)
        # self._layout.addStretch(0)
        self._layout.addSpacing(80)
        self._layout.addWidget(self.status_line)

        # assume the magicbox height is about 30
        h_margin, v_margin = 5, 15
        height = self.magicbox.height()

        self.setFixedHeight(height + v_margin * 2)
        self._layout.setContentsMargins(h_margin, v_margin, h_margin, v_margin)
        self._layout.setSpacing(0)

    def add_stacked_widget(self, widget):
        self._stacked_widget.addWidget(widget)
        if self._stacked_widget.count() > 1:
            self._stack_switch.show()

    def clear_stacked_widget(self):
        while self._stacked_widget.count() > 0:
            self._stacked_widget.removeWidget(self._stacked_widget.currentWidget())
        self._stack_switch.hide()
