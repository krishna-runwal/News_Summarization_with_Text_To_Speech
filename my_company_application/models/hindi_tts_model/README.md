---
library_name: transformers
language:
- hi
license: mit
base_model: microsoft/speecht5_tts
tags:
- text-to-speech
- generated_from_trainer
datasets:
- mozilla-foundation/common_voice_11_0
model-index:
- name: SpeechT5 TTS hindi
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# SpeechT5 TTS hindi

This model is a fine-tuned version of [microsoft/speecht5_tts](https://huggingface.co/microsoft/speecht5_tts) on the common_voice_11_0 dataset.
It achieves the following results on the evaluation set:
- Loss: 0.4304

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 1e-05
- train_batch_size: 16
- eval_batch_size: 8
- seed: 42
- gradient_accumulation_steps: 4
- total_train_batch_size: 64
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- lr_scheduler_warmup_steps: 500
- training_steps: 4000
- mixed_precision_training: Native AMP

### Training results

| Training Loss | Epoch   | Step | Validation Loss |
|:-------------:|:-------:|:----:|:---------------:|
| 0.4659        | 15.1515 | 1000 | 0.4438          |
| 0.4534        | 30.3030 | 2000 | 0.4314          |
| 0.4482        | 45.4545 | 3000 | 0.4300          |
| 0.433         | 60.6061 | 4000 | 0.4304          |


### Framework versions

- Transformers 4.44.2
- Pytorch 2.5.0+cu121
- Datasets 3.1.0
- Tokenizers 0.19.1
