from PyQt5.QtWidgets import QGraphicsView, QGraphicsRectItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QColor

class ZoomableGraphicsView(QGraphicsView):
    """Vue graphique avec fonctionnalité de zoom rectangle."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPen.Antialiasing)
        self.setDragMode(QGraphicsView.NoDrag)
        
        # État de l'outil zoom
        self.zoom_mode_active = False
        self.zoom_start_point = None
        self.zoom_rect_item = None
        self.plotter = None  # Sera défini plus tard
        
    def set_plotter(self, plotter):
        """Associe le plotter à cette vue."""
        self.plotter = plotter
    
    def enable_zoom_mode(self):
        """Active le mode zoom rectangle."""
        self.zoom_mode_active = True
        self.setCursor(Qt.CrossCursor)
    
    def disable_zoom_mode(self):
        """Désactive le mode zoom rectangle."""
        self.zoom_mode_active = False
        self.setCursor(Qt.ArrowCursor)
        
    def mousePressEvent(self, event):
        """Capture le clic de souris pour débuter le zoom."""
        if self.zoom_mode_active and event.button() == Qt.LeftButton:
            # Enregistrer le point de départ
            self.zoom_start_point = event.pos()
            
            # Créer un rectangle pour visualiser la sélection
            scene_pos = self.mapToScene(event.pos())
            self.zoom_rect_item = QGraphicsRectItem(scene_pos.x(), scene_pos.y(), 0, 0)
            
            # Styliser le rectangle de sélection
            pen = QPen(QColor(0, 0, 255, 128))
            pen.setWidth(1)
            pen.setStyle(Qt.DashLine)
            self.zoom_rect_item.setPen(pen)
            
            # Ajouter à la scène
            if self.scene():
                self.scene().addItem(self.zoom_rect_item)
            
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Met à jour le rectangle de sélection pendant le déplacement."""
        if self.zoom_mode_active and self.zoom_start_point and self.zoom_rect_item:
            # Calculer le rectangle
            start_pos = self.mapToScene(self.zoom_start_point)
            current_pos = self.mapToScene(event.pos())
            
            x = min(start_pos.x(), current_pos.x())
            y = min(start_pos.y(), current_pos.y())
            width = abs(current_pos.x() - start_pos.x())
            height = abs(current_pos.y() - start_pos.y())
            
            # Mettre à jour le rectangle
            self.zoom_rect_item.setRect(x, y, width, height)
            event.accept()
        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Finalise le zoom quand le bouton est relâché."""
        if self.zoom_mode_active and event.button() == Qt.LeftButton and self.zoom_start_point and self.zoom_rect_item:
            # Récupérer le rectangle de sélection
            rect = self.zoom_rect_item.rect()
            
            # Supprimer le rectangle de la scène
            if self.scene():
                self.scene().removeItem(self.zoom_rect_item)
            self.zoom_rect_item = None
            
            # Vérifier que le rectangle a une taille minimale
            if rect.width() > 10 and rect.height() > 10:
                # Appliquer le zoom
                self._apply_zoom(rect)
            
            # Réinitialiser
            self.zoom_start_point = None
            self.disable_zoom_mode()
            event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def _apply_zoom(self, rect):
        """Applique le zoom sur la région sélectionnée."""
        if not self.plotter:
            return
            
        # Obtenir les limites du plotter
        margin_left = self.plotter.margin_left
        margin_top = self.plotter.margin_top
        plot_width = self.plotter.plot_width
        plot_height = self.plotter.plot_height
        
        # Zone de traçage
        plot_rect = QRectF(
            margin_left, 
            margin_top, 
            plot_width,
            plot_height
        )
        
        # S'assurer que le zoom est dans la zone de traçage
        zoom_rect = rect.intersected(plot_rect)
        
        if zoom_rect.isEmpty():
            return
            
        # Convertir les coordonnées d'écran en coordonnées de données
        old_min_x = self.plotter.min_x
        old_max_x = self.plotter.max_x
        old_min_y = self.plotter.min_y
        old_max_y = self.plotter.max_y
        
        # Calculer les nouvelles limites
        new_min_x = old_min_x + (zoom_rect.left() - margin_left) / self.plotter.scale_x
        new_max_x = old_min_x + (zoom_rect.right() - margin_left) / self.plotter.scale_x
        
        # Axe Y inversé dans le système d'écran
        new_max_y = old_max_y - (zoom_rect.top() - margin_top) / self.plotter.scale_y
        new_min_y = old_max_y - (zoom_rect.bottom() - margin_top) / self.plotter.scale_y
        
        # Appliquer le zoom
        self.plotter.set_data_bounds(new_min_x, new_max_x, new_min_y, new_max_y)
        self.plotter.redraw_profile()