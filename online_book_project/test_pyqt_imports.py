import sys
try:
    import PyQt5
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    print("PyQt5 OK", PyQt5.QtCore.PYQT_VERSION_STR)
except Exception as e:
    print("IMPORT ERROR:", repr(e))
print("sys.executable:", sys.executable)
