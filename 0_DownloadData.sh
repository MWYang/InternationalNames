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
