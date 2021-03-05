# This repository is fork of [BERT](https://github.com/google-research/bert)

For export model as saved model, I added export functionality to run_squad.py.

## Saved Model signature
```sh
$ saved_model_cli show --dir <pb basename> --tag_set serve --signature_def serving_default
The given SavedModel SignatureDef contains the following input(s):
  inputs['input_ids'] tensor_info:
      dtype: DT_INT32
      shape: (-1, 384)
      name: input_ids_1:0
  inputs['input_mask'] tensor_info:
      dtype: DT_INT32
      shape: (-1, 384)
      name: input_mask_1:0
  inputs['label_ids'] tensor_info:
      dtype: DT_INT32
      shape: (-1)
      name: label_ids_1:0
  inputs['segment_ids'] tensor_info:
      dtype: DT_INT32
      shape: (-1, 384)
      name: segment_ids_1:0
  inputs['unique_ids'] tensor_info:
      dtype: DT_INT32
      shape: (-1)
      name: unique_ids_1:0
The given SavedModel SignatureDef contains the following output(s):
  outputs['end_logits'] tensor_info:
      dtype: DT_FLOAT
      shape: (-1, 384)
      name: unstack:1
  outputs['start_logits'] tensor_info:
      dtype: DT_FLOAT
      shape: (-1, 384)
      name: unstack:0
  outputs['unique_ids'] tensor_info:
      dtype: DT_INT32
      shape: (-1)
      name: unique_ids_1:0
Method name is: tensorflow/serving/predict
```



