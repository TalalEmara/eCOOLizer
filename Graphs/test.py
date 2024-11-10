import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QSlider
from signal_data import Signal
from cine_graph import CineGraph
from fourier_graph import FourierTransformGraph

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Signal Visualization")
        self.resize(1000, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create the CineGraph for input and output signals
        self.cine_graph1 = CineGraph("Input Signal")
        self.cine_graph2 = CineGraph("Output Signal")
        
        # Link the two CineGraphs 
        self.cine_graph1.link_with(self.cine_graph2)

        # Create the FourierTransformGraph 
        self.fourier_graph = FourierTransformGraph("Fourier Transform")

        layout.addWidget(self.cine_graph1)
        layout.addWidget(self.cine_graph2)
        layout.addWidget(self.fourier_graph)

        self.load_button = QPushButton("Load Signal")
        self.load_button.clicked.connect(self.load_signal)
        layout.addWidget(self.load_button)

        toggle_button = QPushButton("Toggle Audiogram Mode")
        toggle_button.clicked.connect(self.fourier_graph.toggle_audiogram_mode)
        layout.addWidget(toggle_button)

        play_button = QPushButton("Play")
        play_button.clicked.connect(lambda: (self.cine_graph1.play(), self.cine_graph2.play())) 
        layout.addWidget(play_button)

        pause_button = QPushButton("Pause")
        pause_button.clicked.connect(lambda: (self.cine_graph1.pause(), self.cine_graph2.pause())) 
        layout.addWidget(pause_button)

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(lambda: (self.cine_graph1.reset(), self.cine_graph2.reset())) 
        layout.addWidget(reset_button)

        speed_slider = QSlider(Qt.Horizontal)
        speed_slider.setMinimum(50) 
        speed_slider.setMaximum(500) 
        speed_slider.setValue(100)  # Default speed
        speed_slider.setValue(self.cine_graph1.playSpeed) 
        speed_slider.valueChanged.connect(lambda value: (self.cine_graph1.set_play_speed(value), self.cine_graph2.set_play_speed(value)))
        layout.addWidget(speed_slider)

        self.show()

    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.flac *.ogg)")
        if file_path:
            signal = Signal()
            signal.load_signal(file_path)
            
            self.cine_graph1.set_signal(signal)
            self.cine_graph2.set_signal(signal)
            self.fourier_graph.set_signal(signal)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())