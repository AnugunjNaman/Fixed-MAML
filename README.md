# Fixed-MAML
Fixed-MAML: Speech Emotion Recognition.
The repository is inspired from MAML [Pytorch Implementation](
https://github.com/dragen1860/MAML-Pytorch)
#### Steps to reproduce the results.

 1. Download the [EmoFilm Dataset](https://zenodo.org/record/1326428#.X8sFStgzZPY).
 2. Split the dataset based on language and emotion.
 3. Generate silence class label data and download neutral data from [EmoDB-dataset](http://emodb.bilderbar.info/start.html) or you can generate it yourself. 
 4. Create a csv file accordingly to train and run the model.
 5. Keep all the wav files in in data/waveforms/<class labels>/ and csv files in data/ .
 6. After that run train.py with appropriate changes to location for csv and data input.
  
 
