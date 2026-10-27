from datasets import load_dataset

print("Loading dataset...")

dataset = load_dataset("rajistics/indian_food_images")

train_data = dataset["train"]

print("\nTotal training images:", len(train_data))

print("\nFood classes:")
print(train_data.features["label"].names)

print("\nNumber of food classes:",
      len(train_data.features["label"].names))