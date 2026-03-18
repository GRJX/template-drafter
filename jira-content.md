# Release Notes: 3.42.0

### KWM-6060: [Timebox] [3 dagen] Vervolg DAO's omschrijven
*ALS* ontwikkelaar,
*WIL IK* verdergaan met het omschrijven van DAO's naar JPA repositories
*ZODAT* we klaar zijn voor de spring 5 naar 6 update

*Probleem:*
Huidige DAO's worden niet ondersteund in spring 6.

*Oplossing:*
De Dao's omschrijven naar de moderne JPA repositories. 

*Afhankelijkheden:*
 * <teams_of_personen>

*Acceptatiecriteria:*
 * Zoveel mogelijk oude DAO's zijn verwijderd en vervangen door JPA repositories.
 * De testen zijn waar nodig aangepast.
 * Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*
 * Documentatie: <fo_text>
 * <frontend_pagina's_links>
 * <backend_file_links>

---

### KWM-5983:  [Timebox] [3 dagen] Vervolg DAO's omschrijven
*ALS* ontwikkelaar,
*WIL IK* verdergaan met het omschrijven van DAO's naar JPA repositories
*ZODAT* we klaar zijn voor de spring 5 naar 6 update

*Probleem:*
Huidige DAO's worden niet ondersteund in spring 6.

*Oplossing:*
De Dao's omschrijven naar de moderne JPA repositories. 

*Afhankelijkheden:*
 * <teams_of_personen>

*Acceptatiecriteria:*
 * Zoveel mogelijk oude DAO's zijn verwijderd en vervangen door JPA repositories.
 * De testen zijn waar nodig aangepast.
 * Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*
 * Documentatie: <fo_text>
 * <frontend_pagina's_links>
 * <backend_file_links>

---

### KWM-5958: KWM-Coverage in een aparte module
*ALS*  belanghebbende in KWM
*WIL IK* dat ik de coverage in een aparte module komt
*ZODAT* we best practices toepassen qua onderhoudbaarheid en separation of concerns

*Probleem:*
[https://jira.ictu-sd.nl/browse/KWM-5867] , de java testdekking wordt nog geregeld in de reguliere poms met hier een daar een tweak om de boel draaiende te krijgen

*Oplossing:*
De testdekking voor de java code wordt geregeld in een aparte module

*Afhankelijkheden:*
 * <teams_of_personen>

*Acceptatiecriteria:*
 * kwm-coverage module geintroduceerd
 * Coverage is minimaal 56.3 %
 * De KWM-importer fix uit [https://jira.ictu-sd.nl/browse/KWM-5867] zit erin,of beter de KWM-importer testen draaien en zijn zichtbaar in de coverage rapporten
 * Wanneer tijd over, een epic aanmaken voor onze andere repo's om het zo op te lossen
 * <Time-bound>
 * Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*
 * Documentatie: zie [https://gitlab.dictuy.iesprd.ictu-sr.nl/kwm/kwm-portal/-/merge_requests/1044] voor de code en de links in het MR overzicht
 * Zie EAD voor een werkend voorbeeld
 * Lees het woord tweak lichtjes (denk aan jacoco skip etc), het belangrijkste probleem is opgelost in de vorige story. Dat was dat coverage van de laatste java code lezende module niet meegeteld werd als dit de laatste module is. Doordat kwm-docker de laatste module is in de huidige oplossing. Deze komt na alle java modules), is dit probleem verholpen.  

---

### KWM-5949: Verbeter KWM docs release proces
*Als* ontwikkelaar,
*Wil ik* een geautomatiseerd releaseproces en geen gebouwde artifacts in de repo.
*Zodat* het release proces robuust is en de repo schoon.

*Probleem:*
Documentatie wordt nu wel gebouwd door maven, maar de resulterende artifacten (pdfs) moeten handmatig naar een folder worden verplaatst. Oude versies moeten ook handmatig in een archief folder worden geplaatst en worden ingecheckt, terwijl deze versies ook op de release server terecht komen en vanuit de git release tag opnieuw gebouwd kunnen worden indien gewenst.

*Oplossing:*

Dezelfde aanpassing maken als voor de EAD pilot voor gerelateerde ticket [https://jira.ictu-sd.nl/browse/EAD-1137]. Dit houdt in de artifactpaden op eenzelfde manier aan te passen in .gitlab-ci.yml waarbij de lange regel leesbaarder gemaakt wordt door deze naar meerdere regels om te zetten. Daarbij maak ook gebruik van een wat meer overzichtelijker directory structuur.

*Afhankelijkheden:*
 * GEEN

*Acceptatiecriteria:*
 * Documentatie artifacten die vanuit source (bijv asciidoc plain text) gebouwd worden zijn niet meer ingecheckt in de repo
 * Er zijn ook geen archief mappen meer in de repo voor deze documentatie 
 * Deze documentatie artifacten worden nu gebouwd in een target folder (zodat ze met clean worden verwijderd)
 * De versienummers in deze documenten zijn gebaseerd op globale pom properties/variabelen
 * De release pipeline stap plaatst de artifacten met een naam voorzien van versie nummer in de release zip
 * Op deze story is gedocumenteerd welke bestanden zijn verwijderd uit de repo
 * Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/01.Werkwijze-Processen/Scrum#definition-of-done].

*Technische details: (optioneel)*
 * Iets dergelijks werd gedaan in VOS versie 2.1.0. VOS doet dingen anders qua release dat de rest van de repo's. 

---

### KWM-5913:  [Timebox] [5 dagen] Vervolg DAO's omschrijven
*ALS* ontwikkelaar,
*WIL IK* verdergaan met het omschrijven van DAO's naar JPA repositories
*ZODAT* we klaar zijn voor de spring 5 naar 6 update

*Probleem:*
Huidige DAO's worden niet ondersteund in spring 6.

*Oplossing:*
De Dao's omschrijven naar de moderne JPA repositories. 

*Afhankelijkheden:*
 * <teams_of_personen>

*Acceptatiecriteria:*
 * Zoveel mogelijk oude DAO's zijn verwijderd en vervangen door JPA repositories.
 * De testen zijn waar nodig aangepast.
 * Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*
 * Documentatie: <fo_text>
 * <frontend_pagina's_links>
 * <backend_file_links>

---

### KWM-5910: Intrekken van een geaccordeerde batch en FE wijzigingen
ALS (functioneel) beheerder
WIL IK een geaccordeerde batch kunnen in trekken
ZODAT de functionaliteit schaalbaar is en gebruikt kan worden voor alle (342) gemeenten die RvIG als klant heeft

*Probleem:*
Na accordering kan alleen de gehele batch worden ingetrokken. Dit geldt ook voor bestanden die al gedownload zijn. Ingetrokken bestanden worden in de KWM weergegeven als Verwijderd (nieuwe status). Het bestand wordt verwijderd uit de database. Losse bestanden intrekken wordt opgepakt in een aparte story, zie KWM-5606.
Intrekken van een batch op beheerscherm, zie KWM-5904.

*Oplossing:*
Trek op basis van batchnummer de bestanden in. Verwijder of marker deze records.

*Acceptatiecriteria:*
 * Als de batch status geaccordeerd is, en gedownload is door een gemeente heeft moeten alle onderliggende bestanden verwijderd worden. Meta data van de batch blijft bestaan en krijgt status "Verwijderd = ja";
 * Ieder bestand in de batch dat verwijderd wordt krijgt status "Verwijderd = ja" (of afleiden van de batch);
 * Bestanden worden volledig verwijderd uit de database (i.v.m. IB-beleid, geen onnodige data bewaren);
 * De overzichtspagina voor bestanden krijgt een kolom voor de Download status (Gedownload/Niet gedownload) en een Verwijderd status (Ja/Nee);
 * De overzichtspagina krijgt een kolom voor het batchnummer, blijft leeg voor handmatig gedeelde bestanden.
 * De overzichtspagina krijgt een dynamisch filter voor het batchnummer, waarin alleen de batchnummers aangevinkt kunnen worden die aanwezig zijn. En een optie voor handmatig, om alle bestanden zonder batch te laten zien.
 * Alleen een volledige batch kan ingetrokken worden;
 * De gemeente kan de ingetrokken bestanden niet meer downloaden;
 * Story voldoet aan de DoD.
 * *Er komt dus geen apart scherm voor batch bestanden.* 

*Aanvullende info:*

---

### KWM-5908: Batchnummer introduceren
ALS medewerker Beoordelen en Autoriseren van RvIG
WIL IK het beschikbaar stellen van bestanden automatiseren op basis van een batchnummer
ZODAT de functionaliteit schaalbaar is en gebruikt kan worden voor alle (342) gemeenten die RvIG als klant heeft

*Oplossing:*
Inlezen van bestanden die klaar staan voor de verschillende gemeenten gebeurt op batchnummer. Dit batchnummer staat in de bestandsnamen, en is een tijddatumstempel welke is bepaald door de instantie/proces die de bestanden klaarzet. 
Deze batchnummer informatie moet in de db worden opgeslagen zodat er per batch een akkoordatie kan plaatsvinden in het proces. 
Nieuwe tabel moet de velden hebben:
- batchnummer
- datum voorstel
- voorstel gebruiker
- datum geakkoordeerd
- akkoord gebruiker

*Afhankelijkheden:*

*Acceptatiecriteria:*
* maak tabel aan
* db script
* Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*


---

### KWM-5906: Batch moet geaccordeerd worden
ALS medewerker Beoordelen en Autoriseren van RvIG
WIL IK het beschikbaar stellen van bestanden per batch worden geaccordeerd voordat bestanden door gemeenten gedownload kunnen worden.
ZODAT er een controle moment is.

Oplossing:
Geïmporteerde bestanden kunnen aan de hand van het batchnummer worden geaccordeerd voordat deze beschikbaar komen voor de desbetreffende gemeente/gemeenten. 
Batchnummer is de tijddatumstempel uit het bestandsnaam. Op basis van dit batchnummer kunnen de bestanden bij elkaar gehouden worden.
Op basis van dit batchnummer moet een batch geakkoordeerd worden. Zie [http://kwm.portal.latest.kwm-1.dictuy.iesprd.ictu-sr.nl/portal/bpr/beheer/ensiaimport] waar een zelfde functionaliteit is gebouwd. Ipv een vragenlijst is er dan een batchnummer.
Dit scherm op het scherm van [https://jira.ictu-sd.nl/browse/KWM-5904]

Acceptatiecriteria:
 * Op scherm van KWM-5904 scherm [http://kwm.portal.latest.kwm-1.dictuy.iesprd.ictu-sr.nl/portal/bpr/beheer/ensiaimpor] nabouwen.
 * Locatie van deze nieuwe pagina is tab/subpagina op [http://kwm.portal.latest.kwm-1.dictuy.iesprd.ictu-sr.nl/portal/bpr/beheer/bestanddelen/upload]
 * Naam pagina: Accorderen batches
 * Batch kan alleen worden goedgekeurd door een andere gebruiker dan de gebruiker die de batch aanbiedt.
 * Wanneer een batch wordt klaargezet om te worden geaccordeerd moet er een check zijn op de bestandsnamen binnen de batch. Geef foutmelding. Wanneer er een fout is kan de batch niet klaargezet worden. Check op gemeentenummer, batchnummers en REF code.
 * Story voldoet aan de DoD.

Technische details:

---

### KWM-5904: Verplichte velden koppelen aan REFX uit bestandsnaam (nieuw beheerscherm)
ALS medewerker Beoordelen en Autoriseren van RvIG
WIL IK het beschikbaar stellen van bestanden de verplichte velden automatisch worden ingevuld
ZODAT de deze functioneel schaalbaar is

*Probleem:*
Verplichte velden kunnen door de beheerder worden beheerd, op basis van de omschrijving/categorie. Hiervoor moet een aparte pagina komen.
bestandsnaam: 0363_20260102_REFX.xxx
Adhv het REFX gedeelte wordt er bepaald wat de inhoud is van de verplichte velden. 

*Oplossing:*
Maak een beheerpagina waarop de verplichte velden gekoppeld worden aan het REFX gedeelte uit de bestandsnaam. Geef de beheerder de mogelijkheid een REFX te maken, en daaraan de inhoud vd  verplichte te geven. 
Alleen csv bestanden, extentie csv. Pagina is een subpagina (tab) van http://kwm.portal.latest.kwm-1.dictuy.iesprd.ictu-sr.nl/portal/bpr/beheer/bestanddelen/upload (Bewerken verplichte velden), met dezelfde autoristatie.

*Afhankelijkheden:*

*Acceptatiecriteria:*
* Maak een beheer pagina aan. Geef mogelijkheid om een REFX aan te maken en te wijzigen en te verwijderen en voor deze REFX een inhoud te geven voor de verplichte velden (zie tabel voor de verplichte velden: betandsmetadata)
* nieuwe tabellen om deze gegevens te kunnen opslaan
* Maak de db scripts aan voor de nieuwe tabellen.
* Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*


---

### KWM-5902: Importeer bestand vanaf FS tbv "Bestanden delen" 
ALS medewerker Beoordelen en Autoriseren van RvIG
WIL IK het beschikbaar stellen van bestanden automatiseren
ZODAT de functionaliteit schaalbaar is en gebruikt kan worden voor alle (342) gemeenten die RvIG als klant heeft

*Probleem:*
Bestanden op de KWM FS kunnen automatisch worden opgepakt en ingelezen in de database (volgens afgesproken conventie van de bestandsnaam, zie technische details).
bestandsnaam: 363_20260102_REFX.xxx

*Oplossing:*
Interpreteer de bestandsnaam, bepaal adhv hiervan voor welke gemeenten het bestand is bestemd. Gebruik de bestanden delen functionaliteit zoals deze al bestaat. Bepaal de verplichte velden adhv het REFX gedeelte van de bestandsnaam.
Upload bestand naar database, volgens de functionaliteit "Bestanden delen". 
Initiatief ligt bij de beheerder. Dus deze drukt op een knop om het proces te starten. Er is een beheerpagina waarop dit proces gestart kan worden KWM-5904.

*Afhankelijkheden:*

*Acceptatiecriteria:*
 * Interpreteer de bestandsnaam
 * vul de verplichte gegevens in adhv REFX in de bestandsnaam
 * plaats bestand in de database volgens de functionaliteit "Bestanden delen".
 * houd de bestanden bij elkaar op basis van het batchnummer (tijddatumstempel uit de bestandsnaam). Hier zal mogelijkerwijs een extra veld voor moeten worden aangemaakt. Zie KWM-5908 voor de tabel tbv batchnummers
 * De locatie van de bestanden bevinden zich in een subdir. Na het importren de dir verplaatsen naar een dir "Archief". Zoals dat nu ook gebeurt bij BCM.
 * 1 batch per keer.
 * Na accorderen wordt dit proces automatisch gestart
 * Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*

---

### KWM-5898: Update hibernate bytecode provider
*ALS* ontwikkelaar, *WIL IK* de Hibernate bytecode provider migreren van Javassist naar Byte Buddy *ZODAT* we gebruikmaken van de moderne, actief onderhouden standaard.

*Probleem:*

  KWM gebruikt Javassist als Hibernate bytecode provider, terwijl Hibernate sinds versie 5.6 Byte Buddy als default gebruikt. Javassist wordt nauwelijks nog onderhouden.

*Oplossing:*

 Configuratie wijzigen naar Byte Buddy en Javassist dependency verwijderen.

*Afhankelijkheden:*
 * <teams_of_personen>

*Acceptatiecriteria:*
 * hibernate.bytecode.provider=bytebuddy in db.properties
 * javassist dependency en property verwijderd uit pom.xml
 * Alle tests slagen (met name testen met lazy loading/entity relaties)
 * Loop de export-excelsheets na, en vergelijk je branch met de master (staan alle tabs er etc)
 * Story voldoet aan de Dod

*Technische details: (optioneel)*
 * Documentatie: <fo_text>
 * Bestanden: pom.xml, db.properties, ShopPersistenceConfig.java
 * Let op: test specifiek entities met {{{}@OneToMany{}}}, {{@ManyToOne}} en {{FetchType.LAZY}} relaties, omdat de bytecode provider verantwoordelijk is voor het genereren van proxy classes die data pas ophalen wanneer deze daadwerkelijk wordt aangesproken
 *  

---

### KWM-5869: Gemeente markeerverzoeken overzicht omschrijven
*Probleem:*
Zie [http://kwm.portal.latest.kwm-1.dictuy.iesprd.ictu-sr.nl/portal/bpr/monitorgegevens/markeringsverzoek/overzicht|http://kwm.portal.latest.kwm-1.dictuy.iesprd.ictu-sr.nl/portal/bpr/beheer/markeringsverzoek/beoordelen?id=215]

Deze pagina staat is in JSP geschreven. Daarnaast maakt het in de backend gebruik van legacy pagination logica, die het omschrijven van de DAO-backend service vertraagt. Dit kan ook in de frontend.

*Oplossing:*
Deze pagina moet naar react worden omgeschreven.

*Afhankelijkheden:*
 * geen

*Acceptatiecriteria:*
 * Inventariseer/Tune/Pas aan op ART tests (id's hetzelfde laten)
 * Pagina omschrijven naar react
 * Frontend unit test schrijven
 * Backend aanpassen inclusief de testen
 * Pagination in de frontend (er is een beperkte dataset, geverifieerd door Eric Catsburg), zoveel mogelijk legacy criteria eruit 
 * Zoveel mogelijk omschrijven naar SpringJPA
 * Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*
 * geen

---

### KWM-5867: Sonar laat hele coverage zien
*ALS* Team Ypsilon
*WIL IK* dat sonar alle coverage laat zien 
*ZODAT* we duidelijk hebben hoeveel testdekking we hebben

*Probleem:*

In KWM worden de testresultaten geisoleerd per module gemeten, waardoor we een lagere dekking zien dan in de realiteit. De DTO's krijgen een coverage van 0% terwijl ze in andere modules wel gebruikt worden

*Oplossing:*

Holistische testdekking ipv geisoleerde

*Afhankelijkheden:*
 * <teams_of_personen>

*Acceptatiecriteria:*
 * Testdekking is als geheel, en niet per module
 * <Achievable>
 * <Relevant>
 * <Time-bound>
 * Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*
 * Documentatie: <fo_text>
 * In IntelliJ kan je de testdekking laten zien inclusief andere modules
 * <backend_file_links>

---

### KWM-5816: [Timebox] [5 dagen] Vervolg DAO's omschrijven
*ALS* ontwikkelaar,
*WIL IK* verdergaan met het omschrijven van DAO's naar JPA repositories
*ZODAT* we klaar zijn voor de spring 5 naar 6 update

*Probleem:*
Huidige DAO's worden niet ondersteund in spring 6.

*Oplossing:*
De Dao's omschrijven naar de moderne JPA repositories. 

*Afhankelijkheden:*
 * <teams_of_personen>

*Acceptatiecriteria:*
 * Zoveel mogelijk oude DAO's zijn verwijderd en vervangen door JPA repositories.
 * De testen zijn waar nodig aangepast.
 * Story voldoet aan de [DoD|https://gitlab.dictuy.iesprd.ictu-sr.nl/ypsilon/docs/-/wikis/Scrum#definition-of-done].

*Technische details: (optioneel)*
 * Documentatie: <fo_text>
 * <frontend_pagina's_links>
 * <backend_file_links>

---

### KWM-5037: checkstyle op kwm importer module toepassen
*.sp...Huidige situatie*

Kwm importer was een losse gitlab repository waarin checkstyle niet werd toegepast. Sinds story KWM 4929 is kwm importer een submodule in de kwm portal (repository). Bij het samenvoegen is een checkstyle suppression geconfigureerd zodat de importer niet aan de check style regels hoeft te voldoen.

*Gewenste situatie*

De suppression is verwijderd en de importer module voldoet aan dezelfde checkstyle regels als de rest van kwm source code.

*Acceptatie criteria:*
 * De suppression 

{color:#d5b778}<suppress {color}checks{color:#6aab73}=".*" {color}files{color:#6aab73}="kwm-importer[\\/|file:///].*.java"{color}{color:#d5b778}/>{color}voor de importer is verwijderd uit checkstyle-suppressions.xml
 * Alle resulterende checkstyle overtredingen zijn opgelost

 

 

---

