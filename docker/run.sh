set -eux

pip install sqlalchemy
pip install gensim

wscraper initialize
wscraper root set --page_chunk 100
wscraper new my_task
wscraper switch my_task
wscraper import workspace/sample.xml --name mini
wscraper set --wikipedia mini --worker 2 --language japanese
wscraper tokenizer mecab
wscraper model new w2v word2vec
wscraper model new wf word_frequency
wscraper model new d2v doc2vec
wscraper model build -r
wscraper database set --dialect mysql --user user --password password --host mysql --port 3306 --database wscraper
wscraper database migrate -r
wscraper database seed -r
