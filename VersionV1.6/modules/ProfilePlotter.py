import math
import os
from qgis.core import QgsProject
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPen, QColor
import plotly.graph_objects as go
import plotly.io as pio

class ProfilePlotter:
    """Classe pour tracer le profil en long sur un QWebEngineView."""
    
    def __init__(self, web_view):
        """Initialise le traceur de profil.
        
        Args:
            web_view: QWebEngineView pour afficher le profil
        """
        self.web_view = web_view
        
        # Dimensions du profil (en unités du monde réel)
        self.min_x = 0
        self.max_x = 100
        self.min_y = 0
        self.max_y = 10
        
        # Variables pour stocker les données courantes
        self.current_profile_data = None
        self.current_settings = None
        self.original_min_x = None
        self.original_max_x = None
        self.original_min_y = None
        self.original_max_y = None

        # Dossier par défaut pour les exports
        self.export_folder = os.path.join(QgsProject.instance().homePath() or os.path.expanduser("~"), "exports_profils")
        # Créer le dossier s'il n'existe pas
        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)

        # Configurer le gestionnaire de téléchargements
        self.configure_download_handler()

    def configure_download_handler(self):
        """Configure le gestionnaire de téléchargements pour QWebEngineView."""
        from PyQt5.QtWebEngineWidgets import QWebEngineProfile
        
        # Obtenir le profil par défaut
        profile = QWebEngineProfile.defaultProfile()
        
        # Définir le dossier de téléchargement
        profile.setDownloadPath(self.export_folder)
        
        # Connecter le signal de téléchargement demandé
        profile.downloadRequested.connect(self.handle_download)


    def get_unique_filepath(self, base_path):
        """Génère un chemin de fichier unique en incrémentant un compteur si le fichier existe déjà.
        
        Args:
            base_path: Chemin de base du fichier (avec extension)
            
        Returns:
            str: Chemin de fichier unique
        """
        if not os.path.exists(base_path):
            return base_path
        
        # Séparer le chemin en base et extension
        root, ext = os.path.splitext(base_path)
        counter = 1
        
        # Incrémenter le compteur jusqu'à trouver un nom de fichier disponible
        while os.path.exists(f"{root}_{counter}{ext}"):
            counter += 1
        
        return f"{root}_{counter}{ext}"

    def handle_download(self, download):
        """Gère les demandes de téléchargement."""
        # Accepter automatiquement le téléchargement et utiliser le nom de fichier suggéré
        from PyQt5.QtCore import QUrl
        
        # Obtenir le nom de fichier suggéré
        suggested_filename = download.suggestedFileName()
        
        # Construire le chemin complet
        path = os.path.join(self.export_folder, suggested_filename)
        
        # Définir le chemin de téléchargement
        download.setPath(path)
        
        # Accepter le téléchargement
        download.accept()
        
        # Connecter un signal pour notifier quand le téléchargement est terminé
        download.finished.connect(lambda: self.download_finished(path))


    def download_finished(self, path):
        """Notification lorsqu'un téléchargement est terminé."""
        from PyQt5.QtWidgets import QMessageBox
        
        # Afficher un message à l'utilisateur
        QMessageBox.information(
            None, 
            "Téléchargement terminé", 
            f"Le profil a été enregistré dans:\n{path}"
        )

    def plot_profile(self, profile_data, settings):
        """Trace le profil en long avec Plotly.
        
        Args:
            profile_data: Données du profil
            settings: Paramètres du tracé
        """
        # Sauvegarder les données et paramètres pour le redessinage
        self.current_profile_data = profile_data
        self.current_settings = settings
        
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
        if (profile_data['min_z'] != float('inf') and 
            profile_data['max_z'] != float('-inf') and
            profile_data['min_z'] == profile_data['min_z'] and
            profile_data['max_z'] == profile_data['max_z']):
            
            range_z = profile_data['max_z'] - profile_data['min_z']
            margin_z = max(0.5, range_z * 0.1)  # Au moins 0.5m de marge
            
            self.min_y = profile_data['min_z'] - margin_z
            self.max_y = profile_data['max_z'] + margin_z
        else:
            # Valeurs par défaut si min_z ou max_z sont invalides
            self.min_y = 0
            self.max_y = 10

        # Sauvegarder les valeurs originales pour le reset du zoom
        self.original_min_x = self.min_x
        self.original_max_x = self.max_x
        self.original_min_y = self.min_y
        self.original_max_y = self.max_y
        
        # Créer le graphique Plotly
        fig = self._create_plotly_figure(profile_data, settings)
        
        # Configuration pour que la figure s'adapte automatiquement
        fig.update_layout(
            autosize=True,
            margin=dict(l=50, r=50, t=100, b=50, pad=0),
            height=None,  # Laisser la hauteur s'adapter
            width=None    # Laisser la largeur s'adapter
        )
        
        # Créer un style CSS pour que le contenu s'adapte à la fenêtre
        css_style = """
        <style>
            html, body {
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
            .plotly-graph-div {
                width: 100%;
                height: 100%;
            }
        </style>
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Convertir en HTML et afficher dans le QWebEngineView
        html = pio.to_html(
            fig, 
            include_plotlyjs='cdn',
            config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'profil_en_long_{timestamp}',
                    'height': 800,
                    'width': 1200,
                    'scale': 2  # Meilleure résolution pour l'export
                },
                'responsive': True  # Important pour l'adaptation automatique
            },
            full_html=True  # Générer un document HTML complet
        )
        
        # Insérer notre style CSS dans l'en-tête HTML
        html = html.replace('<head>', f'<head>{css_style}')
        
        # Afficher dans le QWebEngineView
        self.web_view.setHtml(html)
        self.fig = fig  # Stocker la figure pour l'export
        
    def _create_plotly_figure(self, profile_data, settings):
        """Crée une figure Plotly pour le profil en long."""
        fig = go.Figure()
        
        # Variables pour contrôler la légende
        first_tn_added = False
        first_cana_added = False
        first_gs_added = False
        first_regard_added = False
        
        # Dessiner le terrain naturel si demandé
        if settings.get('show_tn', True) and profile_data['regards']:
            x_tn = []
            y_tn = []
            
            for regard in profile_data['regards']:
                if regard.get('distance') is not None and regard.get('tn') is not None:
                    if not math.isnan(regard['distance']) and not math.isnan(regard['tn']):
                        x_tn.append(regard['distance'])
                        y_tn.append(regard['tn'])
            
            if x_tn:
                fig.add_trace(go.Scatter(
                    x=x_tn,
                    y=y_tn,
                    mode='lines+markers',
                    name='Terrain Naturel',  # Nom générique pour la légende
                    line=dict(color='brown', width=2),
                    hovertemplate='Distance: %{x:.2f}m<br>TN: %{y:.2f}m<extra></extra>'
                ))
                first_tn_added = True
        
        # Dessiner les canalisations
        for cana in profile_data['canalisations']:
            # Fond d'écoulement (FE)
            if (cana.get('z_amont') is not None and cana.get('z_aval') is not None and
                cana.get('start_distance') is not None and cana.get('end_distance') is not None):
                
                # Tracer le fond d'écoulement
                fig.add_trace(go.Scatter(
                    x=[cana['start_distance'], cana['end_distance']],
                    y=[cana['z_amont'], cana['z_aval']],
                    mode='lines',
                    name='Canalisation (FE)',  # Nom générique
                    line=dict(color='blue', width=3),
                    hovertemplate='Cana ' + f"{cana.get('id', '')}" + '<br>Distance: %{x:.2f}m<br>FE: %{y:.2f}m<extra></extra>',
                    showlegend=not first_cana_added  # Afficher dans la légende seulement la première fois
                ))
                first_cana_added = True
                
                # Tracer la génératrice supérieure
                dn = cana.get('dn', 0.2)  # Diamètre par défaut: 200mm
                
                fig.add_trace(go.Scatter(
                    x=[cana['start_distance'], cana['end_distance']],
                    y=[cana['z_amont'] + dn, cana['z_aval'] + dn],
                    mode='lines',
                    name='Génératrice Supérieure',  # Nom générique
                    line=dict(color='lightblue', width=2, dash='dash'),
                    hovertemplate='Cana ' + f"{cana.get('id', '')}" + '<br>Distance: %{x:.2f}m<br>GS: %{y:.2f}m<extra></extra>',
                    showlegend=not first_gs_added  # Afficher dans la légende seulement la première fois
                ))
                first_gs_added = True
                
                # Ajouter le texte de pente si disponible
                if cana.get('pente') is not None and settings.get('show_pente', True):
                    mid_x = (cana['start_distance'] + cana['end_distance']) / 2
                    mid_y = (cana['z_amont'] + cana['z_aval']) / 2
                    
                    fig.add_annotation(
                        x=mid_x,
                        y=mid_y + 0.2,  # Décalage au-dessus de la canalisation
                        text=f"{cana['pente']:.2f}%",
                        showarrow=False,
                        font=dict(size=10, color="blue")
                    )
        
        # Dessiner les regards
        for regard in profile_data['regards']:
            if (regard.get('distance') is not None and 
                regard.get('fe') is not None):
                
                # Récupérer les données du regard
                x = regard['distance']
                y_fe = regard['fe']
                y_tn = regard.get('tn', y_fe + 1.5)  # Par défaut TN = FE + 1.5m
                
                # Récupérer le diamètre du regard (par défaut 1m si non spécifié)
                dn = regard.get('dn', 1.0)
                
                # Calculer les positions des traits verticaux
                x_left = x - dn/2
                x_right = x + dn/2
                
                # Dessiner le premier trait vertical (gauche)
                fig.add_trace(go.Scatter(
                    x=[x_left, x_left],
                    y=[y_fe, y_tn],
                    mode='lines',
                    name='Regard',  # Nom générique pour tous les regards
                    line=dict(color='red', width=2),
                    hovertemplate='Regard ' + f"{regard.get('id', '')}" + '<br>FE: ' + f"{y_fe:.2f}m" + '<br>TN: ' + f"{y_tn:.2f}m" + '<extra></extra>',
                    showlegend=not first_regard_added  # Montrer dans la légende seulement la première fois
                ))
                first_regard_added = True
                
                # Dessiner le second trait vertical (droite)
                fig.add_trace(go.Scatter(
                    x=[x_right, x_right],
                    y=[y_fe, y_tn],
                    mode='lines',
                    name='Regard',  # Même nom pour la cohérence
                    line=dict(color='red', width=2),
                    hovertemplate='Regard ' + f"{regard.get('id', '')}" + '<br>FE: ' + f"{y_fe:.2f}m" + '<br>TN: ' + f"{y_tn:.2f}m" + '<extra></extra>',
                    showlegend=False  # Ne jamais montrer dans la légende
                ))
                
                # Dessiner le trait horizontal en haut (TN)
                fig.add_trace(go.Scatter(
                    x=[x_left, x_right],
                    y=[y_tn, y_tn],
                    mode='lines',
                    line=dict(color='red', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Dessiner le trait horizontal en bas (FE)
                fig.add_trace(go.Scatter(
                    x=[x_left, x_right],
                    y=[y_fe, y_fe],
                    mode='lines',
                    line=dict(color='red', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Ajouter les étiquettes si demandé
                if settings.get('show_fe', True):
                    fig.add_annotation(
                        x=x + dn/2 + 0.5,  # Décalage à droite du regard
                        y=y_fe,
                        text=f"FE: {y_fe:.2f}",
                        showarrow=False,
                        font=dict(size=10, color="red")
                    )
                
                if settings.get('show_tn', True):
                    fig.add_annotation(
                        x=x + dn/2 + 0.5,  # Décalage à droite du regard
                        y=y_tn,
                        text=f"TN: {y_tn:.2f}",
                        showarrow=False,
                        font=dict(size=10, color="brown")
                    )
        
        # Configuration de la mise en page
        fig.update_layout(
            title="Profil en long",
            xaxis_title="Distance (m)",
            yaxis_title="Altitude (mNGF)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=50, r=50, t=100, b=50),
            height=600,
            plot_bgcolor='white',
            hovermode='closest'
        )

        # Amélioration des axes avec traits noirs et graduations
        fig.update_xaxes(
            range=[self.min_x, self.max_x],
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            ticks='outside',
            ticklen=8,
            tickwidth=1.5,
            tickcolor='black',
            minor_showgrid=True,
            gridcolor='lightgray'
        )

        fig.update_yaxes(
            range=[self.min_y, self.max_y],
            showline=True,
            linewidth=2, 
            linecolor='black',
            mirror=True,
            ticks='outside',
            ticklen=8,
            tickwidth=1.5,
            tickcolor='black',
            minor_showgrid=True,
            gridcolor='lightgray'
        )
        
        return fig
    
    def set_data_bounds(self, min_x, max_x, min_y, max_y):
        """Définit les nouvelles limites des données pour le zoom."""
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.redraw_profile()
    
    def redraw_profile(self):
        """Redessine le profil avec les nouvelles limites sans changer les données."""
        if hasattr(self, 'current_profile_data') and hasattr(self, 'current_settings'):
            self.plot_profile(self.current_profile_data, self.current_settings)
    
    def reset_zoom(self):
        """Réinitialise le zoom aux valeurs initiales."""
        if hasattr(self, 'original_min_x'):
            self.min_x = self.original_min_x
            self.max_x = self.original_max_x
            self.min_y = self.original_min_y
            self.max_y = self.original_max_y
            self.redraw_profile()
    
    def capture_to_file(self, filename=None):
        """Capture le contenu du QWebEngineView et l'enregistre dans le dossier d'export."""
        if not hasattr(self, 'web_view') or not self.web_view:
            print("QWebEngineView non disponible pour la capture")
            return None
            
        # Générer un nom de fichier par défaut basé sur la date/heure si non fourni
        if not filename:
            from datetime import datetime
            now = datetime.now()
            filename = f"profil_{now.strftime('%Y%m%d_%H%M%S')}.png"
        
        # S'assurer que le fichier a l'extension .png
        if not filename.lower().endswith('.png'):
            filename += '.png'
        
        # Chemin complet du fichier
        base_path = os.path.join(self.export_folder, filename)
        
        # Obtenir un chemin unique pour éviter l'écrasement
        filepath = self.get_unique_filepath(base_path)
        
        # Capturer le contenu visible
        def callback(result):
            if result:
                print(f"Capture enregistrée dans {filepath}")
            else:
                print(f"Échec de la capture dans {filepath}")
        
        # Utiliser la fonction de capture native de QWebEnginePage
        self.web_view.page().captureVisibleContents(callback)
        
        return filepath
    
    def get_export_folder(self):
        """Retourne le chemin du dossier d'export actuel."""
        return self.export_folder

    def set_export_folder(self, folder_path):
        """Définit le dossier d'export par défaut."""
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            self.export_folder = folder_path
            return True
        return False
    
