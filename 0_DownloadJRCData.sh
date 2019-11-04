wget https://wt-public.emm4u.eu/data/entities.gzip
mv entities.gzip entities.gz
gzip -d entities.gz
mkdir input
mv entities input/JRCRawData.txt
