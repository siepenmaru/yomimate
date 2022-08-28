from PyQt5 import QtCore

"""
Static methods for widgets with drag drop capability
"""
class DragDropWidget():
    """
    drag and drop signal handling adapted from
    https://learndataanalysis.org/how-to-implement-image-drag-and-drop-feature-pyqt5-tutorial/
    """
    @staticmethod
    def dragEnterEvent(event):
        if event.mimeData().hasImage:
            event.accept()
            return True
        else:
            event.ignore()
            return False

    @staticmethod
    def dragMoveEvent(event):
        if event.mimeData().hasImage:
            event.accept()
            return True
        else:
            event.ignore()
            return False

    @staticmethod
    def dropEvent(event) -> str | None:
        if event.mimeData().hasImage:
            event.setDropAction(QtCore.Qt.CopyAction)
            try:
                file_path = event.mimeData().urls()[0].toLocalFile()
                if file_path:
                    event.accept()
                    return file_path
                else:
                    event.ignore()
                    return None
            except:
                event.ignore()
                return None
        else:
            event.ignore()
            return None
