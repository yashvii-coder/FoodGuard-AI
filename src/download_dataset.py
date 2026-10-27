from datasets import load_dataset

print("Downloading Indian Food dataset...")

dataset = load_dataset("rajistics/indian_food_images")

print("\nDataset downloaded successfully!")
print(dataset)

print("\nTraining samples:", len(dataset["train"]))