"""A client that talks to tensorflow_model_server loaded with korquad model.

Example Run
```sh
bazel-bin/client/client \
--context "이순신 장군 나이는 36세이다." \
--question "이순신 장군의 나이는?" \
--vocab_file ~/data/bert_finetuned/vocab.txt
```
"""
import random
import tokenization
import unicodedata

from absl import app
from absl import flags
from absl import logging
import grpc
import numpy as np
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

FLAGS = flags.FLAGS
flags.DEFINE_string('context', None, 'Context for question.')
flags.DEFINE_integer('max_seq_length', 384, 'Maximum total input sequence length')
flags.DEFINE_string('question', None, 'Question for context.')
flags.DEFINE_string('vocab_file', None, 'Vocab file for tokenizer.')
flags.DEFINE_string('server', 'localhost:8500', '<IP>:<Port> address.')


def make_input_for_model(tokenizer, question, context, max_seq_length):
	question_tokens = tokenizer.tokenize(question)
	logging.info(f'{question} -> {question_tokens}')
	context_tokens = tokenizer.tokenize(context)
	logging.info(f'{context} -> {context_tokens}')

	max_tokens_for_doc = max_seq_length - len(question_tokens) - 3
	context_tokens = context_tokens[:max_tokens_for_doc]

	tokens = []
	segment_ids = []
	tokens.append('[CLS]')
	segment_ids.append(0)
	for token in question_tokens:
		tokens.append(token)
		segment_ids.append(0)
	tokens.append('[SEP]')
	segment_ids.append(0)
	for token in context_tokens:
		tokens.append(token)
		segment_ids.append(1)
	tokens.append('[SEP]')
	segment_ids.append(1)

	input_ids = tokenizer.convert_tokens_to_ids(tokens)
	input_mask = [1] * len(input_ids)

	while len(input_ids) < max_seq_length:
		input_ids.append(0)
		input_mask.append(0)
		segment_ids.append(0)
	
	return input_ids, input_mask, segment_ids


def do_inference(stub, input_ids, input_mask, segment_ids, unique_ids):
	request = predict_pb2.PredictRequest()
	request.model_spec.name = 'korquad_v1'
	request.model_spec.signature_name = 'serving_default'
	request.inputs['input_ids'].CopyFrom(
		tf.make_tensor_proto(input_ids, shape=[1, len(input_ids)]))
	request.inputs['input_mask'].CopyFrom(
		tf.make_tensor_proto(input_mask, shape=[1, len(input_mask)]))
	request.inputs['segment_ids'].CopyFrom(
		tf.make_tensor_proto(segment_ids, shape=[1, len(segment_ids)]))
	request.inputs['unique_ids'].CopyFrom(
		tf.make_tensor_proto(unique_ids, shape=[1]))
	
	result_future = stub.Predict.future(request, 5.0)
	return result_future

def main(Unused):
	del Unused  # Unused.

	tokenizer = tokenization.FullTokenizer(vocab_file=FLAGS.vocab_file,	do_lower_case=True)
	logging.info(tokenizer.tokenize(unicodedata.normalize('NFD', '이순신')))

	input_ids, input_mask, segment_ids = make_input_for_model(
		tokenizer, FLAGS.question, FLAGS.context, FLAGS.max_seq_length)

	with grpc.insecure_channel(FLAGS.server) as channel:
		stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
		result_future = do_inference(stub, input_ids, input_mask, segment_ids, random.randint(0,100))
		outputs = result_future.result()
		start_index = np.argmax(outputs.outputs['start_logits'].float_val)
		end_index = np.argmax(outputs.outputs['end_logits'].float_val)
		logging.info(f'start: {start_index}, end: {end_index}')
		logging.info(f'Answer: {tokenizer.tokenize(FLAGS.context)[start_index:end_index]}')
		#logging.info(result_future.result())
		
		
	

if __name__ == '__main__':
	app.run(main)
