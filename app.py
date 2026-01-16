from gui.main_window import MainWindow
from db.database import init_db

if __name__ == "__main__":
    init_db()
    app = MainWindow()
    app.run()
