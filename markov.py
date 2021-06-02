#! /Users/Luca/miniconda3/envs/markov_test/bin/python3
import json
import argparse
from random import choice

def generate_model(text):
	model = {}
	for i in range(len(text) - 1):
		curr_word = text[i]
		next_word = text[i+1]
		if not curr_word in model:
			model[curr_word] = {}
		if not next_word in model[curr_word]:
			model[curr_word][next_word] = 1 
		else:
			model[curr_word][next_word] += 1
	return model

def generate_ngram_model(text, ngram):
	model = {}
	for i in range(1, len(text) - 1):
		prev_word = text[i-1]
		curr_word = text[i]
		next_word = text[i+1]
		if not curr_word in model:
			model[curr_word] = {}
		if not next_word in model[curr_word]:
			model[curr_word][next_word] = 1 
		else:
			model[curr_word][next_word] += 1
	return model


def predict_next_token(model, word):
	choices = []
	for next_word in model[word].keys():
		for occurances in range(0, model[word][next_word]):
			choices.append(next_word)
	return choice(choices)

def generate_text(model, word, max_depth=10):
	next_token = predict_next_token(model, word)
	if max_depth == 1:
		return word + " " + next_token
	else:
		return word + " " + generate_text(model, next_token, max_depth-1)

def load_text(file_name):
	text = []
	with open(file_name, "r") as _file:
		for line in _file:
			text.extend(line.split(" "))
		for i in range(len(text)):
			text[i] = text[i].lower()
	return text

def write_model(model):
	with open('model.json', 'w') as _file:
		json.dump(model, _file, sort_keys=True, indent=4)

def load_model(filepath="model.json"):
	with open(filepath, 'r') as _file:
		return json.load(_file)


def get_parser():
	parser = argparse.ArgumentParser(
		description = "A Simple Markov Chain Tool"
	)

	parser.add_argument(
		"-t", "--text", type=str, help="Text Source File"
	)

	parser.add_argument(
		"-s", "--seed", type=str, help="Seed Token"
	)

	parser.add_argument(
		"-r", "--recur", type=int, help="Recursion Depth"
	)

	parser.add_argument(
		"-n", "--ngram", type=int, help="Number of Tokens"
	)
	
	return parser

def main(args: argparse.Namespace):

	if args.text is not None:
		text = load_text(args.text)
		if args.ngram:
			model = generate_ngram_model(text, args.ngram)
		else:
			model = generate_model(text)
		write_model(model)
	elif args.seed is not None:
		model = load_model()
		if args.recur:
			text = generate_text(model, args.seed, args.recur)
		else:
			text = generate_text(model, args.seed)
		print(text)

if __name__ == "__main__":
	parser = get_parser()
	args = parser.parse_args()
	main(args)

