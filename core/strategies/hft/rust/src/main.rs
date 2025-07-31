mod types;
mod order_book;
mod engine;
mod strategy;
mod data;
mod plot;


fn main() {
    println!("🚀 HFT Engine Booting Up...");
    engine::run_simulation();
}
