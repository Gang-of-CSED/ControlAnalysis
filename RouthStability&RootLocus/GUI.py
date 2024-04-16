import sys
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QSizePolicy
from PyQt5.QtGui import QFont, QColor, QTextDocument, QIcon
from PyQt5.QtCore import Qt

from Routh import RouthHerwitzCriterion, getPolynomialCoefficients, prepareString, getSystemPoles
from RootLocus import plotRootLocus, getPolesandZeros

class RouthHerwitzApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Routh-Hurwitz Criterion & Root Locus Plotter")
        self.setWindowIcon(QIcon('assets/logo.png'))
        self.setGeometry(100, 100, 1000, 600)
        self.setFont(QFont("Arial", 12))  # Set default font for the entire GUI

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        left_layout = QVBoxLayout()
        layout.addLayout(left_layout)

        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)

        self.polynomial_label = QLabel("Denominator:")
        input_layout.addWidget(self.polynomial_label)

        self.polynomial_entry = QLineEdit()
        self.polynomial_entry.setPlaceholderText("Example: s^2 + 3*s + 5")
        self.polynomial_entry.setFixedWidth(500)  
        input_layout.addWidget(self.polynomial_entry)

        self.numerator_label = QLabel("Numerator (optional):")
        
        input_layout.addWidget(self.numerator_label)

        self.numerator_entry = QLineEdit()
        self.numerator_entry.setPlaceholderText("Example: s + 1, Default: 1")
        self.numerator_entry.setFixedWidth(500)
        input_layout.addWidget(self.numerator_entry)
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        self.calculate_button.setFixedWidth(130)  
        self.calculate_button.setFixedHeight(30)
        self.calculate_button.setFont(QFont("Arial", 11))
        self.calculate_button.setStyleSheet("background-color: #e8ebef; color: black; border: 1px solid #666f79; border-radius: 10px;")
        self.calculate_button.setCursor(Qt.PointingHandCursor)
        input_layout.addWidget(self.calculate_button)

        left_layout.addWidget(input_widget)
        self.table_label = QLabel("Routh-Hurwitz Table:")
        self.table_label.setFont(QFont("Arial", 12))
        self.table_label.hide()
        left_layout.addWidget(self.table_label)

        self.table = QTableWidget()
        # remove the focus border
        self.table.setFocusPolicy(0)
        self.table.setStyleSheet("QTableWidget::item:focus { border: none; }")
        
        # remove the border
        self.table.setFrameStyle(0)
        self.table.setWindowTitle("Routh-Hurwitz Table")
        left_layout.addWidget(self.table)

        self.output_label = QLabel()
        self.output_label.setFont(QFont("Arial", 12))
        left_layout.addWidget(self.output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFrameStyle(0)
        left_layout.addWidget(self.output_text)

        self.canvas = None

    def calculate(self):
        denominator_string = self.polynomial_entry.text()
        numerator_string = self.numerator_entry.text()
        denominator_string = prepareString(denominator_string)
        numerator_string = prepareString(numerator_string)
        denominator = getPolynomialCoefficients(denominator_string)
        if numerator_string:
            temp = getPolynomialCoefficients(numerator_string)
            if temp:
                numerator = temp
            else:
                self.numerator_entry.setText('')
                numerator = [1]
        else:
            numerator = [1]
        if len(numerator) > len(denominator):
            self.numerator_entry.setText('')
            numerator = [1]
        table, sign_changes = RouthHerwitzCriterion(denominator)
        # poles = getSystemPoles(denominator_string)
        poles, zeros = getPolesandZeros(denominator, numerator)
        poles = {pole: np.count_nonzero(poles == pole) for pole in poles}
        zeros = {zero: np.count_nonzero(zeros == zero) for zero in zeros}
        output = ""
        output += f"Number of sign changes (Roots in the RHP): {sign_changes}\n"
        output += "System Poles:\n"
        print(poles)
        for pole in poles:
            # print each pole with only 4 decimal places
            output += f'  {sp.N(pole, 4)}'
            if poles[pole] > 1:
                output += f' with multiplicity {poles[pole]}'
            output += '\n'
        if zeros:
            output += "System Zeros:\n"
            for zero in zeros:
                output += f'  {sp.N(zero, 4)}'
                if zeros[zero] > 1:
                    output += f' with multiplicity {zeros[zero]}'
                output += '\n'

        self.output_text.setPlainText(output)

        self.plot_root_locus(denominator, numerator)

        self.display_routh_table(table)

        # Update output label color based on stability
        if table is None:
            self.table_label.setText("Invalid input for Routh-Hurwitz Criterion")
            self.table_label.setStyleSheet("color: red")
            self.table.clear()
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.table.hide()
            if poles == [] or getPolynomialCoefficients(denominator_string) == []:
                self.output_label.setText("Invalid input")
                self.table_label.hide()
                self.output_label.setStyleSheet("color: red")
                self.output_text.setPlainText("")
                self.output_label.setFont(QFont("Arial", 12, QFont.Bold))
            else:
                unstable_poles = 0
                for pole in poles:
                    if pole.real > 0:
                        unstable_poles += 1
                if unstable_poles == 0:
                    self.output_label.setText("System is stable")
                    self.output_label.setStyleSheet("color: green")
                else:
                    self.output_label.setText("System isn't stable")
                    self.output_label.setStyleSheet("color: red")
                output = "System Poles:\n"
                for pole in poles:
                    output += f'  {sp.N(pole, 4)}'
                    if poles[pole] > 1:
                        output += f' with multiplicity {poles[pole]}'
                    output += '\n'
                if zeros:
                    output += "System Zeros:\n"
                    for zero in zeros:
                        output += f'  {sp.N(zero, 4)}'
                        if zeros[zero] > 1:
                            output += f' with multiplicity {zeros[zero]}'
                        output += '\n'
                self.output_text.setPlainText(output)

        elif sign_changes == 0:
            self.table_label.show()
            self.table.show()
            self.output_label.setText("System is stable")
            self.output_label.setStyleSheet("color: green")
        else:
            self.table_label.show()
            self.table.show()
            self.output_label.setText("System isn't stable")
            self.output_label.setStyleSheet("color: red")

    def display_routh_table(self, table):
        if table is None:
            self.table.clear()
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            #self.table_label.hide()
            self.table.hide()
            return
        self.table_label.setText("Routh-Hurwitz Table:")
        self.table_label.setStyleSheet("color: black")
        self.table_label.show()
        self.table.show()
        n = len(table)
        self.table.setRowCount(n)
        self.table.setColumnCount(len(table[0]))
        # Set row labels as s^n, s^(n-1), ...
        for i in range(n):
            item = QTableWidgetItem(f's^{n-i-1}')
            self.table.setVerticalHeaderItem(i, item)
            

        # Remove column labels
        self.table.setHorizontalHeaderLabels([])

        for i in range(len(table)):
            for j in range(len(table[0])):
                value = sp.N(table[i][j], n=4)
                if j == 0:
                    if value < 1e-14 and value > -1e-14:
                        item = QTableWidgetItem("ε")
                    elif value > 1e14:
                        item = QTableWidgetItem("∞")
                    elif value < -1e14:
                        item = QTableWidgetItem("-∞")
                    else:
                        item = QTableWidgetItem(str(value))
                else:
                    item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

                # Increase font size
                font = QFont()
                font.setPointSize(12)
                item.setFont(font)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        # table size is adjusted to fit the contents
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

    def plot_root_locus(self, denominator, numerator):
        if self.canvas:
            self.canvas.hide()
            if hasattr(self, 'toolbar'):
                self.toolbar.hide()
        plt.clf()
        if not denominator or len(denominator) < 2:
            if self.canvas:
                self.canvas.hide()
                if hasattr(self, 'toolbar'):
                    self.toolbar.hide()
            return
        plotRootLocus(denominator, numerator)
        if hasattr(self, 'plot_widget'):
            self.centralWidget().layout().removeWidget(self.plot_widget)
            self.plot_widget.deleteLater()
        self.canvas = FigureCanvas(plt.gcf())
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("background-color: #e8ebef; color: black; border: 1px solid #666f79; border-radius: 10px; padding: 5px; margin: 0 5px; font-size: 17px;")


        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.plot_widget = QWidget()
        self.plot_widget.setLayout(layout)
        # fix shrinking issue
        self.plot_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.centralWidget().layout().addWidget(self.plot_widget)
        self.canvas.show()
        self.toolbar.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RouthHerwitzApp()
    window.setStyleSheet("background-color: #e8ebef;")  # Set background color of the window
    for widget in window.findChildren(QWidget):
        if not isinstance(widget, QPushButton):
            widget.setStyleSheet("background-color: transparent;")  # Make widgets transparent
    window.show()
    sys.exit(app.exec_())