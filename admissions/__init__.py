"""
Srovnání párovacích mechanismů pro přijímačky
---------------------------------------------

Doplňující ukázky a vysvětlení ke srovnání algoritmů pro vyhodnocení
přijímacích zkoušek ze studie [Přijímačky na střední školy: promyšlený mechanismus nebo velká národní loterie?](https://idea.cerge-ei.cz/studies/prijimacky-na-stredni-skoly-promysleny-mechanismus-nebo-velka-narodni-loterie) publikované [Institutem pro demokracii a ekonomickou analýzu](https://idea.cerge-ei.cz/)
(IDEA při CERGE-EI).

Párovací mechanismy zjednodušené představují algoritmy, které přiřazují žáky dle výsledků školních
přijímacích zkoušek k jednotlivým středním školám. Jak ukazují zde uvedené příklady, tento algoritmus
není nepodstatný technický detail, ale přímo ovlivňuje, zdali se žáci dostanou na svoji preferovanou školu
nebo nikoli.

Tři základní vlastnosti, které by mělo výsledné přiřazení splňovat (a podle kterých můžeme posuzovat
párovací mechanismy):

1. **Spravedlnost:** o přijetí rozhoduje především výsledek zkoušky a méně úspěšný žák nikdy nemůže
   předběhnout žáka s lepším výsledkem ve zkoušce. Technický pojem označující tuto vlastnost je
   **stabilita** (nebo také neexistence opodstatněné závisti).
2. **Respektování žákovských preferencí:** pokud žák může být přiřazený na jeho více preferovanou školu,
   aniž by tím došlo k horšímu přiřazení kohokoli jiného, pak by tak mělo být učiněno 
   (například formou výměny dvou žáků, pokud oba chtějí být na škole toho druhého). Technicky se tato
   vlastnost nazývá **Pareto efektivita** z pohledu studentů.
3. **Odolnost vůči strategizování:** zdali žáci jsou motivováni uvádět školy v přihláškách dle
   skutečných preferencí, nebo se jim vyplatí uvést školy v jiném pořadí nebo některé školy
   vynechat.

Tyto tři vlastnosti však nemohou být zcela naplněny zároveň, neboť v některých případech by vzájemné
prohození studentů pro dosažení vyšší efektivity porušilo spravedlivost výsledku (jak ukazuje **příklad
o nedosažitelnosti stability a efektivity**).

Zde prezentujeme několik možných párovacích mechanismů:

- **Původní mechanismus navržený Cermatem**: vede ke spravedlivému výsledku, ale nezaručuje plné
  respektování žákovských preferencí (výsledek by bylo možné dále zlepšit vzájemnou výměnou žáků).
- **Mechanismus odloženého přijetí**: nazývaný také **stabilní mechanismus optimální pro studenty**,
  neboť nejvíce zachovává preference žáků mezi všemi spravedlivými mechanismy.
- **Naivní mechanismus**: představuje prosté překlopení stávajícího průběhu zkoušek do verze s pořadím
  škol. Tento algoritmus by sice nejlépe odpovídal doslovnému znění předložené novely školského
  zákona, avšak nezaručuje spravedlivý výsledek.

Ačkoli právě poslední naivní mechanismus doslovně vychází z [novely školského zákona](https://www.psp.cz/sqw/text/tiskt.sqw?O=9&CT=551&CT1=0)
**§60i Způsob hodnocení výsledků přijímacího řízení** (odst. 2 a 3), za hlavní podstatu
lze však mnohem více považovat právě požadavek **spravedlnosti** 
a **respektování žákovských preferencí**.

- *(2) Pokud splní kritéria přijímacího řízení více uchazečů než kolik lze přijmout,
rozhoduje jejich pořadí podle výsledků hodnocení kritérií přijímacího řízení.*
- *(3) Umístí-li se uchazeč na místě opravňujícím k přijetí do více oborů středního
vzdělání, bude přijat do oboru umístěného z těchto oborů středního vzdělání na
přednostnějším pořadí uvedeném v přihlášce podle § 60b; do ostatních oborů středního
vzdělání nebude uchazeč přijat.*

Poslední mechanismus, **stabilní mechanismus optimální pro školy**, je uvedený pouze jako doplňující,
neboť dosáhne vždy stejného výsledku jako mechanismus představený Cermatem. Tento mechanismus vede
vždy k výsledku, který by byl nejvíce preferovaný pro školy, avšak nikoli pro žáky. Rozdíl mezi takovými
výsledky ilustruje příklad **optimalita pro studenty vs. pro školy**.

Jednotlivé příklady na této stránce názorně ukazují, jak velké rozdíly mezi výsledky mohou být, a stručně
popisují jejich průběh po jednotlivých krocích. Výsledkem všech algoritmů je vždy finální přiřazení
k jednotlivým školám (případně odmítnutí na všech školách a nutnost pokračování do druhého kola.
Odolnost vůči strategizování zde detailně rozebírána není, protože s nízkým počtem vybíraných škol
při přihlašování ji nelze plně dosáhnout.

**[Matematicky bylo dokázáno již v roce 1962](https://www.jstor.org/stable/2312726), že mechanismus odloženého přijetí je pro žáky
nejlepším spravedlivým mechanismem. Dnes je ve světě nejčastěji zaváděným mechanismem pro přijímací
zkoušky na střední školy a [v roce 2012 byla udělena Nobelova cena](https://en.wikipedia.org/wiki/List_of_Nobel_Memorial_Prize_laureates_in_Economic_Sciences) matematiku Lloydu Shapleymu a ekonomovi Alvinu Rothovi
právě za výzkum v této oblasti.**

**Proto by bylo velmi žádoucí, aby v souladu s moderními vědeckými poznatky použila mechanismus
odloženého přijetí pro přijímací zkoušky i Česká republika.** Použití tohoto mechanismu
je stejně snadné jako u kteréhokoli jiného algoritmu a nepředstavuje žádnou dodatečnou zátěž.

2023, Tomáš Protivínský, [tomas.protivinsky@cerge-ei.cz](mailto://tomas.protivinsky@cerge-ei.cz)

<i class="bi bi-github" style="font-size: 200%"></i> Zdrojový kód s ukázkovou implementací těchto mechanismů je k dispozici na [githubu](https://github.com/protivinsky/idea-admissions).
Kód zároveň umožňuje generovat grafické srovnání výsledných přiřazení podle jednotlivých algoritmů v podobě HTML zprávy.
"""


from .domain import AdmissionData, Allocation
from .mechanism import Mechanism
from .deferred_acceptance import DeferredAcceptance
from .cermat_mechanism import CermatMechanism
from .naive_mechanism import NaiveMechanism
from .school_optimal_sm import SchoolOptimalSM
