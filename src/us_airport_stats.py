from backbones import DisparityBackboneStrategy, HighSalienceSkeletonBackboneStrategy, PolyaBackboneStrategy
from data      import USAirportDataProvider
from analysis  import p_values, size, order

from matplotlib import pyplot as plt

data_provider = USAirportDataProvider()

backbone_strategy = PolyaBackboneStrategy(a = 1, integer_weights = False)

data_provider.apply_backbone_strategy(backbone_strategy)
backbone = data_provider.get_graph()

ps = p_values(backbone)

interesting_values = [1, 0.0005, 0.003, 0.05, 0.3, 0.5]
orders = []
sizes  = []

for i in interesting_values:
    orders.append(order(backbone, p = i))
    sizes.append(size(backbone, p = i))

    print(f"Order of backbone with salience = {i}: {orders[-1]}")
    print(f"Size of backbone with salience = {i}: {sizes[-1]}")

plt.hist(ps, bins = 100)
plt.title("Distribution of $p$-values in the US Air Travel Póyla Backbone with $a = 2$")
plt.xlabel("$p$-value")
plt.ylabel("Occurrences")
# plt.grid()
plt.xlim((0, 1))
plt.show()

