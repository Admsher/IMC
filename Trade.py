
from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string


class Trader:
    
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        result = {}
        total_buy_amount = 0
        total_sell_amount = 0
        num_buy_orders = 0
        num_sell_orders = 0
        
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
            
            buy_orders_above_average = []
            sell_orders_below_average = []
    
            if len(order_depth.sell_orders) != 0:
                sorted_sell_orders = sorted(order_depth.sell_orders.items(), key=lambda x: x[1], reverse=True)
                total_sell_amount = sum(price * amount for price, amount in order_depth.sell_orders.items())
                average_sell_order = total_sell_amount / len(order_depth.sell_orders) 
                for price, amount in sorted_sell_orders:
                    if int(price) <= average_sell_order:
                   
                        sell_orders_below_average.append((price, -amount))
                
                
                if len(sell_orders_below_average) != 0:
                # Sort sell_orders_below_average based on multiplication of price and amount
                    sell_orders_below_average = sorted(sell_orders_below_average, key=lambda x: int(x[0]) * x[1], reverse=True)
                
                    if len(sell_orders_below_average) >2:
                # Append orders using the first element in sell_orders_below_average
                        for order_price, order_amount in sell_orders_below_average[-2]:
                            orders.append(Order(product, order_price, -order_amount))
    
            if len(order_depth.buy_orders) != 0:
                sorted_buy_orders = sorted(order_depth.buy_orders.items(), key=lambda x: x[1], reverse=True)
                total_buy_amount=sum(price * amount for price, amount in order_depth.buy_orders.items())
                average_buy_order = total_buy_amount / len(order_depth.buy_orders) 
                for price, amount in sorted_buy_orders:
                    if int(price) >= average_buy_order:
                        buy_orders_above_average.append((price, amount))
                
                
                if len(buy_orders_above_average) != 0:
                    # Sort buy_orders_above_average based on multiplication of price and amount
                    buy_orders_above_average = sorted(buy_orders_above_average, key=lambda x: int(x[0]) * x[1], reverse=True)
                
                    # Append orders using the second element in buy_orders_above_average
                   
                    for order_price, order_amount in buy_orders_above_average[1]:
                            orders.append(Order(product, order_price, order_amount))
                
            result[product] = orders
    
        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1
        return result, conversions, traderData
