import gzip, sys
from collections import Counter

tags_filename = sys.argv[1]
num_topics = int(sys.argv[2])

document_ids = []
document_tags = []
tag_topic_counts = {}
tag_totals = Counter()

id_topic_counts = {}

topic_totals = Counter()
topic_word_counts = []
for topic in range(num_topics):
    topic_word_counts.append(Counter())

with open(tags_filename) as tag_reader:
    for line in tag_reader:
        fields = line.split("\t")
        doc_id = fields[0]
        tag = fields[1]
        document_ids.append(doc_id)
        document_tags.append(tag)
        
        if not tag in tag_topic_counts:
            tag_topic_counts[tag] = Counter()
            
for state_filename in sys.argv[3:]:
    with gzip.open(state_filename, "rt") as state_reader:
        for line in state_reader:
            if not line.startswith("#"):
            
                fields = line.split(" ")
                doc_id = int(fields[0])
                word = fields[4]
                topic = int(fields[5])
            
                tag = document_tags[doc_id]
            
                tag_topic_counts[tag][topic] += 1
                tag_totals[tag] += 1
            
                topic_word_counts[topic][word] += 1
                topic_totals[topic] += 1

sorted_tags = sorted(list(tag_totals.keys()))

with open("tag_topics.tsv", "w") as tag_topic_writer:
    tag_topic_writer.write("Tag\tTopic\tCount\n")
    for tag in sorted_tags:
        for topic in range(num_topics):
            tag_topic_writer.write("{}\t{}\t{}\n".format(tag, topic, tag_topic_counts[tag][topic]))

with open("topic_words.tsv", "w") as topic_writer:
    topic_writer.write("Topic\tWords\n")
    for topic in range(num_topics):
        words = [w for (w, c) in topic_word_counts[topic].most_common(50)]
        topic_writer.write("{}\t{}\n".format(topic, " ".join(words)))

