🧬 Fine-tuning my own LLM with LoRA! ✨

Recently, I took a deep dive into Large Language Model fine-tuning using the Qwen/Qwen3-1.7B model from Hugging Face. At first, the model didn’t recognize who I was — so I decided to fix that! 😄

Using a custom dataset describing my characteristics and background, I fine-tuned the model so it could better understand and reflect my persona. This project taught me a lot about prompt engineering, tokenization, and parameter-efficient fine-tuning (PEFT) methods like LoRA.

💡 Since my local GPU (with only 4GB VRAM) couldn’t handle the heavy lifting, I ran the training process on Google Colab, which provided the necessary CUDA resources to get the job done efficiently.

The workflow included:

🧠 Loading and preprocessing a custom JSON dataset
🪶 Applying LoRA fine-tuning for efficient adaptation
🔧 Training the model with Hugging Face’s Trainer
💾 Saving and testing the fine-tuned model

It was fascinating to see the difference between the model’s answers before and after fine-tuning — now it actually knows who Sógor Gergely is! 🥳

#MachineLearning #AI #DeepLearning #LLM #LoRA #FineTuning #NLP #DataScience #HuggingFace #Qwen #GoogleColab #Python #MLProjects #CUDA