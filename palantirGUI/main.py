from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QTabWidget, QGraphicsScene, QVBoxLayout, QGraphicsItem, QGraphicsEllipseItem,QDockWidget, QGraphicsView, QLabel, QGroupBox, QButtonGroup, QPushButton, QSizePolicy, QLineEdit
from PyQt6.QtGui import QIcon, QPainter, QPen, QFont, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QUrl
import sys
import random
import pyqtgraph as pg
from ui.chat.chat import Chat

class DockWidget(QDockWidget):
    def __init__(self, title):
        super().__init__(title)
        empty_widget = QWidget()
        empty_widget.setStyleSheet("background-color: red;")
        self.setWidget(empty_widget)


class Server(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):

        vertical_layout = QVBoxLayout(self)

        self.label1 = QLabel("Chat Privata 1", self)
        vertical_layout.addWidget(self.label1)

        self.label2 = QLabel("Chat Privata 2", self)
        vertical_layout.addWidget(self.label2)


    def create_metric_widget(self, title, value, change):
        widget = QGroupBox(title)
        layout = QVBoxLayout(widget)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #48aff0;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        change_label = QLabel(change)
        change_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color = "#0f9960" if change.startswith('+') else "#db3737" if change.startswith('-') else "#5c7080"
        change_label.setStyleSheet(f"color: {color}; font-size: 12px;")
        
        layout.addWidget(value_label)
        layout.addWidget(change_label)
        
        return widget


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

class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.current_view = "standard"  # "standard" o "satellite"
        self.setup_ui()

    def setup_ui(self):
        # Layout principale
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Toolbar per selezione vista
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # Gruppo di bottoni per selezione vista
        self.view_group = QButtonGroup(self)
        self.view_group.setExclusive(True)
        
        # Bottone vista standard (mappa dark)
        self.btn_standard = QPushButton("🌍 Vista Mappa")
        self.btn_standard.setCheckable(True)
        self.btn_standard.setChecked(True)
        self.btn_standard.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #3daee9;
                color: black;
                border: 1px solid #3daee9;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)
        
        # Bottone vista satellite
        self.btn_satellite = QPushButton("🛰️ Vista Satellite")
        self.btn_satellite.setCheckable(True)
        self.btn_satellite.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #3daee9;
                color: black;
                border: 1px solid #3daee9;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)
        
        # Aggiungi bottoni al gruppo e al layout
        self.view_group.addButton(self.btn_standard)
        self.view_group.addButton(self.btn_satellite)
        
        toolbar_layout.addWidget(self.btn_standard)
        toolbar_layout.addWidget(self.btn_satellite)
        toolbar_layout.addStretch()
        
        main_layout.addLayout(toolbar_layout)

        # WebView per la mappa interattiva
        self.webView = QWebEngineView()
        main_layout.addWidget(self.webView)
        
        # Connessioni dei bottoni
        self.btn_standard.clicked.connect(self.switch_to_standard_view)
        self.btn_satellite.clicked.connect(self.switch_to_satellite_view)
        
        # Carica la vista iniziale
        self.load_current_view()

    def switch_to_standard_view(self):
        self.current_view = "standard"
        self.load_current_view()

    def switch_to_satellite_view(self):
        self.current_view = "satellite"
        self.load_current_view()

    def load_current_view(self):
        if self.current_view == "standard":
            html_content = self.get_standard_map_html()
        else:
            html_content = self.get_satellite_map_html()
        
        self.webView.setHtml(html_content)

    def get_standard_map_html(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dark Intelligence Map - Standard View</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            
            <!-- Leaflet CSS -->
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background-color: #0a0a0a;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                #map {
                    position: absolute;
                    top: 0;
                    bottom: 0;
                    width: 100%;
                    background-color: #0a0a0a;
                }
                
                .custom-popup {
                    background: rgba(0, 20, 40, 0.95);
                    color: white;
                    border: 1px solid #00ffff;
                    border-radius: 8px;
                    padding: 10px;
                    font-family: monospace;
                }
                
                .view-info {
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    background: rgba(0, 0, 0, 0.8);
                    color: #00ffff;
                    padding: 5px 10px;
                    border-radius: 4px;
                    font-family: monospace;
                    font-size: 12px;
                    z-index: 1000;
                    border: 1px solid #00ffff;
                }
            </style>
        </head>
        <body>
            <div class="view-info">🌍 VISTA MAPPA - RETE GLOBALE</div>
            <div id="map"></div>

            <!-- Leaflet JavaScript -->
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            
            <script>
                // Inizializza la mappa
                var map = L.map('map', {
                    center: [25, 20],
                    zoom: 2,
                    zoomControl: true,
                    attributionControl: true,
                    worldCopyJump: false,
                    maxBounds: [[-90, -180], [90, 180]],
                    maxBoundsViscosity: 1.0
                });

                // Layer mappa dark
                var darkLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                    attribution: '©OpenStreetMap, ©CartoDB',
                    subdomains: 'abcd',
                    maxZoom: 20,
                    noWrap: true
                }).addTo(map);

                // DATI CONDIVISI - Server e connessioni
                var cities = [
                    {name: "ROMA-DC1", coords: [41.9028, 12.4964], status: "active", throughput: "1.2 Gbps"},
                    {name: "NYC-DC2", coords: [40.7128, -74.0060], status: "warning", throughput: "0.8 Gbps"},
                    {name: "TK-DC3", coords: [35.6762, 139.6503], status: "active", throughput: "1.5 Gbps"},
                    {name: "SYD-DC4", coords: [-33.8688, 151.2093], status: "critical", throughput: "0.5 Gbps"},
                    {name: "LON-DC5", coords: [51.5074, -0.1278], status: "active", throughput: "1.1 Gbps"},
                    {name: "DBX-DC6", coords: [25.2769, 55.2962], status: "active", throughput: "0.9 Gbps"},
                    {name: "SP-DC7", coords: [-23.5505, -46.6333], status: "warning", throughput: "0.7 Gbps"}
                ];

                var connections = [
                    {from: "ROMA-DC1", to: "NYC-DC2", latency: "89ms", strength: 0.9},
                    {from: "ROMA-DC1", to: "TK-DC3", latency: "210ms", strength: 0.7},
                    {from: "NYC-DC2", to: "LON-DC5", latency: "65ms", strength: 0.8},
                    {from: "TK-DC3", to: "SYD-DC4", latency: "145ms", strength: 0.6},
                    {from: "LON-DC5", to: "DBX-DC6", latency: "95ms", strength: 0.8},
                    {from: "DBX-DC6", to: "SP-DC7", latency: "320ms", strength: 0.5},
                    {from: "NYC-DC2", to: "SP-DC7", latency: "110ms", strength: 0.7}
                ];

                // Aggiungi marker server
                cities.forEach(function(city) {
                    var color = city.status === 'active' ? '#00ff00' : 
                               city.status === 'warning' ? '#ffff00' : '#ff4444';
                    
                    var marker = L.circleMarker(city.coords, {
                        color: color,
                        fillColor: color,
                        fillOpacity: 0.8,
                        radius: 10,
                        weight: 3
                    }).addTo(map);

                    marker.bindPopup(`
                        <div class="custom-popup">
                            <b>🚀 ${city.name}</b><br/>
                            📍 Status: <span style="color: ${color}">${city.status.toUpperCase()}</span><br/>
                            📊 Throughput: ${city.throughput}<br/>
                            📍 Coordinates: ${city.coords[0].toFixed(4)}, ${city.coords[1].toFixed(4)}
                        </div>
                    `);
                });

                // Aggiungi connessioni
                connections.forEach(function(conn) {
                    var fromCity = cities.find(c => c.name === conn.from);
                    var toCity = cities.find(c => c.name === conn.to);
                    
                    if (fromCity && toCity) {
                        var lineColor = conn.latency < 100 ? '#00ff00' : 
                                      conn.latency < 200 ? '#ffff00' : '#ff4444';
                        
                        L.polyline([fromCity.coords, toCity.coords], {
                            color: lineColor,
                            weight: conn.strength * 4,
                            opacity: 0.7,
                            dashArray: conn.strength > 0.7 ? null : '5, 5'
                        }).addTo(map).bindPopup(`
                            <div class="custom-popup">
                                <b>🔗 ${conn.from} → ${conn.to}</b><br/>
                                ⏱️ Latency: ${conn.latency}<br/>
                                💪 Strength: ${(conn.strength * 100).toFixed(0)}%
                            </div>
                        `);
                    }
                });

                console.log("Vista Mappa Standard - Caricata");
            </script>
        </body>
        </html>
        """

    def get_satellite_map_html(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dark Intelligence Map - Satellite View</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            
            <!-- Leaflet CSS -->
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background-color: #0a0a0a;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                #map {
                    position: absolute;
                    top: 0;
                    bottom: 0;
                    width: 100%;
                    background-color: #0a0a0a;
                }
                
                .custom-popup {
                    background: rgba(0, 20, 40, 0.95);
                    color: white;
                    border: 1px solid #00ffff;
                    border-radius: 8px;
                    padding: 10px;
                    font-family: monospace;
                }
                
                .view-info {
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    background: rgba(0, 0, 0, 0.8);
                    color: #ffaa00;
                    padding: 5px 10px;
                    border-radius: 4px;
                    font-family: monospace;
                    font-size: 12px;
                    z-index: 1000;
                    border: 1px solid #ffaa00;
                }
            </style>
        </head>
        <body>
            <div class="view-info">🛰️ VISTA SATELLITE - TRAFFICO GLOBALE</div>
            <div id="map"></div>

            <!-- Leaflet JavaScript -->
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            
            <script>
                // Inizializza la mappa satellite
                var map = L.map('map', {
                    center: [25, 20],
                    zoom: 2,
                    zoomControl: true,
                    attributionControl: true,
                    worldCopyJump: false,
                    maxBounds: [[-90, -180], [90, 180]],
                    maxBoundsViscosity: 1.0
                });

                // Layer satellite
                var satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                    attribution: '© Esri, Earthstar Geographics',
                    maxZoom: 19,
                    noWrap: true
                }).addTo(map);

                // DATI CONDIVISI - Stessi server e connessioni della vista standard
                var cities = [
                    {name: "ROMA-DC1", coords: [41.9028, 12.4964], status: "active", throughput: "1.2 Gbps"},
                    {name: "NYC-DC2", coords: [40.7128, -74.0060], status: "warning", throughput: "0.8 Gbps"},
                    {name: "TK-DC3", coords: [35.6762, 139.6503], status: "active", throughput: "1.5 Gbps"},
                    {name: "SYD-DC4", coords: [-33.8688, 151.2093], status: "critical", throughput: "0.5 Gbps"},
                    {name: "LON-DC5", coords: [51.5074, -0.1278], status: "active", throughput: "1.1 Gbps"},
                    {name: "DBX-DC6", coords: [25.2769, 55.2962], status: "active", throughput: "0.9 Gbps"},
                    {name: "SP-DC7", coords: [-23.5505, -46.6333], status: "warning", throughput: "0.7 Gbps"}
                ];

                var connections = [
                    {from: "ROMA-DC1", to: "NYC-DC2", latency: "89ms", strength: 0.9},
                    {from: "ROMA-DC1", to: "TK-DC3", latency: "210ms", strength: 0.7},
                    {from: "NYC-DC2", to: "LON-DC5", latency: "65ms", strength: 0.8},
                    {from: "TK-DC3", to: "SYD-DC4", latency: "145ms", strength: 0.6},
                    {from: "LON-DC5", to: "DBX-DC6", latency: "95ms", strength: 0.8},
                    {from: "DBX-DC6", to: "SP-DC7", latency: "320ms", strength: 0.5},
                    {from: "NYC-DC2", to: "SP-DC7", latency: "110ms", strength: 0.7}
                ];

                // Aggiungi marker server (stessa posizione, stile diverso)
                cities.forEach(function(city) {
                    var color = city.status === 'active' ? '#00ff00' : 
                               city.status === 'warning' ? '#ffff00' : '#ff4444';
                    
                    // Marker più visibili su sfondo satellite
                    var marker = L.circleMarker(city.coords, {
                        color: '#ffffff',
                        fillColor: color,
                        fillOpacity: 0.9,
                        radius: 12,
                        weight: 3
                    }).addTo(map);

                    marker.bindPopup(`
                        <div class="custom-popup">
                            <b>🛰️ ${city.name}</b><br/>
                            📍 Status: <span style="color: ${color}">${city.status.toUpperCase()}</span><br/>
                            📊 Throughput: ${city.throughput}<br/>
                            📍 Coordinates: ${city.coords[0].toFixed(4)}, ${city.coords[1].toFixed(4)}
                        </div>
                    `);
                });

                // Aggiungi connessioni (stesse connessioni, stile diverso)
                connections.forEach(function(conn) {
                    var fromCity = cities.find(c => c.name === conn.from);
                    var toCity = cities.find(c => c.name === conn.to);
                    
                    if (fromCity && toCity) {
                        var lineColor = conn.latency < 100 ? '#00ff00' : 
                                      conn.latency < 200 ? '#ffff00' : '#ff4444';
                        
                        // Linee più spesse per vista satellite
                        L.polyline([fromCity.coords, toCity.coords], {
                            color: lineColor,
                            weight: conn.strength * 6,
                            opacity: 0.8,
                            dashArray: conn.strength > 0.7 ? null : '8, 8'
                        }).addTo(map).bindPopup(`
                            <div class="custom-popup">
                                <b>📡 ${conn.from} → ${conn.to}</b><br/>
                                ⏱️ Latency: ${conn.latency}<br/>
                                💪 Strength: ${(conn.strength * 100).toFixed(0)}%
                            </div>
                        `);
                    }
                });

                console.log("Vista Satellite - Caricata");
            </script>
        </body>
        </html>
        """
  
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySafety")
        self.setWindowIcon(QIcon("sources/logo.png"))

        width, height = self.getGeometry()
        
        self.width_perc = int(width * 0.8)
        self.height_perc = int(height * 0.7)
        self.setMinimumSize(self.width_perc, self.height_perc)

        self.setStyleSheet("background-color: #1E1E1E;")
    
        widget = QWidget()
        self.setCentralWidget(widget)

        self.main_layout = QHBoxLayout(widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

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

        self._initGUI_()


    def getGeometry(self):
        screen = self.screen()
        screen_size = screen.size()
        width = int(screen_size.width())
        height = int(screen_size.height())

        return width, height

    def _initGUI_(self):        
        settings_dock = DockWidget("Settings")
        settings_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea |
                                      Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, settings_dock)

        entity_dock = DockWidget("Task")
        entity_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea |
                                    Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, entity_dock)


        self.tab_widget = QTabWidget()

        self.chat_tab = QWidget()
        chat_layout = QVBoxLayout(self.chat_tab)

        self.chat_engine = Chat()
        chat_layout.addWidget(self.chat_engine)

        self.tab_widget.addTab(self.chat_tab, QIcon("sources/padlock.png"), "Chat")


        self.graph_tab = QWidget()
        graph_layout = QVBoxLayout(self.graph_tab)

        self.graph_engine = Map()
        graph_layout.addWidget(self.graph_engine)
 
        self.tab_widget.addTab(self.graph_tab, QIcon("sources/map.png"), "Map")


        self.server_tab = QWidget()
        server_layout = QVBoxLayout(self.server_tab)

        self.server_engine = Server()
        server_layout.addWidget(self.server_engine)

        self.tab_widget.addTab(self.server_tab, QIcon("sources/server.png"), "Server")


        self.setCentralWidget(self.tab_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("sources/logo.png"))

    window = MainWindow()
    window.show()

    app.exec()