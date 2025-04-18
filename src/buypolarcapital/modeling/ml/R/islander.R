

# Load required packages
library(quantmod)
library(tidyverse)
library(caret)
library(ISLR)
library(MASS)
library(class)
library(e1071)
library(randomForest)
library(gridExtra)

# Create plots folder if not exists
dir.create("plots", showWarnings = FALSE)

# 1. Download SPY data
getSymbols("SPY", src = "yahoo", from = "2010-01-01", auto.assign = TRUE)
spy <- na.omit(SPY)

# 2. Create lagged returns and features (FIXED)
library(zoo)  # needed for rollapply

spy_returns <- quantmod::dailyReturn(Ad(spy), type = "log")
spy_df <- tibble(
  Date = index(spy_returns),
  Return = as.numeric(spy_returns)
) %>%
  mutate(
    Lag1 = lag(Return, 1),
    Lag2 = lag(Return, 2),
    Lag3 = lag(Return, 3),
    Lag5 = lag(Return, 5),
    Vol5 = rollapply(Return, width = 5, FUN = sd, fill = NA, align = "right"),
    Direction = ifelse(lead(Return) > 0, "Up", "Down")
  ) %>%
  drop_na()


# 3. Train/Test split
set.seed(123)
train_index <- 1:floor(0.8 * nrow(spy_df))
train <- spy_df[train_index, ]
test <- spy_df[-train_index, ]

# 4. Prepare train/test X and y
X_train <- train %>% select(Lag1, Lag2, Lag3, Lag5, Vol5)
X_test  <- test %>% select(Lag1, Lag2, Lag3, Lag5, Vol5)
y_train <- train$Direction
y_test  <- test$Direction

# 5. Fit models
models <- list()

# Logistic Regression
models$logit <- glm(Direction ~ ., data = train %>% select(Direction, Lag1, Lag2, Lag3, Lag5, Vol5), family = "binomial")
pred_logit <- ifelse(predict(models$logit, X_test, type = "response") > 0.5, "Up", "Down")

# LDA
models$lda <- lda(Direction ~ ., data = train %>% select(Direction, Lag1, Lag2, Lag3, Lag5, Vol5))
pred_lda <- predict(models$lda, X_test)$class

# QDA
models$qda <- qda(Direction ~ ., data = train %>% select(Direction, Lag1, Lag2, Lag3, Lag5, Vol5))
pred_qda <- predict(models$qda, X_test)$class

# KNN
pred_knn <- knn(train = scale(X_train), test = scale(X_test), cl = y_train, k = 5)

# Random Forest
models$rf <- randomForest(Direction ~ ., data = train %>% select(Direction, Lag1, Lag2, Lag3, Lag5, Vol5), ntree = 500)
pred_rf <- predict(models$rf, X_test)

# SVM (radial kernel)
models$svm <- svm(Direction ~ ., data = train %>% select(Direction, Lag1, Lag2, Lag3, Lag5, Vol5), kernel = "radial")
pred_svm <- predict(models$svm, X_test)

# 6. Plot confusion matrices
plot_cm <- function(pred, truth, model_name) {
  cm <- confusionMatrix(factor(pred, levels = c("Down", "Up")), factor(truth, levels = c("Down", "Up")))
  ggplot(as.data.frame(cm$table), aes(Prediction, Reference, fill = Freq)) +
    geom_tile() +
    geom_text(aes(label = Freq), size = 6) +
    scale_fill_gradient(low = "white", high = "steelblue") +
    labs(title = paste("Confusion Matrix:", model_name))
}

plots <- list(
  plot_cm(pred_logit, y_test, "Logistic Regression"),
  plot_cm(pred_lda, y_test, "LDA"),
  plot_cm(pred_qda, y_test, "QDA"),
  plot_cm(pred_knn, y_test, "KNN"),
  plot_cm(pred_rf, y_test, "Random Forest"),
  plot_cm(pred_svm, y_test, "SVM")
)

# Save plots to PDF
pdf("plots/spy_classification_results.pdf", width = 12, height = 10)
for (p in plots) print(p)
dev.off()



