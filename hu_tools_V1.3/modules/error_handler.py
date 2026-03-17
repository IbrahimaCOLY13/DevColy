from typing import Optional
import os
import logging
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox

class ErrorHandler:
    _logger = None
    
    @classmethod
    def initialize_logging(cls):
        """Initialise le système de journalisation."""
        if cls._logger is not None:
            return

        # Créer le dossier logs s'il n'existe pas
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)

        # Nom du fichier de log avec la date
        log_file = os.path.join(log_dir, f'hu_tools_{datetime.now().strftime("%Y%m")}.log')

        # Configurer le logger
        cls._logger = logging.getLogger('HU_Tools')
        cls._logger.setLevel(logging.DEBUG)

        # Gestionnaire de fichier
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # Format du log
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s\n'
            'Context: %(context)s\n'
            'Exception: %(exception)s\n'
            '----------------------------------------'
        )
        file_handler.setFormatter(formatter)

        # Ajouter le gestionnaire au logger
        cls._logger.addHandler(file_handler)

    @classmethod
    def get_log_file_path(cls) -> str:
        """Retourne le chemin du fichier de log actuel."""
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        return os.path.join(log_dir, f'hu_tools_{datetime.now().strftime("%Y%m")}.log')

    @classmethod
    def show_log_file(cls):
        """Ouvre le fichier de log avec l'application par défaut du système."""
        log_file = cls.get_log_file_path()
        if os.path.exists(log_file):
            os.startfile(log_file) if os.name == 'nt' else os.system(f'xdg-open "{log_file}"')
        else:
            cls.show_warning("Log introuvable", "Aucun fichier de log n'existe pour le moment.")

    @staticmethod
    def show_error(title: str, message: str, details: Optional[str] = None):
        """Affiche une boîte de dialogue d'erreur standardisée."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        if details:
            msg.setDetailedText(details)
        msg.exec_()

    @staticmethod
    def show_warning(title: str, message: str):
        """Affiche une boîte de dialogue d'avertissement standardisée."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    @classmethod
    def log_error(cls, error: Exception, context: str):
        """Enregistre l'erreur dans un fichier de log."""
        if cls._logger is None:
            cls.initialize_logging()

        extra = {
            'context': context,
            'exception': f"{type(error).__name__}: {str(error)}"
        }
        
        cls._logger.error(
            f"Une erreur s'est produite",
            extra=extra,
            exc_info=True  # Inclut le stack trace
        )
