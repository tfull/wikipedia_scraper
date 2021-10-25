set -eux

wscraper initialize
wscraper root set --language japanese --page_chunk 1000
wscraper root unset --language
wscraper import workspace/sample.xml --name old --copy
wscraper import workspace/sample.xml --name sample --copy
wscraper switch old
wscraper status
wscraper set --language japanese
wscraper status
wscraper rename old new
wscraper switch sample
wscraper set --language japanese
ls ~/.wscraper/wikipedia
wscraper delete new
ls ~/.wscraper/wikipedia

python code.py
