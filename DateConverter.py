import sys
import os
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtGui import QIcon
from ummalqura.hijri_date import HijriDate  # Library for Hijri date conversion
from datetime import date, datetime  # For handling Gregorian dates
from icon import Icon  # Custom icon handling class

class DateConverterApp(QWidget):
    """
    A PyQt5-based application for converting dates between Gregorian and Hijri calendars.
    """

    def __init__(self):
        """
        Initializes the DateConverterApp instance.
        Sets up the user interface and applies styles.
        """
        super().__init__()

        # Load the stylesheet for styling the app
        self.load_stylesheet("./dataConverter.qss")

        # Initialize the user interface components
        self.init_ui()

    def init_ui(self):
        """
        Sets up the user interface (UI) for the Date Converter app.
        Configures layouts, labels, input fields, and buttons.
        """
        layout = QVBoxLayout()  # Main layout

        # Create a horizontal layout for displaying today's Gregorian and Hijri dates
        label_layout = QHBoxLayout()

        # Display the current Gregorian date
        gregorianDate = date.today()
        self.gregorianDate_label = QLabel(f"Date: {gregorianDate}")
        label_layout.addWidget(self.gregorianDate_label)

        # Display the current Hijri date
        hijri_date = HijriDate.get_hijri_date(date.today())
        self.hijri_date_label = QLabel(f"Hijri: {hijri_date}")
        label_layout.addWidget(self.hijri_date_label)

        layout.addLayout(label_layout)  # Add labels to the main layout

        # Input field for entering a date to convert
        search_layout = QHBoxLayout()
        self.date_input_label = QLabel("Enter Date:")
        self.date_input_label.setAlignment(Qt.AlignCenter)
        search_layout.addWidget(self.date_input_label)

        self.date_input = QLineEdit()  # Input field for date entry
        search_layout.addWidget(self.date_input)

        layout.addLayout(search_layout)  # Add input section to the main layout

        # Create buttons for converting dates
        button_layout = QHBoxLayout()
        self.convert_to_hijri_button = QPushButton("Convert to Hijri")
        self.convert_to_hijri_button.clicked.connect(self.convert_to_hijri)
        button_layout.addWidget(self.convert_to_hijri_button)

        self.convert_to_gregorian_button = QPushButton("Convert to Gregorian")
        self.convert_to_gregorian_button.clicked.connect(self.convert_to_gregorian)
        button_layout.addWidget(self.convert_to_gregorian_button)

        layout.addLayout(button_layout)  # Add buttons to the main layout

        # Label for displaying conversion results or error messages
        self.result_display = QLabel("")
        self.result_display.setObjectName("result_display")
        layout.addWidget(self.result_display)

        self.setLayout(layout)  # Set the main layout for the window

    def convert_to_hijri(self):
        """
        Converts the entered Gregorian date to a Hijri date.
        Displays an error if the input is invalid.
        """
        date_input = self.date_input.text()

        if date_input:
            try:
                valid_data = self.convert_to_format(date_input)
                if valid_data == "Enter Valid Date":
                    raise ValueError("Invalid Date Format")

                hijri_result = HijriDate.get_hijri_date(valid_data)
                self.result_display.setText(f"Hijri Date: {hijri_result}")
            except Exception as e:
                self.result_display.setText(f"Error: {str(e)}")
        else:
            self.result_display.setText("Please Enter Date")

    def convert_to_gregorian(self):
        """
        Converts the entered Hijri date to a Gregorian date.
        Displays an error if the input is invalid.
        """
        date_input = self.date_input.text()

        if date_input:
            try:
                valid_data = self.convert_to_format(date_input)
                if valid_data == "Enter Valid Date":
                    raise ValueError("Invalid Date Format")

                gregorian_result = HijriDate.get_georing_date(valid_data)
                self.result_display.setText(f"Gregorian Date: {gregorian_result}")
            except Exception as e:
                self.result_display.setText(f"Error: {str(e)}")
        else:
            self.result_display.setText("Please Enter Date")

    def convert_to_format(self, date_str, output_format="%Y-%m-%d"):
        """
        Validates and converts an input date string to a standard format.
        Tries multiple formats to parse the date successfully.

        Parameters:
            date_str (str): The input date string.
            output_format (str): Desired output date format (default: "%Y-%m-%d").

        Returns:
            str: The formatted date or an error message if invalid.
        """
        input_formats = [
            "%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y",
            "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d",
            "%d.%m.%Y", "%m.%d.%Y", "%Y.%m.%d"
        ]

        for fmt in input_formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime(output_format)
            except ValueError:
                continue

        return "Enter Valid Date"

    def load_stylesheet(self, filepath):
        """
        Loads and applies a QSS stylesheet to the application.

        Parameters:
            filepath (str): Path to the QSS file.
        """
        file = QFile(filepath)
        if file.exists() and file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()
        else:
            print("Failed to load stylesheet: File not found or not accessible.")

class MainWindow(QWidget):
    """
    Main window that hosts the Date Converter App.
    """
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 400)
        icon_path = "./calendar.ico"
        self.app_icon = Icon(self, icon_path, app_name="Date Converter")
        self.form_table = DateConverterApp()

        layout = QVBoxLayout()
        layout.addWidget(self.form_table)
        self.setLayout(layout)

        css_path = self.resource_path("./dataConverter.qss")
        icon_path = self.resource_path("./calendar.ico")
        self.setWindowIcon(QIcon(icon_path))
        with open(css_path, "r") as css_file:
            self.setStyleSheet(css_file.read())

    def resource_path(self, relative_path):
        """
        Retrieves the absolute path for resources, compatible with PyInstaller packaging.
        """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
