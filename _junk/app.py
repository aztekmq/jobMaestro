import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListView, QTextEdit, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import QTimer, QDate, QTime, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMenu, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PyQt6.QtGui import QColor, QPainterPath
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
import glob
import json
import os
import json


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("msa engineered devops enablement")
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()

        # Header
        # Header widget
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)  # Set the layout of the header widget
        header_widget.setObjectName("headerWidget")  # Give it a name for styling
        
        # ... (rest of the header content code)
                
        #header_layout = QHBoxLayout()
        #header_layout.setProperty("headerRole", "true")
                
        # Load PNC Bank icon
        icon_pixmap = QPixmap('pnc.png')
        icon_pixmap = icon_pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)  # for a 32x32 size, for instance
        icon_label = QLabel(self)
        icon_label.setPixmap(icon_pixmap)
        header_layout.addWidget(icon_label)


        # Title in the center
        title_label = QLabel("jobMaestro")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setProperty("fontRole", "title")

        #title_font = QFont()
        #title_font.setPointSize(200)
        #title_font.setBold(True)
        #title_label.setFont(title_font)        
        header_layout.addWidget(title_label, 1)  # the '1' here makes it take up more space, centering it
        
        # Date and Time on the far right
        self.date_label = QLabel(QDate.currentDate().toString())
        self.time_label = QLabel(QTime.currentTime().toString('hh:mm:ss'))
        date_time_layout = QVBoxLayout()
        date_time_layout.addWidget(self.date_label)
        date_time_layout.addWidget(self.time_label)
        header_layout.addLayout(date_time_layout)
        
        # layout.addLayout(header_layout)
        layout.addWidget(header_widget)  # Add the header widget to the main layout
        
        # Searchable navigation menu
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_btn = QPushButton("Search")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        
        self.nav_list = QListView()

        nav_main_layout = QVBoxLayout()
        nav_main_layout.addLayout(search_layout)
        nav_main_layout.addWidget(self.nav_list, 1)

        # Main content
        self.main_content = QTextEdit()
        
        # Combine navigation and main content
        nav_content_layout = QHBoxLayout()
        nav_content_layout.addLayout(nav_main_layout, 1)
        nav_content_layout.addWidget(self.main_content, 2)
        layout.addLayout(nav_content_layout)
        
        # Footer for status messages
        self.footer_label = QLabel("Status message here.")
        layout.addWidget(self.footer_label)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Update time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.setStyleSheet(self.get_styles())

        
        # Set up a QGraphicsView and QGraphicsScene for main content
        self.main_content = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.main_content.setScene(self.scene)
        layout.addWidget(self.main_content)

        # Load tiles from JSON files
        self.load_tiles_from_json()                

    def update_time(self):
        self.time_label.setText(QTime.currentTime().toString('hh:mm:ss'))

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
    
        addAction = contextMenu.addAction("Add")
        restoreAction = contextMenu.addAction("Restore")
        cancelAction = contextMenu.addAction("Cancel")
    
        action = contextMenu.exec(event.globalPos())
    
        if action == addAction:
            self.add_job_template()
    
        elif action == restoreAction:
            # Add your restore logic here if needed
            pass
    
        elif action == cancelAction:
            # Add your cancel logic here if needed
            pass
            
    def add_job_template(self):
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Job Template")
    
        layout = QVBoxLayout()
    
        # Creating the form with blank fields
        name_label = QLabel("Name:")
        name_edit = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(name_edit)
    
        description_label = QLabel("Description:")
        description_edit = QLineEdit()
        layout.addWidget(description_label)
        layout.addWidget(description_edit)
    
        module_label = QLabel("Module:")
        module_edit = QLineEdit()
        layout.addWidget(module_label)
        layout.addWidget(module_edit)
    
        icon_file_label = QLabel("Icon File:")
        icon_file_edit = QLineEdit()
        layout.addWidget(icon_file_label)
        layout.addWidget(icon_file_edit)
    
        # Add Save and Cancel buttons
        save_btn = QPushButton("Save")
        layout.addWidget(save_btn)
    
        dialog.setLayout(layout)
    
        # Connect the save button to save the form data to JSON
        save_btn.clicked.connect(lambda: self.save_to_json(name_edit.text(), description_edit.text(), module_edit.text(), icon_file_edit.text()))
    
        dialog.exec()
    
    def save_to_json(self, name, description, module, icon_file):
        data = {
            "jobTemplate": {
                "name": name,
                "description": description,
                "module": module,
                "iconFile": icon_file
            }
        }
    
        directory = "_jobTemplates"
        if not os.path.exists(directory):
            os.makedirs(directory)
    
        with open(f"{directory}/{name}.json", 'w') as file:
            json.dump(data, file)
    
    def load_tiles_from_json(self):
        x_offset = 10  # Initial x-coordinate for the first tile
        y_offset = 10  # Initial y-coordinate for the first tile

        for file in glob.glob('_jobTemplates/*.json'):
            with open(file, 'r') as json_file:
                data = json.load(json_file)
                # You can extract necessary information from the `data` if needed
                # For this example, we're just creating a tile for each JSON file

                # Create a rounded rectangle (tile) for each JSON
                rounded_rect_path = QPainterPath()
                rounded_rect_path.addRoundedRect(0, 0, 48, 48, 15, 15)
                tile = self.scene.addPath(rounded_rect_path, brush=QColor('#f58120'))
                
                self.scene.addItem(tile)
                tile.setPos(x_offset, y_offset)

                # Adjust the offsets for next tiles. For this example, I'm just increasing the x-coordinate.
                x_offset += 58  # 48 (width of tile) + 10 (space between tiles)

        # Set the scene rect to fit all items
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
                     
    
    def get_styles(self):
        return """
            QMainWindow {
                background-color: #F7F7F7;
            }
            #headerWidget {
                background-color: #f58120;
            }
            QLabel {
                font-size: 14px;
            }
            QLabel[fontRole="title"] {
                font-size: 36px;
                font-weight: normal;
            }     
            QLineEdit, QPushButton, QTextEdit {
                padding: 5px;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = App()
    mainWin.show()
    sys.exit(app.exec())