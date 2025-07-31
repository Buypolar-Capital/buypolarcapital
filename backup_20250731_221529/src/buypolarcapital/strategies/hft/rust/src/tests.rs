#[cfg(test)]
mod tests {
    use super::super::order_book::OrderBook;
    use super::super::types::{Order, Side, OrderType};
    use uuid::Uuid;
    use chrono::Utc;

    #[test]
    fn test_limit_order_matching() {
        let mut book = OrderBook::new();

        // Add a sell order (ask)
        let ask = Order {
            id: Uuid::new_v4(),
            timestamp: Utc::now(),
            side: Side::Sell,
            price: 100.0,
            quantity: 1.0,
            order_type: OrderType::Limit,
        };
        book.insert_order(ask);

        // Add a buy order that crosses the ask
        let bid = Order {
            id: Uuid::new_v4(),
            timestamp: Utc::now(),
            side: Side::Buy,
            price: 101.0,
            quantity: 1.0,
            order_type: OrderType::Limit,
        };
        let trades = book.insert_order(bid);

        assert_eq!(trades.len(), 1);
        let trade = &trades[0];
        assert_eq!(trade.price, 100.0);
        assert_eq!(trade.quantity, 1.0);
    }

    #[test]
    fn test_partial_fill() {
        let mut book = OrderBook::new();

        let ask = Order {
            id: Uuid::new_v4(),
            timestamp: Utc::now(),
            side: Side::Sell,
            price: 100.0,
            quantity: 2.0,
            order_type: OrderType::Limit,
        };
        book.insert_order(ask);

        let bid = Order {
            id: Uuid::new_v4(),
            timestamp: Utc::now(),
            side: Side::Buy,
            price: 101.0,
            quantity: 1.0,
            order_type: OrderType::Limit,
        };
        let trades = book.insert_order(bid);

        assert_eq!(trades.len(), 1);
        assert_eq!(trades[0].quantity, 1.0);
    }
}
