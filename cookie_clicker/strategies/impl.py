"""Here you find strategies, that are more comprehensive"""
from decimal import Decimal
from .base import BaseStrategy

class CheapStrategy(BaseStrategy):
    """This strategy buys always the cheapest item."""
    def __init__(self):
        super(CheapStrategy, self).__init__(name="cheap")

    def __call__(self, cookies, cps, time_left, factory):
        costs = [(factory[building].cost, building)
                 for building in factory]
        costs.sort(key=lambda tup: tup[0])

        if costs[0][0] <= (time_left * cps + cookies):
            return costs[0][1]
        else:
            return None

class ExpensiveStrategy(BaseStrategy):
    """This strategy buys always the most expensive item."""
    def __init__(self):
        super(ExpensiveStrategy, self).__init__(name="expensive")

    def __call__(self, cookies, cps, time_left, factory):
        costs = [(factory[building].cost, building) for building in factory]
        costs.sort(key=lambda tup: tup[0], reverse=True)

        for cost, building in costs:
            if cost <= (time_left * cps + cookies):
                return building
        return None

class MonsterStrategy(BaseStrategy):
    def __init__(self):
        super(MonsterStrategy, self).__init__(name="Monster")

    def __call__(self, cookies, cps, time_left, factory):

        def payback_period(cost: Decimal, cookies_in_bank: Decimal, cps: Decimal,
                           cps_building: Decimal) -> Decimal:
            return max(cost - cookies / cps, 0) / cps + cost / cps_building

        if cps == 0.0:
            return 'Cursor'

        payback_period_per_item = []

        for building_name in factory:
            building = factory[building_name]
            payback_period_per_item.append(
                (building_name,
                 payback_period(cost=building.cost,
                                cookies_in_bank=cookies,
                                cps=cps,
                                cps_building=building.cps)))

        payback_period_per_item.sort(key=lambda tup: tup[1])

        best_option = payback_period_per_item[0][0]
        return best_option
