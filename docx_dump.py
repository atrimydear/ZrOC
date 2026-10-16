import zipfile, sys
from xml.etree import ElementTree as ET
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
out = []
for f in sys.argv[1:]:
    out.append("="*60); out.append("FILE: " + f); out.append("="*60)
    z = zipfile.ZipFile(f)
    root = ET.fromstring(z.read("word/document.xml").decode("utf-8","ignore"))
    for p in root.iter(W+"p"):
        t = "".join((x.text or "") for x in p.iter(W+"t"))
        if t.strip(): out.append(t)
    out.append("")
open(r"D:\Knowledge\LaTeX\实验计划\模板文本.txt","w",encoding="utf-8").write("\n".join(out))
print("ok")
