use crate::types::{Order, Side, OrderType, Trade};
use chrono::Utc;
use uuid::Uuid;

pub struct MarketMaker;

impl MarketMaker {
    pub fn new() -> Self {
        Self
    }

    pub fn generate_orders(&self) -> Vec<Order> {
        let mid = 100.0;
        let spread = 0.0; // Changed to 0.0 to ensure matching
        let timestamp = Utc::now();

        vec![
            Order {
                id: Uuid::new_v4(),
                timestamp,
                side: Side::Buy,
                price: mid - spread,
                quantity: 1.0,
                order_type: OrderType::Limit,
            },
            Order {
                id: Uuid::new_v4(),
                timestamp,
                side: Side::Sell,
                price: mid + spread,
                quantity: 1.0,
                order_type: OrderType::Limit,
            },
        ]
    }
}

pub struct MomentumTrader {
    window: usize,
}

impl MomentumTrader {
    pub fn new() -> Self {
        Self { window: 5 }
    }

    pub fn generate_orders(&mut self, trades: &[Trade]) -> Vec<Order> {
        if trades.len() < self.window {
            return vec![];
        }

        let recent: Vec<f64> = trades.iter()
            .rev()
            .take(self.window)
            .map(|t| t.price)
            .collect();

        let direction = if recent[0] > *recent.last().unwrap() {
            Side::Buy
        } else {
            Side::Sell
        };

        let price = recent[0] + if direction == Side::Buy { 0.01 } else { -0.01 };

        vec![Order {
            id: Uuid::new_v4(),
            timestamp: Utc::now(),
            side: direction,
            price,
            quantity: 0.5,
            order_type: OrderType::Limit,
        }]
    }
}