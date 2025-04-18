use crate::types::Trade;
use std::error::Error;
use std::fs::File;
use std::io::Write;

pub fn write_trades_to_csv(path: &str, trades: &[Trade]) -> Result<(), Box<dyn Error>> {
    let mut file = File::create(path)?;
    writeln!(file, "timestamp,buy_order_id,sell_order_id,price,quantity")?;

    for t in trades {
        writeln!(
            file,
            "{},{},{},{:.2},{:.4}",
            t.timestamp,
            t.buy_order_id,
            t.sell_order_id,
            t.price,
            t.quantity
        )?;
    }

    println!("📁 Trades written to {}", path);
    Ok(())
}
