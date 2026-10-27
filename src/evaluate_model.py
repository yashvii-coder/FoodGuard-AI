from datasets import load_dataset
import tensorflow as tf
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import math
import os

print("Loading dataset...")

dataset = load_dataset("rajistics/indian_food_images")

test_data = dataset["test"]

class_names = test_data.features["label"].names

IMG_SIZE = (224, 224)
BATCH_SIZE = 8

print("\nTest images:", len(test_data))
print("Food classes:", len(class_names))


# ------------------------------------------------------------
# Load trained model
# ------------------------------------------------------------

print("\nLoading trained FoodGuard AI model...")

model = tf.keras.models.load_model(
    "models/foodguard_food_classifier.keras"
)

print("Model loaded successfully!")


# ------------------------------------------------------------
# Test image generator
# ------------------------------------------------------------

def test_generator():

    for item in test_data:

        image = item["image"]

        image = image.convert("RGB")

        image = image.resize(IMG_SIZE)

        image = np.asarray(
            image,
            dtype=np.float32
        )

        label = item["label"]

        yield image, label


# ------------------------------------------------------------
# Create TensorFlow dataset
# ------------------------------------------------------------

test_ds = tf.data.Dataset.from_generator(
    test_generator,
    output_signature=(
        tf.TensorSpec(
            shape=(224, 224, 3),
            dtype=tf.float32
        ),
        tf.TensorSpec(
            shape=(),
            dtype=tf.int32
        )
    )
)

test_ds = test_ds.batch(BATCH_SIZE)


# ------------------------------------------------------------
# Evaluate
# ------------------------------------------------------------

print("\n========================================")
print("EVALUATING FOODGUARD AI")
print("========================================")

loss, accuracy = model.evaluate(test_ds)

print("\nTest Loss:", round(loss, 4))
print("Test Accuracy:", round(accuracy * 100, 2), "%")


# ------------------------------------------------------------
# Predictions
# ------------------------------------------------------------

print("\nGenerating predictions...")

y_true = []
y_pred = []

for images, labels in test_ds:

    predictions = model.predict(
        images,
        verbose=0
    )

    predicted_labels = np.argmax(
        predictions,
        axis=1
    )

    y_true.extend(labels.numpy())
    y_pred.extend(predicted_labels)


# ------------------------------------------------------------
# Classification report
# ------------------------------------------------------------

print("\n========================================")
print("CLASSIFICATION REPORT")
print("========================================\n")

report = classification_report(
    y_true,
    y_pred,
    target_names=class_names,
    digits=4
)

print(report)


# ------------------------------------------------------------
# Confusion matrix
# ------------------------------------------------------------

cm = confusion_matrix(
    y_true,
    y_pred
)

print("\n========================================")
print("CONFUSION MATRIX")
print("========================================\n")

print(cm)


# ------------------------------------------------------------
# Save results
# ------------------------------------------------------------

os.makedirs("results", exist_ok=True)

with open(
    "results/classification_report.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "FOODGUARD AI - MODEL EVALUATION\n"
    )

    file.write(
        "================================\n\n"
    )

    file.write(
        f"Test Accuracy: {accuracy * 100:.2f}%\n"
    )

    file.write(
        f"Test Loss: {loss:.4f}\n\n"
    )

    file.write(report)

np.save(
    "results/confusion_matrix.npy",
    cm
)

print("\nEvaluation results saved in:")
print("results/classification_report.txt")

print("\nConfusion matrix saved in:")
print("results/confusion_matrix.npy")

print("\nEvaluation completed successfully!")