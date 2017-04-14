#!/bin/bash
# Copyright 2015-2016  Sarah Flora Juan
# Copyright 2016  Johns Hopkins University (Author: Yenda Trmal)
# Apache 2.0

resourcedir=$1
datadir=$2

mkdir -p ${datadir}/lang ${datadir}/local/dict


cp $resourcedir/lexicon.txt ${datadir}/local/dict/lexicon.txt
echo "!SIL	SIL" >> ${datadir}/local/dict/lexicon.txt
echo "<unk>	SPN" >> ${datadir}/local/dict/lexicon.txt
env LC_ALL=C sort -u -o ${datadir}/local/dict/lexicon.txt ${datadir}/local/dict/lexicon.txt
cat ${datadir}/local/dict/lexicon.txt | \
    perl -ane 'print join("\n", @F[1..$#F]) . "\n"; '  | \
    sort -u | grep -v 'SIL' > ${datadir}/local/dict/nonsilence_phones.txt


touch ${datadir}/local/dict/extra_questions.txt
touch ${datadir}/local/dict/optional_silence.txt

echo "SIL"   > ${datadir}/local/dict/optional_silence.txt
echo "SIL"   > ${datadir}/local/dict/silence_phones.txt
echo "<UNK>" > ${datadir}/local/dict/oov.txt

echo "Dictionary preparation succeeded"
