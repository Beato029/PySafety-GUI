import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDockWidget, 
                             QWidget, QVBoxLayout, QTabWidget, QToolBar,
                             QStatusBar, QMenuBar, QMenu, QLabel,
                             QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
                             QGraphicsItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import (QPalette, QColor, QAction, QPainter, 
                        QPen, QBrush, QFont)

class EntityNode(QGraphicsEllipseItem):
    def __init__(self, node_id, name, node_type, x, y):
        super().__init__(-25, -25, 50, 50)
        self.node_id = node_id
        self.name = name
        self.node_type = node_type
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setBrush(self.get_node_color(node_type))
        self.setPen(QPen(Qt.GlobalColor.white, 2))
        
    def get_node_color(self, node_type):
        """Restituisce i colori IDENTICI al codice Palantir originale"""
        colors = {
            'person': QColor(255, 107, 107),      # Rosso - John Doe, Jane Smith
            'organization': QColor(78, 205, 196), # Verde acqua - Tech Corp, Data Inc
            'location': QColor(69, 183, 209),     # Blu - New York
            'event': QColor(150, 206, 180),       # Verde - Q1 Meeting
            'project': QColor(254, 202, 87),      # Giallo - Project Alpha
            'default': QColor(119, 140, 163)      # Grigio
        }
        return colors.get(node_type, colors['default'])
        
    def paint(self, painter, option, widget):
        """Disegna il nodo con testo CENTRATO come nel codice originale"""
        super().paint(painter, option, widget)
        painter.setFont(QFont("Arial", 8))
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.name)

class GraphEngine(QGraphicsView):
    def __init__(self):
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.nodes = {}
        self.edges = []
        
        # Carica gli stessi nodi del codice Palantir originale
        self.load_palantir_nodes()
        
    def load_palantir_nodes(self):
        """Carica gli STESSI nodi del codice Palantir originale"""
        sample_nodes = [
            {'id': '1', 'name': 'John Doe', 'type': 'person'},
            {'id': '2', 'name': 'Tech Corp', 'type': 'organization'},
            {'id': '3', 'name': 'New York', 'type': 'location'},
            {'id': '4', 'name': 'Q1 Meeting', 'type': 'event'},
            {'id': '5', 'name': 'Project Alpha', 'type': 'project'},
            {'id': '6', 'name': 'Data Inc', 'type': 'organization'},
            {'id': '7', 'name': 'Jane Smith', 'type': 'person'},
        ]
        
        # Posizioni simili al codice originale (layout circolare)
        positions = [
            (0, 0),     # John Doe - centro
            (150, -100), # Tech Corp - alto destra
            (-150, -100), # New York - alto sinistra
            (0, 150),    # Q1 Meeting - basso centro
            (150, 100),  # Project Alpha - basso destra
            (-150, 100), # Data Inc - basso sinistra
            (100, -150)  # Jane Smith - alto destra
        ]
        
        for i, node_data in enumerate(sample_nodes):
            x, y = positions[i]
            self.add_node(node_data, x, y)
            
        # Aggiungi connessioni come nel codice originale
        self.add_connections()
        
    def add_node(self, node_data, x, y):
        """Aggiunge un nodo alla posizione specificata"""
        node = EntityNode(
            node_data['id'], 
            node_data['name'],
            node_data['type'],
            x, y
        )
        self.nodes[node_data['id']] = node
        self.scene.addItem(node)
        
    def add_connections(self):
        """Aggiunge connessioni tra i nodi come nel codice originale"""
        connections = [
            ('1', '2'),  # John Doe -> Tech Corp
            ('1', '3'),  # John Doe -> New York
            ('1', '4'),  # John Doe -> Q1 Meeting
            ('2', '6'),  # Tech Corp -> Data Inc
            ('1', '7'),  # John Doe -> Jane Smith
            ('2', '5'),  # Tech Corp -> Project Alpha
        ]
        
        for source_id, target_id in connections:
            if source_id in self.nodes and target_id in self.nodes:
                source = self.nodes[source_id]
                target = self.nodes[target_id]
                
                # Crea linea di connessione come nel codice originale
                line = self.scene.addLine(
                    source.pos().x(), source.pos().y(),
                    target.pos().x(), target.pos().y(),
                    QPen(QColor(255, 255, 255, 100), 2, Qt.PenStyle.DashLine)
                )
                self.edges.append(line)

class PalantirDockWidget(QDockWidget):
    def __init__(self, title):
        super().__init__(title)
        # Crea un widget vuoto ma con lo stesso stile di Palantir
        empty_widget = QWidget()
        empty_widget.setStyleSheet("background-color: #353535;")
        self.setWidget(empty_widget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Palantir Desktop - Intelligence Platform")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Applica tema scuro IDENTICO a Palantir
        self.apply_palantir_theme()
        
        # Setup dell'UI completa come Palantir
        self.setup_ui()
        
    def apply_palantir_theme(self):
        """Applica il tema scuro identico al codice Palantir originale"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        
        self.setPalette(dark_palette)
        
        # STILE CSS IDENTICO al codice Palantir originale
        self.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #3daee9;
            }
            QToolBar {
                background-color: #404040;
                border: none;
                spacing: 5px;
                padding: 5px;
            }
            QStatusBar {
                background-color: #2b2b2b;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #555;
                background-color: #404040;
            }
            QTabBar::tab {
                background-color: #353535;
                color: white;
                padding: 8px 15px;
                border: 1px solid #555;
            }
            QTabBar::tab:selected {
                background-color: #3daee9;
                color: black;
            }
            QDockWidget {
                background-color: #353535;
                color: white;
            }
            QDockWidget::title {
                background-color: #2b2b2b;
                padding: 5px;
            }
            QTreeWidget, QTableWidget, QTextEdit, QListView {
                background-color: #353535;
                color: white;
                border: 1px solid #555;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: white;
                padding: 5px;
                border: 1px solid #555;
            }
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: 1px solid #555;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QLineEdit, QComboBox {
                background-color: #353535;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QGroupBox {
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
    def setup_ui(self):
        """Setup completo dell'interfaccia come Palantir originale"""
        
        # =============================================================================
        # MENU BAR - Identico a Palantir
        # =============================================================================
        menubar = self.menuBar()
        
        # File Menu - Stesse voci del codice originale
        file_menu = menubar.addMenu('&File')
        file_menu.addAction('&New Project', self.dummy_action)
        file_menu.addAction('&Open Data', self.dummy_action)
        file_menu.addSeparator()
        file_menu.addAction('E&xit', self.close)
        
        # Analysis Menu - Stesse voci del codice originale
        analysis_menu = menubar.addMenu('&Analysis')
        analysis_menu.addAction('&Machine Learning', self.dummy_action)
        analysis_menu.addAction('&Network Analysis', self.dummy_action)
        analysis_menu.addAction('&Statistical Report', self.dummy_action)
        
        # View Menu - Stesse voci del codice originale
        view_menu = menubar.addMenu('&View')
        view_menu.addAction('&Reset Layout', self.dummy_action)

        # =============================================================================
        # TOOLBAR - Identico a Palantir
        # =============================================================================
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Bottoni azioni principali - Stessi del codice originale
        toolbar.addAction('📊 Load Data', self.dummy_action)
        toolbar.addAction('🤖 ML Analysis', self.dummy_action)
        toolbar.addAction('🔄 Layout', self.apply_graph_layout)
        toolbar.addSeparator()
        
        # Ricerca - Stesso del codice originale
        search_label = QLabel("Search:")
        toolbar.addWidget(search_label)
        
        search_box = QLabel("Search entities...")  # Placeholder
        search_box.setMaximumWidth(200)
        toolbar.addWidget(search_box)
        
        toolbar.addSeparator()
        
        # Selezione algoritmo - Stesso del codice originale
        algo_label = QLabel("Clustering")
        toolbar.addWidget(algo_label)

        # =============================================================================
        # CENTRAL WIDGET - Tab principale con GRAPH ENGINE come Palantir originale
        # =============================================================================
        self.tab_widget = QTabWidget()
        
        # Tab 1: Object Graph - Con i CERCHI e NOMI del codice originale
        self.graph_tab = QWidget()
        graph_layout = QVBoxLayout(self.graph_tab)
        
        # Aggiungi il Graph Engine con i nodi Palantir
        self.graph_engine = GraphEngine()
        graph_layout.addWidget(self.graph_engine)
        
        self.tab_widget.addTab(self.graph_tab, "🎯 Object Graph")
        
        # Tab 2: Analytics Dashboard - Stesso nome del codice originale  
        analytics_tab = QWidget()
        analytics_tab.setStyleSheet("background-color: #404040;")
        self.tab_widget.addTab(analytics_tab, "📈 Analytics")
        
        # Tab 3: Timeline - Stesso nome del codice originale
        timeline_tab = QWidget()
        timeline_tab.setStyleSheet("background-color: #404040;")
        self.tab_widget.addTab(timeline_tab, "⏱️ Timeline")
        
        # Tab 4: Geospatial - Stesso nome del codice originale
        map_tab = QWidget()
        map_tab.setStyleSheet("background-color: #404040;")
        self.tab_widget.addTab(map_tab, "🗺️ Geospatial")
        
        self.setCentralWidget(self.tab_widget)

        # =============================================================================
        # DOCK WIDGETS - Posizioni e nomi IDENTICI a Palantir originale
        # =============================================================================
        
        # DOCK SINISTRO: Entity Explorer 
        entity_dock = PalantirDockWidget("🔍 Entities")
        entity_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                                   Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, entity_dock)
        
        # DOCK DESTRO: Query Builder
        query_dock = PalantirDockWidget("🔎 Query Builder")
        query_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                                  Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, query_dock)
        
        # DOCK INFERIORE: Analysis Results  
        results_dock = PalantirDockWidget("📋 Analysis Results")
        results_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea | 
                                    Qt.DockWidgetArea.TopDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, results_dock)

        # =============================================================================
        # STATUS BAR - Identico a Palantir originale
        # =============================================================================
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # Status label - Stesso testo del codice originale
        status_label = QLabel("Ready - Palantir Desktop Clone")
        status_bar.addWidget(status_label)
        
        # Progress bar - Stessa del codice originale
        progress_label = QLabel("Progress: ")
        status_bar.addPermanentWidget(progress_label)

    def dummy_action(self):
        """Azione placeholder per i menu"""
        pass
        
    def apply_graph_layout(self):
        """Applica il layout force-directed come nel codice originale"""
        # Simula il re-layout dei nodi
        for node_id, node in self.graph_engine.nodes.items():
            new_x = random.uniform(-200, 200)
            new_y = random.uniform(-200, 200)
            node.setPos(new_x, new_y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())