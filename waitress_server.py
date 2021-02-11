from waitress import serve
import main
from src.window_type_updater import WindowTypeUpdater

updater = WindowTypeUpdater()
updater.start()
serve(main.app, host='0.0.0.0', port=9090)