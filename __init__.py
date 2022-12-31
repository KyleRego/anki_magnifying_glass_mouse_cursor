from aqt import mw
from aqt.qt import *

config = mw.addonManager.getConfig(__name__)
zoomwidth = zoomheight = config["larger square side length (pixels)"]
width = height = config["smaller square side length (pixels)"]
pos_x_crosshair = config["positive-x crosshair length (pixels)"]
neg_x_crosshair = config["negative-x crosshair length (pixels)"]
pos_y_crosshair = config["positive-y crosshair length (pixels)"]
neg_y_crosshair = config["negative-y crosshair length (pixels)"]
timeout_interval = config["delay to turn off zoom mouse (milliseconds)"]

cursors_pushed_to_stack_per_shortcut = 10

class AnkiMagnifyingGlassMouseCursor():
    def __init__(self):
        self.timer = QTimer(mw)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.reset_zoom_mouse)
        self.cursors_on_stack = 0

    def handle_zoom_mouse_shortcut(self):
        self.persist_zoom_mouse()
        self.timer.start(timeout_interval)

    def persist_zoom_mouse(self):
        i = 0
        while i < cursors_pushed_to_stack_per_shortcut:
            parent: AnkiQt = mw
            point1: QPoint = QCursor.pos()
            point2: QPoint = parent.mapFromGlobal(point1)
            size = QSize(width, height)
            rectangle = QRect(point2, size)
            rectangle.moveCenter(point2)
            pixmap1: QPixmap = parent.grab(rectangle)

            painter = QPainter(pixmap1)
            midx, midy = width/2, height/2
            painter.drawLine(midx, midy-pos_y_crosshair, midx, midy+neg_y_crosshair)
            painter.drawLine(midx-neg_x_crosshair, midy, midx+pos_x_crosshair, midy)
            painter.end()

            enlarged_pixmap = pixmap1.scaled(zoomwidth, zoomheight)
            newcursor = QCursor(enlarged_pixmap)
            mw.app.setOverrideCursor(newcursor)
            i += 1
        self.cursors_on_stack += cursors_pushed_to_stack_per_shortcut

    def reset_zoom_mouse(self):
        while self.cursors_on_stack > 0:
            mw.app.restoreOverrideCursor()
            self.cursors_on_stack -= 1

anki_magnifying_glass_mouse_cursor = AnkiMagnifyingGlassMouseCursor()

action = QAction("Zoom Mouse", mw)
action.setShortcut("Alt+C")
action.triggered.connect(anki_magnifying_glass_mouse_cursor.handle_zoom_mouse_shortcut)
mw.form.menuTools.addAction(action)
