set -eux

wscraper initialize
wscraper root set --language japanese --page_chunk 1000
wscraper root unset --language
wscraper import workspace/sample.xml --name old
wscraper switch old
wscraper status
wscraper set --language japanese
wscraper status
wscraper rename old new
