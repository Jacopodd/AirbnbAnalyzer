import gzip
import shutil

with gzip.open("../data/reviews.csv.gz", 'rb') as f_in:
    with open("../data/review.csv", 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print("✅ File estratto come calendar.csv")
