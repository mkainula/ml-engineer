### NLP model

Data from sfnet.tar.gz, try to predict newsgroup group name from message. Preprocessor just creates a file with single row for each message with __label__newsgroup_name.

Example :

```
λ  fastText-0.1.0 ./fasttext supervised -input output.train -output model_output -epoch 25 -wordNgrams 2
Read 1M words
Number of words:  166312
Number of labels: 79
Progress: 100.0%  words/sec/thread: 1008038  lr: 0.000000  loss: 2.509740  eta: 0h0m

λ  fastText-0.1.0 ./fasttext test model_output.bin output.valid
N    1992
P@1    0.771
R@1    0.771
Number of examples: 1992
```
