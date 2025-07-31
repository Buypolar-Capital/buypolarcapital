use crate::types::Trade;
use crate::order_book::OrderBook;
use crate::strategy::{MarketMaker, MomentumTrader};
use crate::data::write_trades_to_csv;
use crate::plot::plot_trades;

pub fn run_simulation() {
    let mut book = OrderBook::new();
    let mm = MarketMaker::new();
    let mut momentum = MomentumTrader::new();
    let mut all_trades: Vec<Trade> = Vec::new();

    // Sim horizon
    for _ in 0..100 {
        let mm_orders = mm.generate_orders();
        let mo_orders = momentum.generate_orders(&all_trades);

        for order in mm_orders.into_iter().chain(mo_orders) {
            let trades = book.insert_order(order);
            all_trades.extend(trades);
        }
    }

    // Output stats
    print_summary_stats(&all_trades);

    // Save to CSV
    write_trades_to_csv("data/trades.csv", &all_trades).expect("CSV write failed");

    // Save to PNG
    plot_trades("plots/trades.png", &all_trades).expect("Plotting failed");
}

fn print_summary_stats(trades: &[Trade]) {
    let total_volume: f64 = trades.iter().map(|t| t.quantity).sum();
    let notional: f64 = trades.iter().map(|t| t.price * t.quantity).sum();
    let vwap = if total_volume > 0.0 {
        notional / total_volume
    } else {
        0.0
    };

    println!("\n📊 TRADE SUMMARY");
    println!("Total trades: {}", trades.len());
    println!("Total volume: {:.2}", total_volume);
    println!("VWAP: {:.2}", vwap);
}