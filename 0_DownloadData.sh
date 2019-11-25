mkdir input
cd input

wget https://wt-public.emm4u.eu/data/entities.gzip
mv entities.gzip entities.gz
gzip -d entities.gz
mv entities JRCRawData.txt

wget https://github.com/OpenGenderTracking/globalnamedata/raw/master/assets/usprocessed.csv
wget https://github.com/OpenGenderTracking/globalnamedata/raw/master/assets/ukprocessed.csv

wget https://github.com/first20hours/google-10000-english/raw/master/google-10000-english-usa.txt
wget https://github.com/first20hours/google-10000-english/raw/master/google-10000-english.txt

wget https://gist.githubusercontent.com/Miserlou/11500b2345d3fe850c92/raw/e36859a9eef58c231865429ade1c142a2b75f16e/gistfile1.txt -O 'top_1000_us_cities.txt'