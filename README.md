### Skripty k FYKOSímu příjmu řešení a obálkování

`makeprijem.py`

Masterskript, potřebuje `download.py`, `switch.py` a `pdfjoin.py` (a `white.pdf`).
Dělá to samé, jako tyhle tři skripty dohromady, prakticky celý příjem.

Momentálně tedy stačí spustit tento skript*, zbytek popisu jsou spíše doplňující informace.

*pokud chceme oddělit "joined" sobubory pro české a zahraniční řešitele, je potřeba ještě před spuštěním `makeprijem.py` stáhnout z fksdb (export "Submity zahraničních řešitelů") seznam zahraničních submitů a uložit je do souboru `download/rocnik{rocnik}/serie{serie}/submitids.csv` -- zkontroluj, že je soubor oddělen středníky (resp. stačí, ať má jen jeden sloupec s hlavičkou "submit").

`pdfsplit.py`

Natáhne opravené joined soubory z `"/corrected/rocnik{rocnik}/serie{serie}/joined_uloha-{problem}_{file_type}.pdf"`, kde `file_type` je buď "czech" nebo "foreign" (tyhle složky se musí ručně založit a dát tam soubory), na ročník a sérii se zeptá a díky souboru, co vytvořil `pdfjoin.py` je zase rozpojí na jednotlivé řešitele a rozřadí do složek podle úloh pod `"/corrected/..."`

Pokud stejná složka `"/corrected/rocnik{rocnik}/serie{serie}/"` obsahuje i soubor `submits.csv` (csv oddělené ";", kde jeden sloupeček má název "submit" a obsahuje sumbitids) a při spouštění se zadá (user input) že chceme pouze zahraniční řešitele, tak se do složky "upload_me" přesunou pouze ty soubory, jejichž submitids jsou v daném csv.

`upload.py`

checkne, jestli mají řešení správný tvar pro upload, tedy "*__submitid*". Pokud mají, uloží si všechny submitid do souoru a uploadne řešení na server.
Pozn.: aktuálně uploaduje všechno, co je v pdf v localpath, předpokládá, že v localpath jsou jen podsložky "uloha-1". Na serveru nejsou předem vytvořené složky `rocnikRR/serieS`, takže se musí předtím vytvořit. To není úplně ideální řešení, výhledově zkusím vymyslet něco lepšího.

`download.py`

Stáhne řešení do adresářové strukrury `./download/rocnikRR/serieS/uloha-U`

`switch.py`

Stáhnutá řešní jsou pojmenovaná ve formátu "jméno_příjmení..."
přehodí je, aby řešení byla správně abecedně seřazená "přijmení_jméno". U řešitelů, kteří mají 3+ jmen se zeptá na input od uživatele, které je příjmení.
Tato víceslovná jména a pozice přijmení si ukládá. 
Také vytvoří zálohu všech řešení po přehození jmen (pokud už záloha neexistuje).
perlička: "ch" se v systému v angličtině řadí pod "c", takže tento skript nahradí "ch" na začátku jména za "hzz"

`pdfjoin.py`

Stáhnutá řešení spojí do jednoho souboru, resp. osmi — jeden pro každou úlohu — resp. šesnácti (oddělení českých a zahraničních). Tyto soubory jsou `download/rocnik{rocnik}/serie{serie}/joined_uloha-{problem}_{file_type}.pdf`. Pro oddělení zahraničních je potřeba soubor `submitids.csv` -- viz popis u `makeprijem.py`.
Vždycky se stane, že někdo odevzdá řešení ve formátu, které tento skript nezvládne mergnout. Taková řešení skript posbírá a hodí do složky exceptions v podsložce série. 
Ptá se na možnosti: dohromady nebo odděleně. Dohromady nahází všechny exceptions do jedné složky (hodí se pro tisk), odděleně to rozdělí podle úloh (hodí se pro posílání při elektronickém opravování).
Doporučuji do těchto složek pak přidat věci, co prijdou mailem a poštou a všechno to pak mergnout do jednoho souboru (random online convertorem).
Zároveň si skript vytvoří v podsložce série soubor `stranyprorozdeleni_uloha-{problem}.txt`, kam uloží počet stran a pořadí řešitelů v jednotlivých joined souborech, což se celkem hodí na rozdělování (které je potřeba u elektronického odesílání řešení).

`white.pdf`

Tohle potřebuje `pdfjoin` (a tedy i `makeprijem`). Je to prázdná stránka, která se přidává k řešením účastníků, aby měly vždy sudý počet stran (aby byl snadný oboustranný tisk).

