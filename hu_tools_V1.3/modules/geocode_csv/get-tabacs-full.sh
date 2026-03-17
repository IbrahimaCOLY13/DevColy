#!/usr/bin/env bash

wget https://www.douane.gouv.fr/sites/default/files/openData/files/annuaire-des-debits-de-tabac-2018.zip
unp annuaire-des-debits-de-tabac-2018.zip
cat annuaire-des-debits-de-tabac-2018.csv | iconv -f WINDOWS-1252 -t UTF-8 >| annuaire-des-debits-de-tabac-2018-utf8.csv
head -n 20 annuaire-des-debits-de-tabac-2018-utf8.csv > annuaire-des-debits-de-tabac-2018-utf8-20lines.csv
