# Code to generate a tSNE plot of single cell data
# Includes Hotellings T2 ellipses and p-values
# matt.spick@surrey.ac.uk, 19 September 2024

# Load necessary libraries and .csv
library(ICSNP)
library(ggplot2)
library(Rtsne)
data <- read.csv("csv_with_data.csv")

# Sample should be in column 1 and Class in column 2

# This assumes data are not scaled and include NAs, replaces NAs with half-min
features <- data[, -c(1, 2)]
features_cleaned <- features[, colSums(is.na(features)) < nrow(features)]
features_cleaned <- features_cleaned[, sapply(features_cleaned, function(x) length(unique(na.omit(x))) > 1)]
features_imputed <- apply(features_cleaned, 2, function(x) {
  min_value <- min(x, na.rm = TRUE)  # Find the minimum value for each column
  x[is.na(x)] <- 0.5 * min_value     # Replace NA with half of the minimum value
  return(x)
})

# Rebuild the dataset with imputed features, keeping 'Sample' and 'Class' columns
# Does dimension reduction by tSNE
data_imputed <- data.frame(data[, 1:2], features_imputed)
sample_col <- data_imputed[, 1]  # Sample column
class_col <- data_imputed[, 2]   # Class column
features <- data_imputed[, -c(1, 2)]  # All remaining columns are features
set.seed(42)  # For reproducibility
tsne_result <- Rtsne(features, dims = 2, perplexity = 5, verbose = TRUE, max_iter = 1000)

# t-SNE coordinates
tsne_data <- data.frame(tsne_result$Y, Class = class_col)
colnames(tsne_data) <- c("tSNE1", "tSNE2", "Class")

# Perform Hotelling's T² test using the t-SNE transformed data
class1 <- tsne_data[tsne_data$Class == unique(class_col)[1], c("tSNE1", "tSNE2")]
class2 <- tsne_data[tsne_data$Class == unique(class_col)[2], c("tSNE1", "tSNE2")]
hotelling_result <- HotellingsT2(class1, class2)
t2_statistic <- hotelling_result$statistic
p_value <- hotelling_result$p.value

# Make plot
plot_title <- paste0("t-SNE with Hotelling's T² Ellipses\nT² Statistic: ", round(t2_statistic, 2), 
                     ", p-value: ", format.pval(p_value, digits = 3))
ggplot(tsne_data, aes(x = tSNE1, y = tSNE2, color = Class)) +
  geom_point(size = 3) +
  stat_ellipse(level = 0.95, linetype = "dashed", size = 1.2) +  # 95% confidence ellipse
  theme_minimal() +
  labs(title = plot_title,
       x = "t-SNE Dimension 1",
       y = "t-SNE Dimension 2")

t2_statistic
p_value

