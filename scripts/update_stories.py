import json,re,urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

URL="https://academicallamerica.com/archives.aspx"
LIMIT=10
DATE=re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")

class P(HTMLParser):
    def __init__(self): super().__init__();self.table=False;self.row=False;self.cell=False;self.rows=[];self.cells=[];self.text=[];self.href="";self.ltext=[]
    def handle_starttag(self,t,a):
        t=t.lower()
        if t=="table" and not self.table:self.table=True
        elif self.table and t=="tr":self.row=True;self.cells=[]
        elif self.row and t in ("td","th"):self.cell=True;self.text=[];self.href="";self.ltext=[]
        elif self.cell and t=="a":self.href=dict(a).get("href","");self.ltext=[]
    def handle_data(self,d):
        if self.cell:self.text.append(d);self.ltext.append(d) if self.href else None
    def handle_endtag(self,t):
        t=t.lower()
        if t in ("td","th") and self.cell:
            self.cells.append((" ".join("".join(self.text).split()),self.href," ".join("".join(self.ltext).split())));self.cell=False
        elif t=="tr" and self.row:
            if self.cells:self.rows.append(self.cells)
            self.row=False
        elif t=="table" and self.table:self.table=False

req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req,timeout=30) as r: html=r.read().decode("utf-8","replace")
p=P();p.feed(html)
out=[]
for row in p.rows:
    if not row or not DATE.match(row[0][0]): continue
    linkcell=next((x for x in row if x[1] and x[2]),None)
    if not linkcell: continue
    out.append({"title":linkcell[2],"date":row[0][0],"link":urljoin(URL,linkcell[1])})
    if len(out)>=LIMIT: break
if len(out)<LIMIT: raise RuntimeError(f"Found only {len(out)} stories")
open("stories.json","w",encoding="utf-8").write(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
print(f"Updated {len(out)} stories")
