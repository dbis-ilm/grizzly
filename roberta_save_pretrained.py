from transformers import RobertaForSequenceClassification, RobertaTokenizer

tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
tokenizer.save_pretrained("myroberta")
