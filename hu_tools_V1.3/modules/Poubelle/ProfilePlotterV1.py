import math
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QImage

class ProfilePlotter:
    """Classe pour tracer le profil en long sur un QGraphicsView."""
    
    def __init__(self, graphics_view):
        """Initialise le traceur de profil.
        
        Args:
            graphics_view: QGraphicsView pour afficher le profil
        """
        self.graphics_view = graphics_view
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Si c'est une vue zoomable, associer le plotter
        if hasattr(self.graphics_view, 'set_plotter'):
            self.graphics_view.set_plotter(self)
        
        # Marges du graphique (en pixels)
        self.margin_left = 50
        self.margin_right = 50
        self.margin_top = 50
        self.margin_bottom = 50
        
        # Zone de dessin (en pixels)
        self.plot_width = 800
        self.plot_height = 400
        
        # Dimensions du profil (en unités du monde réel)
        self.min_x = 0
        self.max_x = 100
        self.min_y = 0
        self.max_y = 10
        
        # Facteurs d'échelle
        self.scale_x = 1
        self.scale_y = 1
        
        # Dimensions de la vue (en pixels)
        self.view_width = self.plot_width + self.margin_left + self.margin_right
        self.view_height = self.plot_height + self.margin_top + self.margin_bottom
        
        # Configurer la scène
        self.scene.setSceneRect(0, 0, self.view_width, self.view_height)
    
    def plot_profile(self, profile_data, settings):
        """Trace le profil en long.
        
        Args:
            profile_data: Données du profil
            settings: Paramètres du tracé
        """
        # Sauvegarder les données et paramètres pour le redessinage
        self.current_profile_data = profile_data
        self.current_settings = settings

        # Effacer la scène
        self.scene.clear()
        
        # Vérifier les données
        if not profile_data or not profile_data['canalisations']:
            return
        
        # Récupérer les dimensions du profil
        self.min_x = 0
        if math.isnan(profile_data['cumulative_distance']) or profile_data['cumulative_distance'] <= 0:
            self.max_x = 100  # Valeur par défaut
        else:
            self.max_x = profile_data['cumulative_distance']
        
        # Récupérer min_z et max_z (avec une marge de 10%)
        if profile_data['min_z'] != float('inf') and profile_data['max_z'] != float('-inf'):
            range_z = profile_data['max_z'] - profile_data['min_z']
            margin_z = max(0.5, range_z * 0.1)  # Au moins 0.5m de marge
            
            self.min_y = profile_data['min_z'] - margin_z
            self.max_y = profile_data['max_z'] + margin_z
        else:
            self.min_y = 0
            self.max_y = 10
        
        # Récupérer min_z et max_z (avec une marge de 10%)
        if (profile_data['min_z'] != float('inf') and 
            profile_data['max_z'] != float('-inf') and
            profile_data['min_z'] == profile_data['min_z'] and  # Vérifie que ce n'est pas NaN
            profile_data['max_z'] == profile_data['max_z']):   # Vérifie que ce n'est pas NaN
            
            range_z = profile_data['max_z'] - profile_data['min_z']
            margin_z = max(0.5, range_z * 0.1)  # Au moins 0.5m de marge
            
            self.min_y = profile_data['min_z'] - margin_z
            self.max_y = profile_data['max_z'] + margin_z
        else:
            # Valeurs par défaut si min_z ou max_z sont invalides
            self.min_y = 0
            self.max_y = 10

        # Calculer les facteurs d'échelle avec vérification
        if (self.max_x - self.min_x) > 0:
            self.scale_x = self.plot_width / (self.max_x - self.min_x)
        else:
            self.scale_x = 1.0
            
        if (self.max_y - self.min_y) > 0:
            self.scale_y = self.plot_height / (self.max_y - self.min_y)
        else:
            self.scale_y = 1.0

        # Limiter les facteurs d'échelle pour éviter des valeurs extrêmes
        self.scale_x = max(0.1, min(self.scale_x, 1000))
        self.scale_y = max(0.1, min(self.scale_y, 1000))

        print(f"Facteurs d'échelle: scale_x={self.scale_x}, scale_y={self.scale_y}")
                
        # Tracer les axes
        self._draw_axes()
        
        # Tracer les canalisations
        self._draw_canalisations(profile_data['canalisations'])
        
        # Tracer les regards
        self._draw_regards(profile_data['regards'], settings)
        
        # Ajuster la vue
        self.reset_zoom()
    
    def reset_zoom(self):
        """Réinitialise le zoom de la vue."""
        self.graphics_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
    
    def export_png(self, filepath):
        """Exporte le profil au format PNG.
        
        Args:
            filepath: Chemin du fichier PNG
        
        Returns:
            bool: True si l'export a réussi, False sinon
        """
        try:
            # Créer une image aux dimensions de la scène
            image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
            image.fill(Qt.white)
            
            # Créer un QPainter pour dessiner sur l'image
            painter = QPainter(image)
            self.scene.render(painter)
            painter.end()
            
            # Sauvegarder l'image
            return image.save(filepath)
        except Exception as e:
            print(f"Erreur lors de l'export PNG: {e}")
            return False
    
    def _draw_axes(self):
        """Trace les axes du graphique."""
        # Stylo pour les axes
        pen = QPen(Qt.black, 1)
        
        # Axe X (distance)
        x_axis = QGraphicsLineItem(
            self.margin_left, self.view_height - self.margin_bottom,
            self.view_width - self.margin_right, self.view_height - self.margin_bottom
        )
        x_axis.setPen(pen)
        self.scene.addItem(x_axis)
        
        # Axe Y (altitude)
        y_axis = QGraphicsLineItem(
            self.margin_left, self.margin_top,
            self.margin_left, self.view_height - self.margin_bottom
        )
        y_axis.setPen(pen)
        self.scene.addItem(y_axis)
        
        # Graduations sur l'axe X (distance)
        x_step = self._calculate_step(self.max_x - self.min_x)
        
        # Vérifier que les valeurs sont valides avant de les utiliser
        if (math.isnan(self.min_x) or math.isnan(self.max_x) or 
            math.isinf(self.min_x) or math.isinf(self.max_x)):
            min_x, max_x = 0, 10
        else:
            min_x, max_x = self.min_x, self.max_x
        
        # Utiliser les valeurs vérifiées
        for x in range(int(min_x), int(max_x) + 1, x_step):
            # Position en pixels
            px = self._world_to_pixel_x(x)
            
            # Ligne de graduation
            tick = QGraphicsLineItem(
                px, self.view_height - self.margin_bottom,
                px, self.view_height - self.margin_bottom + 5
            )
            tick.setPen(pen)
            self.scene.addItem(tick)
            
            # Texte de graduation
            text = QGraphicsTextItem(str(x))
            text.setPos(px - 10, self.view_height - self.margin_bottom + 5)
            self.scene.addItem(text)
        
        # Titre de l'axe X
        x_title = QGraphicsTextItem("Longueur (m)")
        x_title.setPos(self.margin_left + self.plot_width/2 - 40, 
                    self.view_height - self.margin_bottom + 30)
        self.scene.addItem(x_title)
        
        # Faire la même vérification pour l'axe Y
        if (math.isnan(self.min_y) or math.isnan(self.max_y) or 
            math.isinf(self.min_y) or math.isinf(self.max_y)):
            min_y, max_y = 0, 10
        else:
            min_y, max_y = self.min_y, self.max_y
        
        # Graduations sur l'axe Y (altitude)
        y_step = self._calculate_step(max_y - min_y)
        for y in range(int(min_y), int(max_y) + 1, y_step):
            # Position en pixels
            py = self._world_to_pixel_y(y)
            
            # Ligne de graduation
            tick = QGraphicsLineItem(
                self.margin_left - 5, py,
                self.margin_left, py
            )
            tick.setPen(pen)
            self.scene.addItem(tick)
            
            # Texte de graduation
            text = QGraphicsTextItem(str(y))
            text.setPos(self.margin_left - 30, py - 10)
            self.scene.addItem(text)
        
        # Titre de l'axe Y
        y_title = QGraphicsTextItem("Altitude (mNGF)")
        y_title.setPos(self.margin_left - 90, self.margin_top + 30)
        y_title.setRotation(-90)
        self.scene.addItem(y_title)
    
    def _draw_canalisations(self, canalisations):
        """Trace les canalisations."""
        # Stylo pour les canalisations
        fe_pen = QPen(QColor(0, 0, 255), 2)  # Bleu
        gs_pen = QPen(QColor(0, 100, 255), 1, Qt.DashLine)  # Bleu clair en pointillés
        
        # Ajouter un débogage pour vérifier les données
        print(f"Nombre de canalisations à tracer: {len(canalisations)}")
        
        for cana in canalisations:
            # Vérification plus complète des données
            if (cana['z_amont'] is None or cana['z_aval'] is None or 
                math.isnan(cana['z_amont']) or math.isnan(cana['z_aval']) or
                math.isinf(cana['z_amont']) or math.isinf(cana['z_aval']) or
                math.isnan(cana['start_distance']) or math.isnan(cana['end_distance']) or
                math.isinf(cana['start_distance']) or math.isinf(cana['end_distance'])):
                print(f"Données invalides pour la canalisation {cana['id']}")
                continue
            
            # Positions en pixels pour le FE (fond d'écoulement)
            x1 = self._world_to_pixel_x(cana['start_distance'])
            y1_fe = self._world_to_pixel_y(cana['z_amont'])
            x2 = self._world_to_pixel_x(cana['end_distance'])
            y2_fe = self._world_to_pixel_y(cana['z_aval'])
            
            # Obtenir le diamètre de la canalisation
            dn = cana.get('dn', 0.2)  # Valeur par défaut: 200mm
            
            # Positions pour la génératrice supérieure (FE + diamètre)
            y1_gs = self._world_to_pixel_y(cana['z_amont'] + dn)
            y2_gs = self._world_to_pixel_y(cana['z_aval'] + dn)
            
            # Déboguer les positions calculées
            print(f"Canalisation {cana['id']}: ({x1}, {y1_fe}) à ({x2}, {y2_fe})")
            
            # Tracer le fond d'écoulement (FE)
            fe_line = QGraphicsLineItem(x1, y1_fe, x2, y2_fe)
            fe_line.setPen(fe_pen)
            self.scene.addItem(fe_line)
            
            # Tracer la génératrice supérieure (GS)
            gs_line = QGraphicsLineItem(x1, y1_gs, x2, y2_gs)
            gs_line.setPen(gs_pen)
            self.scene.addItem(gs_line)
            
            # Tracer les lignes verticales aux extrémités
            left_line = QGraphicsLineItem(x1, y1_fe, x1, y1_gs)
            right_line = QGraphicsLineItem(x2, y2_fe, x2, y2_gs)
            left_line.setPen(fe_pen)
            right_line.setPen(fe_pen)
            self.scene.addItem(left_line)
            self.scene.addItem(right_line)
            
            # Ajouter le texte de pente si disponible
            if cana.get('pente') is not None:  # Utiliser .get() pour éviter KeyError
                # Position du texte (au milieu de la canalisation)
                x_text = (x1 + x2) / 2
                y_text = (y1_fe + y2_fe) / 2 - 10
                
                # Créer le texte
                text = QGraphicsTextItem(f"{cana['pente']:.2f}%")
                text.setPos(x_text - 20, y_text)
                self.scene.addItem(text)
    
    def _draw_regards(self, regards, settings):
        """Trace les regards."""
        # Stylo pour les regards
        pen = QPen(Qt.red, 2)
        
        # Stylo pour le terrain naturel
        tn_pen = QPen(QColor(139, 69, 19), 2)  # Marron
        
        # Ajouter un débogage pour vérifier les données
        print(f"Nombre de regards à tracer: {len(regards)}")
        
        # Dessiner d'abord la ligne du terrain naturel si possible
        if len(regards) > 1 and settings.get('show_tn', True):
            tn_points = []
            for regard in regards:
                if regard.get('tn') is not None and not math.isnan(regard.get('tn', 0)) and not math.isinf(regard.get('tn', 0)):
                    x = self._world_to_pixel_x(regard['distance'])
                    y = self._world_to_pixel_y(regard['tn'])
                    tn_points.append((x, y))
            
            # Tracer la ligne du TN si on a au moins 2 points
            if len(tn_points) >= 2:
                for i in range(len(tn_points) - 1):
                    tn_line = QGraphicsLineItem(tn_points[i][0], tn_points[i][1], 
                                            tn_points[i+1][0], tn_points[i+1][1])
                    tn_line.setPen(tn_pen)
                    self.scene.addItem(tn_line)
        
        # Tracer ensuite chaque regard
        for regard in regards:
            # Vérification plus complète des données
            if (regard['distance'] is None or regard['fe'] is None or
                math.isnan(regard['distance']) or math.isnan(regard['fe']) or
                math.isinf(regard['distance']) or math.isinf(regard['fe'])):
                print(f"Données invalides pour le regard ID: {regard.get('id', 'inconnu')}")
                continue
            
            # Position en pixels
            x = self._world_to_pixel_x(regard['distance'])
            y_fe = self._world_to_pixel_y(regard['fe'])
            
            # Déboguer les positions calculées
            print(f"Regard {regard.get('id')}: distance={regard['distance']}, fe={regard['fe']}, tn={regard.get('tn')}")
            
            # Diamètre du regard (en pixels)
            dn_pixels = 20  # Taille par défaut
            if regard.get('dn') is not None:
                dn_pixels = regard['dn'] * self.scale_x  # Convertir m en pixels
                dn_pixels = max(10, min(dn_pixels, 50))  # Limiter entre 10 et 50 pixels
            
            # Tracer le regard avec deux traits verticaux
            half_width = dn_pixels / 2
            
            # Y du terrain naturel
            y_tn = y_fe
            if regard.get('tn') is not None and not math.isnan(regard.get('tn')) and not math.isinf(regard.get('tn')):
                y_tn = self._world_to_pixel_y(regard['tn'])
            
            # Tracer les deux traits verticaux
            left_line = QGraphicsLineItem(x - half_width, y_tn, x - half_width, y_fe)
            right_line = QGraphicsLineItem(x + half_width, y_tn, x + half_width, y_fe)
            left_line.setPen(pen)
            right_line.setPen(pen)
            self.scene.addItem(left_line)
            self.scene.addItem(right_line)
            
            # Ligne horizontale au fond du regard
            bottom_line = QGraphicsLineItem(x - half_width, y_fe, x + half_width, y_fe)
            bottom_line.setPen(pen)
            self.scene.addItem(bottom_line)
            
            # Ajouter les étiquettes si demandé
            if settings.get('show_fe', True):
                text = QGraphicsTextItem(f"FE: {regard['fe']:.2f}")
                text.setPos(x + half_width + 5, y_fe - 5)
                self.scene.addItem(text)
            
            if settings.get('show_tn', True) and regard.get('tn') is not None:
                text = QGraphicsTextItem(f"TN: {regard['tn']:.2f}")
                text.setPos(x + half_width + 5, y_tn - 15)
                self.scene.addItem(text)

    def _world_to_pixel_x(self, x):
        """Convertit une coordonnée X du monde réel en pixels."""
        # Vérifier que x est une valeur valide
        if x is None or math.isnan(x) or math.isinf(x):
            # Utiliser une valeur par défaut au milieu de l'écran
            return self.margin_left + self.plot_width / 2
            
        return self.margin_left + (x - self.min_x) * self.scale_x
    
    def _world_to_pixel_y(self, y):
        """Convertit une coordonnée Y du monde réel en pixels."""
        # Vérifier que y est une valeur valide
        if y is None or math.isnan(y) or math.isinf(y):
            # Utiliser une valeur par défaut au milieu de l'écran
            return self.view_height - self.margin_bottom - self.plot_height / 2
            
        # Inverser l'axe Y (origine en haut à gauche)
        return self.view_height - self.margin_bottom - (y - self.min_y) * self.scale_y
    
    def _calculate_step(self, range_value):
        """Calcule un pas approprié pour les graduations des axes."""
        # Vérifier si range_value est NaN, infini, zéro ou négatif
        if range_value != range_value or range_value <= 0 or math.isinf(range_value):
            return 1
        
        try:
            # Ordre de grandeur
            magnitude = 10 ** math.floor(math.log10(range_value))
            
            # Facteur (1, 2, 5)
            if range_value / magnitude >= 5:
                return 5 * magnitude
            elif range_value / magnitude >= 2:
                return 2 * magnitude
            else:
                return magnitude
        except (ValueError, OverflowError, ZeroDivisionError):
            # En cas d'erreur, retourner une valeur par défaut
            return 1
        
    def set_data_bounds(self, min_x, max_x, min_y, max_y):
        """Définit les nouvelles limites des données pour le zoom."""
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        
        # Recalculer les facteurs d'échelle
        if (self.max_x - self.min_x) > 0:
            self.scale_x = self.plot_width / (self.max_x - self.min_x)
        else:
            self.scale_x = 1.0
            
        if (self.max_y - self.min_y) > 0:
            self.scale_y = self.plot_height / (self.max_y - self.min_y)
        else:
            self.scale_y = 1.0
        
        # Limiter les facteurs d'échelle pour éviter des valeurs extrêmes
        self.scale_x = max(0.1, min(self.scale_x, 1000))
        self.scale_y = max(0.1, min(self.scale_y, 1000))
    
    def redraw_profile(self):
        """Redessine le profil avec les nouvelles limites sans changer les données."""
        if hasattr(self, 'current_profile_data') and hasattr(self, 'current_settings'):
            self.plot_profile(self.current_profile_data, self.current_settings)
        else:
            print("Aucune donnée de profil à redessiner")