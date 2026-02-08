import unittest
import numpy as np
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.settings import settings
from src.models.gbm import GeometricBrownianMotionStrategy
from src.models.student_t import StudentTStrategy

class TestArchitecture(unittest.TestCase):
    
    def test_singleton_settings(self):
        """GAP 3 VALIDATION: Verificar que Settings es un Singleton único."""
        s1 = settings
        s2 = settings
        # Deben ser exactamente el mismo objeto en memoria
        self.assertIs(s1, s2)
        # Verificar que cargó variables críticas
        self.assertTrue(len(s1.TICKERS) > 0)
        self.assertEqual(s1.HORIZON, 252)

    def test_strategy_polymorphism(self):
        """GAP 2 VALIDATION: Verificar que ambas estrategias siguen el contrato."""
        # Datos Dummy (100 días, 2 activos)
        dummy_returns = np.random.normal(0, 0.01, size=(100, 2))
        import pandas as pd
        df = pd.DataFrame(dummy_returns, columns=['A', 'B'])
        
        # Probar GBM
        gbm = GeometricBrownianMotionStrategy()
        gbm.train(df)
        self.assertIsNotNone(gbm.chol_matrix, "GBM debe calcular Cholesky")
        
        # Probar t-Student
        stu = StudentTStrategy()
        stu.train(df)
        self.assertTrue(2.0 < stu.nu < 100, "Nu debe estar en rango sensato")

    def test_gold_layer_structure(self):
        """GAP 1 VALIDATION: Verificar existencia de directorios."""
        gold_path = os.path.join(settings.DATA_DIR, "gold")
        self.assertTrue(os.path.exists(gold_path))

if __name__ == '__main__':
    unittest.main()