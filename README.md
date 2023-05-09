# Scripts to extract abstracts from arXiv's XML API

Papers in arXiv are organized in categories, like `cs.CL` for computational linguistics or `cs.LG` for machine learning. To download all abstracts in a category and then extract abstracts to a tab-delimited file, run

    python get.py cs.CL
    python parse.py cs.CL > cs.CL.tsv

This script follows the [arXiv API terms of use](https://info.arxiv.org/help/api/tou.html), which does not allow more than one query per three seconds. You will stop getting results if you go faster.

The parse script creates a tab-delimited file with three columns: the arXiv id, the year and month, and the text. By default it repeats the title twice, following Talley et al. in Nature Methods.

To use Mallet for topic modeling, run the following import commands to generate a custom high-frequency word list as candidates for a stoplist.

    Mallet/bin/mallet import-file --input cs.CL.tsv --output cs.CL.mallet --keep-sequence
    Mallet/bin/mallet info --print-feature-counts --input cs.CL.mallet | sort -rn -k 2 > vocab.txt
    head -200 vocab.txt | cut -f 1 > stoplist.txt

I suggest editing the stoplist by hand at this point.

To import and run a model, these commands run 1000 sampling burn-in iterations and then an additional 1000 iterations saving sampling states every 100 iterations.

    Mallet/bin/mallet import-file --input cs.CL.tsv --output cs.CL.stopped.mallet --keep-sequence --stoplist-file stoplist.txt
    Mallet/bin/mallet train-topics --input cs.CL.stopped.mallet --num-topics 100 --optimize-interval 20 --optimize-burn-in 50 --output-state cl-t100.state.gz
    Mallet/bin/mallet train-topics --input cs.CL.stopped.mallet --num-topics 100 --input-state cl-t100.state.gz --output-state cl-t100.state.iter.gz --output-state-interval 100

Finally, to generate summary files for topics and document-topic distributions:

    python to_tsv.py cs.CL.tsv 100 cl-t100.state.iter.gz*
