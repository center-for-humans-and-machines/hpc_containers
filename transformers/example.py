import math

from datasets import Dataset
from transformers import AutoTokenizer
from transformers import DataCollatorForLanguageModeling
from transformers import AutoModelForCausalLM, TrainingArguments, Trainer
import os


print(os.environ)


def main():
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

    ds = Dataset.from_dict({"text": [" ".join(["I will learn to repeat myself!"]*10)] * 5000})
    ds = ds.train_test_split(test_size=0.2)

    def preprocess_function(examples):
        result = tokenizer(examples["text"])
        result["labels"] = result["input_ids"].copy()
        return result

    tokenized_ds = ds.map(preprocess_function, batched=True)

    tokenizer.pad_token = tokenizer.eos_token
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir="model",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_ds["train"],
        eval_dataset=tokenized_ds["test"],
        data_collator=data_collator,
    )

    trainer.train()

    eval_results = trainer.evaluate()
    print(f"Perplexity: {math.exp(eval_results['eval_loss']):.2f}")


if __name__ == "__main__":
    main()
