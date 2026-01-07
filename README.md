Satellite Imagery Based Property Valuation

This project focuses on predicting residential property prices by combining tabular housing attributes with satellite imagery using a multimodal learning approach.

The objective is to analyze whether satellite images provide additional spatial and contextual information beyond traditional housing features.

Dataset Description

The dataset consists of two main components:

1. Tabular Property Data

Includes structured housing attributes such as:

Bedrooms, bathrooms Living area and lot size
Floors, waterfront, view
Condition, grade
Latitude and longitude.

2. Satellite Images

Satellite images are fetched using Mapbox Static Images API
Each image corresponds to a property’s latitude–longitude location
Images are used to capture spatial context such as neighborhood density, surroundings, and layout.

Methodology
Data Preprocessing

Log transformation applied to property prices to stabilize variance.
Standard scaling applied to numerical features.
Train–validation split performed on the merged dataset.

Baseline Model:

Linear Regression using only tabular features.
Serves as a benchmark for comparison.

Multimodal Model:

Tabular features combined with image-derived features.
Linear Regression trained on the combined feature space.
Demonstrates improvement over the baseline model.

Model Performance:

when the model is tabular only the RMSE and R2 Score was ~0.26 and ~0.75 respectively and when we use the Multimodal (Tabular+Image) the RMSE and R2 Score is ~0.24 and ~0.79 

The results show that incorporating satellite imagery improves predictive performance.

Model Interpretability (Grad-CAM):

Grad-CAM visualizations are used to highlight important regions in satellite images that influence the model’s predictions.

These visualizations indicate that the model focuses on:

Built-up areas

Property structures

Surrounding neighborhood patterns.

This provides qualitative evidence that satellite imagery contributes meaningful spatial information.

Notes:

Raw satellite images are not included in the repository due to size constraints.

Image fetching requires a valid Mapbox API token.
