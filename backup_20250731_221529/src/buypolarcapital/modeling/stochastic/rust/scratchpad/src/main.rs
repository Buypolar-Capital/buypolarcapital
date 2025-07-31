use rand::Rng;
use std::fs;
use plotters::prelude::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // === Config ===
    let steps = 100;
    let mut price = 100.0;
    let mut rng = rand::thread_rng();
    let mut prices = vec![price];

    // === Simulate Random Walk ===
    for _ in 0..steps {
        let change: f64 = rng.gen_range(-1.0..1.0);
        price += change;
        prices.push(price);
    }

    // === Ensure output directory exists ===
    fs::create_dir_all("../plots")?;

    // === Plot to SVG ===
    let path = "../plots/random_walk.svg";
    let root = SVGBackend::new(path, (800, 600)).into_drawing_area();
    root.fill(&WHITE)?;

    let (min_price, max_price) = prices
        .iter()
        .fold((f64::MAX, f64::MIN), |(min, max), &x| (min.min(x), max.max(x)));

    let mut chart = ChartBuilder::on(&root)
        .caption("Random Walk Price Path", ("sans-serif", 28))
        .margin(20)
        .x_label_area_size(40)
        .y_label_area_size(40)
        .build_cartesian_2d(0usize..steps as usize, min_price..max_price)?;

    chart
        .configure_mesh()
        .x_desc("Step")
        .y_desc("Price")
        .draw()?;

    chart
        .draw_series(LineSeries::new(
            prices.iter().enumerate().map(|(i, &p)| (i, p)),
            &BLUE,
        ))?
        .label("Price")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &BLUE));

    chart.configure_series_labels().background_style(&WHITE).draw()?;

    root.present()?;
    println!("✅ Plot generated: {}", path);
    println!("Note: To convert SVG to PDF, use a tool like rsvg-convert or an online converter.");

    Ok(())
}