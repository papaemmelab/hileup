import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pysam
import chileup

config = chileup.Config(tags=[], track_read_names=True,
            track_base_qualities=True, track_mapping_qualities=True,
            exclude_flags=pysam.FQCFAIL | pysam.FSECONDARY | pysam.FSUPPLEMENTARY | pysam.FDUP,
            min_base_quality=10, min_mapping_quality=10)

def test_off_by_one():
    bam = pysam.AlignmentFile("tests/soft.bam", "rb")
    pos = 10080
    h = chileup.pileup(bam, "1", pos, config)
    assert h.bases == b"", h.bases

def test_insertion():
    bam = pysam.AlignmentFile("tests/three.bam", "rb")
    pos = 1585270
    h = chileup.pileup(bam, "1", pos, config)
    assert h.bases == b'TT'
    assert len(h.deletions) == 2


def main(bam, config):

    for pos in range(10000, 12000):
        h = chileup.pileup(bam, "1", pos, config)
        print(pos, h.bases, len(h.bqs), len(h.deletions), len(h.insertions))

if __name__ == "__main__":
    bam = pysam.AlignmentFile("/data/human/hg002.cram", "rc",
                reference_filename="/data/human/g1k_v37_decoy.fa")

    config = chileup.Config(tags=[], track_read_names=True,
            track_base_qualities=True, track_mapping_qualities=True,
            exclude_flags=pysam.FQCFAIL | pysam.FSECONDARY | pysam.FSUPPLEMENTARY | pysam.FDUP,
            min_base_quality=10, min_mapping_quality=10)

    pos = 10080
    h = chileup.pileup(bam, "1", pos, config)
    #print(pos, h.bases)
    test_off_by_one()
    test_insertion()

    #main(bam, config)