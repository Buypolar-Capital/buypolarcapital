use chrono::{DateTime, Utc};
use uuid::Uuid;

#[derive(Debug, Clone)]
#[allow(dead_code)]
pub enum OrderType {
    Limit,
    Market,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Side {
    Buy,
    Sell,
}

#[derive(Debug, Clone)]
#[allow(dead_code)]
pub struct Order {
    pub id: Uuid,
    pub timestamp: DateTime<Utc>,
    pub side: Side,
    pub price: f64,
    pub quantity: f64,
    pub order_type: OrderType,
}

#[derive(Debug, Clone)]
pub struct Trade {
    pub buy_order_id: Uuid,
    pub sell_order_id: Uuid,
    pub price: f64,
    pub quantity: f64,
    pub timestamp: DateTime<Utc>,
    pub initiator: Side, // Added to track which side initiated the trade
}