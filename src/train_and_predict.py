"""
Trains a Random Forest classifier on Sparkify user engagement features
and writes churn predictions back to BigQuery.
"""

from google.cloud import bigquery
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

PROJECT_ID = "spotify-churn-pipeline"
SOURCE_TABLE = "spotify-churn-pipeline.sparkify_churn.user_features"
OUTPUT_TABLE = "spotify-churn-pipeline.sparkify_churn.churn_predictions"

# Classification threshold chosen to favor recall over precision, since
# missing an at-risk user (false negative) is more costly in a retention
# context than a low-cost false-positive outreach. See README for details.
CHURN_THRESHOLD = 0.35


def load_features(client):
    query = f"SELECT * FROM `{SOURCE_TABLE}`"
    return client.query(query).to_dataframe()


def train_model(df):
    X = df.drop(columns=['userId', 'has_churned'])
    y = df['has_churned']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)

    # Evaluation on held-out test set
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= CHURN_THRESHOLD).astype(int)

    print("Classification Report (test set, threshold=%.2f):" % CHURN_THRESHOLD)
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.3f}")

    return model, X.columns


def assign_risk_segment(prob):
    if prob >= 0.6:
        return 'High Risk'
    elif prob >= CHURN_THRESHOLD:
        return 'Medium Risk'
    else:
        return 'Low Risk'


def generate_predictions(model, df, feature_columns):
    X_all = df[feature_columns]
    probabilities = model.predict_proba(X_all)[:, 1]

    predictions_df = pd.DataFrame({
        'user_id': df['userId'],
        'churn_probability': probabilities
    })
    predictions_df['risk_segment'] = predictions_df['churn_probability'].apply(assign_risk_segment)
    return predictions_df


def write_predictions(client, predictions_df):
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(predictions_df, OUTPUT_TABLE, job_config=job_config)
    job.result()
    print(f"Loaded {job.output_rows} rows into {OUTPUT_TABLE}")


if __name__ == "__main__":
    client = bigquery.Client(project=PROJECT_ID)

    df = load_features(client)
    model, feature_columns = train_model(df)
    predictions_df = generate_predictions(model, df, feature_columns)
    write_predictions(client, predictions_df)