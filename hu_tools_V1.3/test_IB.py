from hu_tools.HU_tools import ProviderEDV
from hu_tools.OutilsDivers.Bilanclasstopo import Statistiques_sdaeu_v4

# Test
algo = Statistiques_sdaeu_v4()
provider = ProviderEDV()
provider.loadAlgorithms()
print([a.id() for a in provider.algorithms()])

