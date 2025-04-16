use std::collections::VecDeque;
use crate::types::{Order, Side, Trade};
use chrono::Utc;

pub struct OrderBook {
    pub bids: VecDeque<Order>,
    pub asks: VecDeque<Order>,
}

impl OrderBook {
    pub fn new() -> Self {
        Self {
            bids: VecDeque::new(),
            asks: VecDeque::new(),
        }
    }

    pub fn insert_order(&mut self, mut order: Order) -> Vec<Trade> {
        let mut trades = Vec::new();
        match order.side {
            Side::Buy => {
                while let Some(ask) = self.asks.front_mut() {
                    if order.price >= ask.price && order.quantity > 0.0 {
                        let qty = order.quantity.min(ask.quantity);
                        trades.push(Trade {
                            buy_order_id: order.id,
                            sell_order_id: ask.id,
                            price: ask.price,
                            quantity: qty,
                            timestamp: Utc::now(),
                            initiator: Side::Buy, // Initiator is the incoming buy order
                        });
    
                        order.quantity -= qty;
                        ask.quantity -= qty;
    
                        if ask.quantity <= 0.0 {
                            self.asks.pop_front();
                        }
                    } else {
                        break;
                    }
                }
                if order.quantity > 0.0 {
                    self.bids.push_back(order);
                }
            }
            Side::Sell => {
                while let Some(bid) = self.bids.front_mut() {
                    if order.price <= bid.price && order.quantity > 0.0 {
                        let qty = order.quantity.min(bid.quantity);
                        trades.push(Trade {
                            buy_order_id: bid.id,
                            sell_order_id: order.id,
                            price: bid.price,
                            quantity: qty,
                            timestamp: Utc::now(),
                            initiator: Side::Sell, // Initiator is the incoming sell order
                        });
    
                        order.quantity -= qty;
                        bid.quantity -= qty;
    
                        if bid.quantity <= 0.0 {
                            self.bids.pop_front();
                        }
                    } else {
                        break;
                    }
                }
                if order.quantity > 0.0 {
                    self.asks.push_back(order);
                }
            }
        }
        trades
    }
}