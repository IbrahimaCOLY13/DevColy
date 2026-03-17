import unittest
import os
import shutil
from datetime import datetime
from modules.error_handler import ErrorHandler

class TestErrorHandler(unittest.TestCase):
    """Tests pour la classe ErrorHandler."""

    def setUp(self):
        """Exécuté avant chaque test."""
        # Créer un dossier temporaire pour les logs de test
        self.test_log_dir = os.path.join(os.path.dirname(__file__), 'test_logs')
        os.makedirs(self.test_log_dir, exist_ok=True)
        
        # Sauvegarder le dossier de logs original
        self.original_log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        
        # Rediriger les logs vers le dossier de test
        ErrorHandler._logger = None  # Réinitialiser le logger
        self.log_file = os.path.join(self.test_log_dir, f'hu_tools_{datetime.now().strftime("%Y%m")}.log')

    def tearDown(self):
        """Exécuté après chaque test."""
        # Nettoyer les fichiers de test
        if os.path.exists(self.test_log_dir):
            shutil.rmtree(self.test_log_dir)
        
        # Réinitialiser le logger
        ErrorHandler._logger = None

    def test_log_initialization(self):
        """Teste l'initialisation du système de logging."""
        ErrorHandler.initialize_logging()
        self.assertTrue(os.path.exists(self.original_log_dir))
        
    def test_log_file_creation(self):
        """Teste si le fichier de log est créé lors de la première erreur."""
        test_error = ValueError("Test error message")
        ErrorHandler.log_error(test_error, "Test context")
        
        self.assertTrue(os.path.exists(self.original_log_dir))
        log_file = ErrorHandler.get_log_file_path()
        self.assertTrue(os.path.exists(log_file))

    def test_log_content(self):
        """Teste si le contenu du log est correct."""
        # Créer une erreur de test
        test_error = ValueError("Test error message")
        test_context = "Test context"
        
        # Logger l'erreur
        ErrorHandler.log_error(test_error, test_context)
        
        # Lire le fichier de log
        log_file = ErrorHandler.get_log_file_path()
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
        
        # Vérifier le contenu
        self.assertIn("ERROR", log_content)
        self.assertIn("Test error message", log_content)
        self.assertIn("Test context", log_content)
        self.assertIn("ValueError", log_content)

    def test_multiple_logs(self):
        """Teste l'enregistrement de plusieurs erreurs."""
        errors = [
            (ValueError("Error 1"), "Context 1"),
            (TypeError("Error 2"), "Context 2"),
            (RuntimeError("Error 3"), "Context 3")
        ]
        
        # Logger plusieurs erreurs
        for error, context in errors:
            ErrorHandler.log_error(error, context)
        
        # Vérifier le fichier de log
        log_file = ErrorHandler.get_log_file_path()
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
        
        # Vérifier que toutes les erreurs sont présentes
        for error, context in errors:
            self.assertIn(str(error), log_content)
            self.assertIn(context, log_content)

    def test_log_file_path(self):
        """Teste la génération du chemin du fichier de log."""
        expected_filename = f'hu_tools_{datetime.now().strftime("%Y%m")}.log'
        log_path = ErrorHandler.get_log_file_path()
        self.assertTrue(log_path.endswith(expected_filename))

if __name__ == '__main__':
    unittest.main()