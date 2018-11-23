sort -R output.csv > output_randomized.csv
head -n 6370 output_randomized.csv > output.train
tail -n 2000 output_randomized.csv > output.valid
./fasttext supervised -input output.train -output model_output
./fasttext supervised -input output.train -output model_output -epoch 25 -wordNgrams 2
