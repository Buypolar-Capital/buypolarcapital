use crate::types::{Trade, Side};
use plotters::prelude::*;
use std::error::Error;
use std::fs;

pub fn plot_trades(path: &str, trades: &[Trade]) -> Result<(), Box<dyn Error>> {
    if trades.is_empty() {
        println!("⚠️ No trades to plot.");
        return Ok(());
    }

    // Ensure the directory exists
    if let Some(parent) = std::path::Path::new(path).parent() {
        fs::create_dir_all(parent)?;
    }

    let root = BitMapBackend::new(path, (1200, 800)).into_drawing_area();
    root.fill(&WHITE)?;

    let (min_price, max_price) = trades.iter().fold((f64::MAX, f64::MIN), |(min, max), t| {
        (min.min(t.price), max.max(t.price))
    });

    let max_qty = trades.iter().map(|t| t.quantity).fold(0.0, f64::max);

    // Split the drawing area: 60% for price chart, 40% for volume chart
    let areas = root.split_evenly((2, 1));

    // Price Chart
    let mut price_chart = ChartBuilder::on(&areas[0])
        .caption("Trade Prices Over Time", ("sans-serif", 30).into_font())
        .margin(20)
        .x_label_area_size(40)
        .y_label_area_size(60)
        .build_cartesian_2d(0..trades.len(), (min_price - 0.05)..(max_price + 0.05))?;

    price_chart
        .configure_mesh()
        .x_desc("Trade Index")
        .y_desc("Price")
        .set_all_tick_mark_size(5)
        .x_labels(10)
        .y_labels(8)
        .axis_desc_style(("sans-serif", 20).into_font())
        .label_style(("sans-serif", 15).into_font())
        .light_line_style(&WHITE)
        .bold_line_style(&BLACK.mix(0.2))
        .draw()?;

    // Draw price points, color-coded by initiator
    price_chart.draw_series(trades.iter().enumerate().map(|(i, t)| {
        let color = if t.initiator == Side::Buy { GREEN } else { RED };
        Circle::new((i, t.price), 4, color.filled())
    }))?;

    // Draw a line connecting the price points
    price_chart.draw_series(LineSeries::new(
        trades.iter().enumerate().map(|(i, t)| (i, t.price)),
        &BLUE,
    ))?;

    // Add legend for price chart using EmptyElement
    price_chart
        .draw_series(std::iter::once(
            EmptyElement::at((0, min_price))
                + Circle::new((0, 0), 5, GREEN.filled()),
        ))?
        .label("Buy Initiated")
        .legend(|(x, y)| Circle::new((x + 15, y), 5, GREEN.filled()));

    price_chart
        .draw_series(std::iter::once(
            EmptyElement::at((0, min_price))
                + Circle::new((0, 0), 5, RED.filled()),
        ))?
        .label("Sell Initiated")
        .legend(|(x, y)| Circle::new((x + 15, y), 5, RED.filled()));

    price_chart
        .configure_series_labels()
        .position(SeriesLabelPosition::UpperRight)
        .background_style(&WHITE.mix(0.8))
        .border_style(&BLACK)
        .label_font(("sans-serif", 15).into_font())
        .draw()?;

    // Volume Chart (Histogram)
    let mut vol_chart = ChartBuilder::on(&areas[1])
        .caption("Trade Volume Over Time", ("sans-serif", 25).into_font())
        .margin(20)
        .x_label_area_size(40)
        .y_label_area_size(60)
        .build_cartesian_2d(0..trades.len(), 0.0..(max_qty * 1.1))?;

    vol_chart
        .configure_mesh()
        .x_desc("Trade Index")
        .y_desc("Volume")
        .set_all_tick_mark_size(5)
        .x_labels(10)
        .y_labels(5)
        .axis_desc_style(("sans-serif", 20).into_font())
        .label_style(("sans-serif", 15).into_font())
        .light_line_style(&WHITE)
        .bold_line_style(&BLACK.mix(0.2))
        .draw()?;

    // Draw histogram for buy-initiated trades (green)
    vol_chart.draw_series(
        Histogram::vertical(&vol_chart)
            .style(GREEN.mix(0.7).filled())
            .margin(1)
            .data(
                trades
                    .iter()
                    .enumerate()
                    .filter(|(_, t)| t.initiator == Side::Buy)
                    .map(|(i, t)| (i, t.quantity)),
            ),
    )?;

    // Draw histogram for sell-initiated trades (red)
    vol_chart.draw_series(
        Histogram::vertical(&vol_chart)
            .style(RED.mix(0.7).filled())
            .margin(1)
            .data(
                trades
                    .iter()
                    .enumerate()
                    .filter(|(_, t)| t.initiator == Side::Sell)
                    .map(|(i, t)| (i, t.quantity)),
            ),
    )?;

    // Add legend for volume chart
    vol_chart
        .draw_series(std::iter::once(
            EmptyElement::at((0, 0.0))
                + Rectangle::new([(0, 0), (0, 0)], GREEN.mix(0.7).filled()),
        ))?
        .label("Buy Initiated")
        .legend(|(x, y)| Rectangle::new([(x, y), (x + 15, y - 5)], GREEN.mix(0.7).filled()));

    vol_chart
        .draw_series(std::iter::once(
            EmptyElement::at((0, 0.0))
                + Rectangle::new([(0, 0), (0, 0)], RED.mix(0.7).filled()),
        ))?
        .label("Sell Initiated")
        .legend(|(x, y)| Rectangle::new([(x, y), (x + 15, y - 5)], RED.mix(0.7).filled()));

    vol_chart
        .configure_series_labels()
        .position(SeriesLabelPosition::UpperRight)
        .background_style(&WHITE.mix(0.8))
        .border_style(&BLACK)
        .label_font(("sans-serif", 15).into_font())
        .draw()?;

    println!("📊 Plot saved to {}", path);
    Ok(())
}