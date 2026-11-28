from pathlib import Path
import string
import random
OUT_DIR=Path('stat_files')
OUT_DIR.mkdir(parents=True,exist_ok=True)
PLAN={'.docx':3,'.xlsx':3,'.pdf':3,'.txt':4,'.csv':2,'.json':2,'.md':2,'':4,'.bin':3,'.zip':2,'.jpg':1,'.png':1}

def random_text(n):
    return ''.join(random.choices(string.ascii_letters+string.digits+' /n',k=n))
def build_one(name):
    path=OUT_DIR/name
    if path.suffix.lower()=='.bin':
        path.write_bytes(random.randbytes(random.randint(100,512)))
    else:
        path.write_text(random_text(random.randint(100,500)))


