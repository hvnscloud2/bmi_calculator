from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import sys

class BMICalculator(QMainWindow):
    # basic config
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI calculator")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(800, 600)
        default_font = QFont('Ebrima', 12)
        QApplication.setFont(default_font)
        self.background_image = QtGui.QPixmap("background.png")
        self.is_metric = True
        self.initUI()
        self.center()

    def initUI(self):
        # layout
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(50, 10, 50, 10)

        # title 
        layout.addSpacing(40)
        title_label = QLabel("BMI calculator")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 50px; color: black;")
        layout.addWidget(title_label)
        layout.addSpacing(40)

        # weight
        self.weight_label = QLabel("Enter your weight (kg):")
        self.weight_label.setStyleSheet("color: black;")
        self.weight_input = QLineEdit(self)
        self.weight_input.setPlaceholderText("e.g., 70")
        self.weight_input.setStyleSheet("font-size: 20px; padding: 5px;")
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)
        layout.addSpacing(20)

        # height
        self.height_label = QLabel("Enter your height (cm):")
        self.height_label.setStyleSheet("color: black;")
        self.height_input = QLineEdit(self)
        self.height_input.setPlaceholderText("e.g., 175")
        self.height_input.setStyleSheet("font-size: 20px; padding: 5px;")
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)

        # calculate button
        layout.addSpacing(40)
        self.calculate_button = QPushButton("Calculate", self)
        self.calculate_button.setStyleSheet("padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;")
        self.calculate_button.clicked.connect(self.bmi_calculation)
        layout.addWidget(self.calculate_button)
        layout.addSpacing(40)

        # result
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setMinimumHeight(50)
        layout.addWidget(self.result_label)

        # links
        links_layout = QHBoxLayout()
        links_layout.setAlignment(Qt.AlignCenter)
        layout.addSpacing(40)
        
        change_conversion_link = QLabel('<a href="#" style="color: black; text-decoration: none;">change conversion</a>')
        change_conversion_link.setStyleSheet("margin: 0 5px; font-size: 18px;")
        
        self.label = QLabel("|")
        self.label.setStyleSheet("margin: 0; font-size: 14px;")
        
        author_link = QLabel('<a href="https://linktr.ee/nhy6ck" style="color: black; text-decoration: none;">author</a>')
        author_link.setStyleSheet("margin: 0 5px; font-size: 18px;")

        links_layout.addWidget(change_conversion_link)
        change_conversion_link.mousePressEvent = lambda event: self.change_conversion()

        links_layout.addWidget(self.label)
        links_layout.addWidget(author_link)
        
        author_link.setOpenExternalLinks(True)
        
        layout.addLayout(links_layout)
        layout.addSpacing(20)
        
        # central widget 
        central_widget = QWidget()
        central_widget.setLayout(layout)
        
        self.setCentralWidget(central_widget)

    # bg image
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)
     
    # bmi calculation
    def bmi_calculation(self):
         try:
            if self.is_metric:
                weight = float(self.weight_input.text())
                height_cm = float(self.height_input.text())
                height_m = height_cm / 100.0
            else:
                weight_lb = float(self.weight_input.text())
                height_ft = float(self.height_input.text())
                height_m = (height_ft * 0.3048)
                weight = weight_lb * 0.453592
            
            bmi = weight / (height_m ** 2)
            classification = self.bmi_classification(bmi)
            self.result_label.setText(f"BMI: {bmi:.2f} - {classification}")
            self.result_label.setStyleSheet("color: black;")  
            self.weight_input.clear()
            self.height_input.clear()

         except ValueError:
            self.result_label.setText("Please enter valid numbers.")
            self.result_label.setStyleSheet("color: red;")  
    
    # bmi classification
    def bmi_classification(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
         
    # conversion
    def change_conversion(self):
        if self.is_metric:
            self.is_metric = False
            self.weight_label.setText("Enter your weight (pounds):")
            self.height_label.setText("Enter your height (feet):")
            self.weight_input.setPlaceholderText("e.g., 154")
            self.height_input.setPlaceholderText("e.g., 5.8")
            self.weight_input.clear()
            self.height_input.clear()
        else:
            self.is_metric = True
            self.weight_label.setText("Enter your weight (kg):")
            self.height_label.setText("Enter your height (cm):")
            self.weight_input.setPlaceholderText("e.g., 70")
            self.height_input.setPlaceholderText("e.g., 175")
            self.weight_input.clear()
            self.height_input.clear()

        for widget in [self.weight_label, self.height_label]:
            widget.adjustSize()

    # center the window
    def center(self):
        qr = self.frameGeometry()  
        cp = QDesktopWidget().availableGeometry().center()  
        qr.moveCenter(cp)  
        self.move(qr.topLeft())  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BMICalculator()
    window.show()
    sys.exit(app.exec_())