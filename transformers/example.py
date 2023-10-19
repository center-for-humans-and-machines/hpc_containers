# Reference: https://huggingface.co/docs/transformers/tasks/language_modeling
import math

from datasets import Dataset
from transformers import AutoTokenizer
from transformers import DataCollatorForLanguageModeling
from transformers import AutoModelForCausalLM, TrainingArguments, Trainer
# import os
# print(os.environ)


def main():
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

    ds = Dataset.from_text("./input.txt")
    ds = ds.train_test_split(test_size=0.2)

    def tokenize(examples):
        return tokenizer(examples["text"])

    tokenized_ds = ds.map(tokenize, batched=True, remove_columns=["text"])

    def chunk_text(examples):
        chunk_size = 128
        # Concatenate tokens of the batch
        examples = {key: sum(examples[key], []) for key in examples}
        # Split tokens into chunks of chunk_size
        # We will drop the remainder of size < chunk_size
        total_length = len(examples["input_ids"])
        max_length = (total_length // chunk_size) * chunk_size
        examples = {
            key: [value[i : i + chunk_size] for i in range(0, max_length, chunk_size)]
            for key, value in examples.items()
        }
        examples["labels"] = examples["input_ids"].copy()

        return examples

    lm_ds = tokenized_ds.map(chunk_text, batched=True)

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
        train_dataset=lm_ds["train"],
        eval_dataset=lm_ds["test"],
        data_collator=data_collator,
    )

    trainer.train()

    eval_results = trainer.evaluate()
    print(f"Perplexity: {math.exp(eval_results['eval_loss']):.2f}")


if __name__ == "__main__":
    main()
