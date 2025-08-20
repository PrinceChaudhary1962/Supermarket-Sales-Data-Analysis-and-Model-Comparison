
# 🛒 Supermarket Sales Data Analysis and Model Comparison

This project focuses on exploratory data analysis (EDA) and performance comparison of machine learning algorithms using a supermarket sales dataset. The goal is not to predict future sales, but to evaluate the effectiveness of different models on the existing dataset.

## 📌 Objective

- Perform comprehensive EDA on the supermarket sales dataset
- Compare classification algorithms (K-Nearest Neighbors, Random Forest, etc.)
- Visualize insights and evaluate model accuracy

## 📊 Dataset

The dataset includes features such as:
- Branch, City, Customer type, Gender
- Product line, Unit price, Quantity
- Tax, Total, Date, Time, Payment Method
- Customer Ratings

> The dataset was cleaned and preprocessed to handle categorical and numerical features for model training.

## 🧰 Tools & Technologies

- **Python** (Pandas, NumPy, Matplotlib, Seaborn)
- **Scikit-learn** (KNN, RandomForestClassifier, train-test split, LabelEncoder)
- **Jupyter Notebook** for analysis and visualization

## ⚙️ Models Compared

| Model                  | Description                                  |
|------------------------|----------------------------------------------|
| K-Nearest Neighbors    | Distance-based classifier                    |
| Random Forest Classifier | Ensemble of decision trees for better generalization |

## 📈 Performance Metrics

- Accuracy
- Confusion Matrix
- Classification Report

> The dataset was split into training and testing sets to validate the models' generalization capabilities.

## 📌 Key Insights

- Gender and Product Line were influential in patterns of purchase
- Random Forest outperformed KNN on accuracy
- Clear visualization of categorical distributions helped in understanding customer behavior

## 📂 Folder Structure
```supermarket-sales-analysis/
│
├── 📄 README.md                     # Project description and usage
├── 📄 requirements.txt             # Python libraries needed
├── 📄 .gitignore                   # Files/folders to ignore in version control
│
├── 📒 sales_Prediction_and_EDA.ipynb  # Main Jupyter Notebook
│
├── 📁 data/                        # Dataset storage
│   └── supermarket_sales.csv
│
├── 📁 images/                      # Visualizations for README or documentation
│   └── correlation_matrix.png
│   └── model_accuracy_plot.png
│
├── 📁 src/                         # (Optional) Python scripts if modularized
│   └── preprocessing.py
│   └── model_comparison.py
│
└── 📁 outputs/                     # (Optional) Exported reports, model files
    └── confusion_matrix.png
    └── classification_report.txt
