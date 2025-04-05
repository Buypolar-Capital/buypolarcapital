from datetime import datetime, timedelta
from data.vwap_dataset import VWAPExecutionDataset
from model.vwap_trainer import VWAPExecutionTrainer

def main():
    # Load dataset for the last 30 days
    dataset = VWAPExecutionDataset("AAPL", days_back=30)
    train, test = dataset.get_train_test_split(train_days=24, test_days=5)

    print(f"Training on {len(train)} days, Testing on {len(test)} days")

    # Train and test the model
    trainer = VWAPExecutionTrainer(train, test)
    trainer.train_model(epochs=10)
    slippages = trainer.test_model()

    # Plot and export results
    trainer.plot_results(slippages)

if __name__ == "__main__":
    main()