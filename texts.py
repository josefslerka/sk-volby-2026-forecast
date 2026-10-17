"""SK 2026 public site texts (cs)."""

TITLE = "Slovensko 2026: veřejný experiment s AI forecastingem"
LEAD = ("Pravděpodobnostní předpověď 16 slovenských voleb 24. 10. 2026: osm předsedů samosprávných krajů (VÚC) "
        "a osm primátorů krajských měst. Nejdřív čistá AI bez kurzů, vedle ní sázkové kurzy a jejich kombinace. "
        "Po volbách vše vyhodnotíme podle předem zveřejněných pravidel.")

CHANGES_BOX = """<div class="card" style="border-left:4px solid var(--accent)"><h2 style="margin-top:0">Stav k 17. 10. 2026, 21:40</h2>
<ul>
<li><b>Všech 16 předpovědí AI je hotových.</b> Vznikly bez znalosti kurzů a zamkli jsme je ve 20:37. Kurzy jsme četli až potom (Niké, Tipsport, 20:40–21:15).</li>
<li><b>AI a sázky mají stejného favorita v 15 závodech ze 16.</b> Jinak je to jen v <b>Banské Bystrici</b>: AI dává Noskovi 63 %, sázky Javorčíkové 53 %.</li>
<li><b>Velké rozdíly v míře jistoty:</b> v Košicích má AI Lörince na 55 % a Polačka až třetího (19 %), sázky Polačka těsně druhého (39 %). Trnku v Košickém kraji má AI na 66 %, sázky na 51 %. Naopak u Forgáče (Trenčín), Oľhy (Prešov) a Fiabáneho (Žilina) dávají sázky o 12–19 bodů víc než AI.</li>
<li>Hodnotit se bude poslední zamčená předpověď před <b>pátkem 23. 10. 12:00</b>.</li>
</ul>
<p style="margin-bottom:0"><a href="denik.html">Podrobně v deníku →</a> · <a href="pravidla.html">Pravidla →</a></p></div>"""

ABOUT = """<div class="card"><p><b>Co je to za experiment.</b> Zkoušíme, jak dobrým forecasterem může být AI agent. Každou předpověď
vytváří vícekroková AI pipeline (Claude): upřesnění otázky, rešerše, odhad, kontrola, že tvrzení stojí na zdrojích, oponentura
(red-team) a agregace. Všech 16 závodů má stejné zadání. Kandidáty bereme jen z oficiálních seznamů ministerstva vnitra SR.
Člověk pipeline řídí a kontroluje, ale čísla nemění.</p>
<p><b>Proč „bez kurzů“.</b> AI kurzy nevidí. Díky tomu půjde po volbách změřit, jestli přidává informaci, nebo jen opakuje trh.
V 8 závodech ze 16 agent při hledání zahlédl titulek typu „sázkovka favorizuje X“, čísla neviděl. Takové závody označujeme ⚠.</p>
<p><b>Sázky</b> jsou kurzy Niké a Tipsportu po odečtení marže (power de-vig), zprůměrované. Marže jsou tu vysoké, 17–45 %.
<b>AI + sázky</b> je vážený průměr obou v log-odds, stejně jako u <a href="https://josefslerka.github.io/senat-2026-forecast/">Senátu 2026</a>.</p>
<p>Navazuje na experiment <a href="https://josefslerka.github.io/senat-2026-forecast/">Senát 2026</a>.</p></div>"""

RACE_NOTES = {
    "prim-ba": "Bratislava: AI v2 (84 %). Verze 1 měla 92 %, než agent dohledal druhý průzkum.",
    "prim-tt": "Úřadující primátor nekandiduje.",
    "prim-tn": "Úřadující primátor nekandiduje. Žádný průzkum.",
    "prim-za": "Žádný reprezentativní průzkum.",
    "prim-po": "Žádný průzkum.",
}

RULES = """<h1>Pravidla</h1><p class="lead">Zveřejněno před volbami. Předregistrace interně 17. 10. 2026 v 19:20, před prvním odhadem.</p>
<h2>Co předpovídáme</h2><p>Vítěze 16 jednokolových voleb 24. 10. 2026 (zvolen je kandidát s nejvíce platnými hlasy). Každá předpověď je rozdělení
pravděpodobnosti mezi kandidáty, včetně položky „ostatní“. Výsledky bereme od Štatistického úradu SR (volbysr.sk).</p>
<h2>Série</h2><ul>
<li><b>AI</b>: čistá AI pipeline bez sázkových kurzů. Mění se jen při novém faktu (průzkum, odstoupení, podpora), nikdy kvůli pohybu kurzů.</li>
<li><b>Sázky</b>: Niké + Tipsport, power de-vig, průměr knih.</li>
<li><b>AI + sázky</b>: log-odds průměr AI a sázek (ρ = 0,55, stejné jako u Senátu 2026).</li></ul>
<h2>Hodnocená předpověď</h2><p>AI: poslední zamčená verze před pátkem 23. 10. 2026 12:00. Sázky: kurzy přečtené po tomto zámku, nejpozději ve 13:00.
Pozdější kurzy jsou jen reference.</p>
<h2>Metriky</h2><p>Hlavní metrika: Brierovo skóre proti vítězi (součet přes všechny výstupy). Dál logaritmické skóre a trefa favorita.
Výsledky ukážeme pro všech 16 závodů, zvlášť pro kraje a pro města, a jako párová srovnání po závodech. Vzorek je malý,
takže rozdíly budeme formulovat opatrně a vždy s počtem závodů.</p>
<h2>Pořadí každý den</h2><p>Zprávy → případný update AI → zamknutí → teprve potom kurzy.</p>"""

JOURNAL = """<h1>Deník</h1>
<h2>So 17. 10. 2026: den 1</h2>
<h3>Co jsme udělali</h3><ul>
<li>19:20 předregistrace a jednotné zadání pro všech 16 závodů.</li>
<li>Oficiální seznamy kandidátů: <a href="https://www.minv.sk/?samosprava26-info10">ministerstvo vnitra SR</a> (104 kandidátů). Dva kandidáti odstoupili oficiálně (Laššáková v Prešovském kraji, Géci v Košickém kraji), osm podle tisku. Jejich jména zůstávají na lístku, ale hlasy se nepočítají.</li>
<li>Ve čtyřech dávkách proběhlo 16 celých pipeline (rešerše, odhad, kontrola zdrojů, red-team, agregace). Poslední odhad jsme zamkli ve 20:37.</li>
<li>Teprve potom jsme přečetli kurzy: Niké (všech 16), Tipsport (všech 16; dva kraje z tipsport.sk, který má stejnou nabídku).</li></ul>
<h3>Jak se AI a sázky liší</h3><p>Favorit se liší jen v Banské Bystrici (AI Nosko, sázky Javorčíková). Ve zbylých 15 závodech je favorit stejný,
liší se ale míra jistoty. AI je opatrnější u Forgáče, Oľhy, Fiabáneho a Valla, kde sázky dávají o 10–19 bodů víc.
Naopak u Trnky, Lörince a Noska je AI jistější než sázky. Po Senátu, kde AI favority podceňovala, sledujeme hlavně první skupinu.</p>
<h3>Chyby a nápravy</h3><ul>
<li><b>Přehlédnuté průzkumy (2×).</b> V Trnavském kraji rešerše nenašla průzkum AKO pro JOJ 24 (dohledal ho až red-team). V Bratislavě první verze nenašla průzkum SANEP pro Kanál 1. <i>Příčina:</i> každý závod hledal sám. <i>Náprava:</i> společný soubor průzkumů pro všechny závody. Bratislava dostala opravenou verzi 2 (Vallo z 92 na 84 %), stále před zámkem a bez kurzů.</li>
<li><b>Vyčerpaný limit vyhledávání.</b> Od druhé dávky agenti dohledávali přímo přes stránky médií. Chybí hlavně výsledky voleb 2023 a 2024 po městech. U dotčených závodů je to zapsané.</li>
<li><b>Titulky o kurzech.</b> V 8 závodech agent ve výsledcích hledání zahlédl titulek o kurzech, čísla neviděl. <i>Náprava:</i> rozšířený seznam vylučovacích slov. Závody jsou na přehledu označené ⚠.</li>
<li><b>Mylná stopa.</b> Red-team jednoho závodu tvrdil, že existuje nezávislý průzkum s Trnkou na 49 %. Byl to únorový průzkum na objednávku soupeře, předpověď Košického kraje se proto neměnila.</li>
<li><b>Drobné opravy dat:</b> počet rozhodnutých respondentů v nitranském průzkumu AKO (267, ne 317); časy čtení kurzů upřesněné podle commitů.</li></ul>
<h3>Nové zdroje dne</h3><ul>
<li>Seznamy kandidátů: <a href="https://www.minv.sk/?samosprava26-info10">minv.sk</a></li>
<li>Průzkumy AKO pro JOJ 24: <a href="https://joj24.noviny.sk/prieskumy/1271485-viskupic-ma-pred-zupnymi-volbami-vyrazny-naskok-prieskum-ukazal-aj-prekvapenie-na-druhom-mieste">Trnavský</a>,
<a href="https://joj24.noviny.sk/prieskumy/1268562-kto-bude-zupanom-trencianskeho-kraja-takmer-stvrtina-opytanych-este-nevie-komu-da-hlas">Trenčiansky</a>,
<a href="https://joj24.noviny.sk/prieskumy/1269439-najmladsi-by-volili-inak-volebny-model-v-nitrianskom-kraji-priniesol-zaujimave-rozdiely">Nitriansky</a>,
<a href="https://joj24.noviny.sk/prieskumy/1265252-volebny-prieskum-joj-24-v-zilinskom-kraji-jedno-meno-ziskalo-takmer-polovicu-volicov">Žilinský</a>,
<a href="https://joj24.noviny.sk/prieskumy/1266317-kde-ma-lunter-najsilnejsiu-podporu-a-kde-suja-prieskum-joj-24-odhalil-velke-rozdiely-medzi-okresmi">Banskobystrický</a>,
<a href="https://joj24.noviny.sk/prieskumy/1272728-majersky-alebo-mazurek-prieskum-joj-24-ukazal-koho-by-volili-ludia-v-presovskom-kraji">Prešovský kraj</a></li>
<li>Bratislava: <a href="https://kanal1.sk/exkluzivny-prieskum-pre-kanal1-kto-by-sa-stal-primatorom-bratislavy-a-kto-by-viedol-bratislavsky-kraj-keby-sa-volby-konali-dnes">SANEP / Kanál 1</a>,
<a href="https://sita.sk/vallo-ma-pred-razom-naskok-prieskum-tiez-ukazal-akou-znamkou-by-bratislavcania-ohodnotili-jeho-doterajsiu-pracu/">Ixactly / Markíza (SITA)</a></li>
<li>Košice: <a href="https://www.kosiceonline.sk/prieskum-ipsosu-pre-radio-kosice-volebny-model-pre-volby-primatora-kosic-vedie-ladislav-lorinc">Ipsos / Rádio Košice</a></li>
<li>Banská Bystrica: <a href="https://bbonline.sk/prieskum-ako-pre-bbonline-sk-volby-primatora-banskej-bystrice-prinesu-tesny-suboj-jana-noska-a-diany-javorcikovej/">AKO / BBonline</a>,
<a href="https://www.bystricoviny.sk/spravy/v-predvolebnom-prieskume-bbonline-figuroavla-nerealna-vekova-vzorka-volicov-co-zasadne-skreslilo-vysledky/">kritika vzorku (Bystricoviny)</a>,
<a href="https://www.ta3.com/clanok/1051497/preco-kosice-nema-iste-nikto-a-obhaji-vallo-prieskum-pre-ta3-ukazal-favoritov-komunalok-dva-kraje-a-hlavne-mesta">SANEP / TA3</a></li>
<li>Trnava: <a href="https://www.trnavskyhlas.sk/c/42873-nemcovska-alebo-baros-prieskum-naznacil-jasnych-favoritov-volieb-v-trnave/">průzkum Trnavské univerzity</a>,
<a href="https://www.trnavskyhlas.sk/c/42851-zmena-v-trnave-lubica-horvathova-odstupuje-z-volieb,-podporuje-evu-nemcovsku/">odstoupení Horváthové</a></li>
<li>Odstoupení: <a href="https://www.zilinak.sk/clanky/43457/video-anna-belousova-zamiesala-karty-v-boji-o-zilinsku-zupu-vzdala-sa-kandidatury">Belousovová (Žilinský kraj)</a>,
<a href="https://www.presovak.sk/clanky/15758/dalsi-kandidat-odstupuje-z-volieb-na-presovskeho-zupana">Prešovský kraj</a></li></ul>
<h3>Další kroky</h3><p>Každý den projdeme zprávy (nové průzkumy, odstoupení do 22. 10. 7:00) a pak přečteme kurzy. V pátek 23. 10. ve 12:00 je freeze.</p>"""
