minimap2 -ax sr ../../reference.fasta results/merged_reads.fastq > aligned.sam

samtools view -bS aligned.sam > aligned.bam

samtools sort -o aligned_sorted.bam aligned.bam

samtools index aligned_sorted.bam

# Make sure to use the correct BED file
ivar trim -b ../../DENV3.bed -p trimmed -i aligned_sorted.bam -q 15 -m 50 -s 4 -e

samtools sort -o trimmed_sorted.bam trimmed.bam && samtools index trimmed_sorted.bam

samtools mpileup -aa -A -d 600000 -Q 20 -q 0 -B -f ../../reference.fasta trimmed_sorted.bam | cut -f1-4 > depths.tsv

freyja variants trimmed_sorted.bam --variants variants.tsv --depths depths.tsv --ref ../../reference.fasta

freyja demix variants.tsv depths.tsv --output freyja_demix.txt --barcodes ../../barcode.csv