# ---------------- Helper Functions ----------------
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def clean(t): return ''.join(c for c in t.upper() if c.isalpha())
def num(c): return ord(c) - 65
def ch(n): return chr((n % 26) + 65)

def modinv(a, m=26):      # Modular Inverse
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

# ---------------- 1. Additive Cipher ----------------
def add_enc(t, k): return ''.join(ch(num(c)+k) for c in clean(t))
def add_dec(t, k): return ''.join(ch(num(c)-k) for c in clean(t))

# ---------------- 2. Multiplicative Cipher ----------------
def mul_enc(t, k): return ''.join(ch(num(c)*k) for c in clean(t))
def mul_dec(t, k): return ''.join(ch(num(c)*modinv(k)) for c in clean(t))

# ---------------- 3. Affine Cipher ----------------
def aff_enc(t, a, b): return ''.join(ch(a*num(c)+b) for c in clean(t))
def aff_dec(t, a, b): return ''.join(ch(mod4inv(a)*(num(c)-b)) for c in clean(t))
    
# ---------------- 4. Playfair Cipher ----------------
def pf_table(key):
    key = clean(key).replace('J', 'I')
    key += ''.join(c for c in ALPHA if c!='J' and c not in key)
    return [list(key[i:i+5]) for i in range(0,25,5)]

def pf_pos(tab): return {tab[r][c]:(r,c) for r in range(5) for c in range(5)}

def pf_pair(txt):
    txt=clean(txt).replace('J','I'); p=[]; i=0
    while i<len(txt):
        a=txt[i]; b=txt[i+1] if i+1<len(txt) else 'X'
        if a==b: b='X'; i+=1
        else: i+=2
        p.append((a,b))
    return p

def pf_enc(t,k):
    tab=pf_table(k);pos=pf_pos(tab);out=[]
    for a,b in pf_pair(t):
        r1,c1=pos[a]; r2,c2=pos[b]
        if r1==r2: out+=tab[r1][(c1+1)%5],tab[r2][(c2+1)%5]
        elif c1==c2: out+=tab[(r1+1)%5][c1],tab[(r2+1)%5][c2]
        else: out+=tab[r1][c2],tab[r2][c1]
    return ''.join(out)

def pf_dec(t,k):
    tab=pf_table(k);pos=pf_pos(tab);out=[]
    for i in range(0,len(t),2):
        a,b=t[i],t[i+1];r1,c1=pos[a];r2,c2=pos[b]
        if r1==r2: out+=tab[r1][(c1-1)%5],tab[r2][(c2-1)%5]
        elif c1==c2: out+=tab[(r1-1)%5][c1],tab[(r2-1)%5][c2]
        else: out+=tab[r1][c2],tab[r2][c1]
    return ''.join(out)

# ---------------- 5. Hill Cipher (2x2) ----------------
def det2(m): return (m[0][0]*m[1][1] - m[0][1]*m[1][0]) % 26
def inv2(m):
    d=det2(m);di=modinv(d)
    return [[(m[1][1]*di)%26,(-m[0][1]*di)%26],
            [(-m[1][0]*di)%26,(m[0][0]*di)%26]]

def hill_enc(t,k):
    t=clean(t)
    while len(t)%2: t+='X'
    out=""
    for i in range(0,len(t),2):
        a=num(t[i]);b=num(t[i+1])
        x=(k[0][0]*a+k[0][1]*b)%26
        y=(k[1][0]*a+k[1][1]*b)%26
        out+=ch(x)+ch(y)
    return out

def hill_dec(t,k):
    ik=inv2(k);out=""
    for i in range(0,len(t),2):
        a=num(t[i]);b=num(t[i+1])
        x=(ik[0][0]*a+ik[0][1]*b)%26
        y=(ik[1][0]*a+ik[1][1]*b)%26
        out+=ch(x)+ch(y)
    return out

# ---------------- Main Program ----------------
print("Choose Cipher:\n1.Additive\n2.Multiplicative\n3.Affine\n4.Playfair\n5.Hill")
chc=int(input("Enter choice: "))
text=input("Enter text: ")

if chc==1:
    k=int(input("Enter key: "))
    c=add_enc(text,k);print("Cipher:",c);print("Decrypt:",add_dec(c,k))

elif chc==2:
    k=int(input("Enter key (coprime with 26): "))
    c=mul_enc(text,k);print("Cipher:",c);print("Decrypt:",mul_dec(c,k))

elif chc==3:
    a=int(input("Enter 'a' (coprime with 26): "))
    b=int(input("Enter 'b': "))
    c=aff_enc(text,a,b);print("Cipher:",c);print("Decrypt:",aff_dec(c,a,b))

elif chc==4:
    k=input("Enter key: ")
    c=pf_enc(text,k);print("Cipher:",c);print("Decrypt:",pf_dec(c,k))

elif chc==5:
    print("Enter 2x2 key matrix:")
    k=[[int(input("k11: ")),int(input("k12: "))],[int(input("k21: ")),int(input("k22: "))]]
    c=hill_enc(text,k);print("Cipher:",c);print("Decrypt:",hill_dec(c,k))
else:
    print("Invalid choice!")


print("this is for testing")