# CSSToTheRescue

## Dag 0
Ik heb vandaag geleerd hoe ik gebruik kan maken van de systeem appearance mode en mijn websites daarmee kan aanpassen, dus als een gebruiker zijn telefoon in dark mode heeft is de website ook in dark mode. Verder heb ik gewerkt met clip-path: circle / polygon / path. 

## Dag 1
Vandaag hadden we de introductie presentatie waar ik clip-path, color-scheme en accent-color. De presentatie ging redelijk en het eindresultaat van de website was wel grappig, maar verder ook niet.

Vandaag kregen we ook een introductie van de eindopdracht, die gaat verlopen als het volgende:

## Dag 3

## Dag 4

## Dag 5
Vandaag ben ik thuis gebleven, maar heb wel behoorlijke progressie geboekt ik had in de bus een brilliant idee hoe ik het probleem van meerdere onderdelen in verschillende animaties kon omzeilen. Ik had als idee om na elke animatie de kubus ontzichbaar gemaakt en de volgende state zichtbaar te maken en niet met opacity maar met diplay. Hierdoor kan ik per kubus bedenken hoe ik deze wil laten draaien. Elke state is dan ook zelf custom gemaakt op basis van de eind patroon van de vorige state. Vandaag heb ik dit gedaan voor 4 states tot een oplossing maar nog zonder animaties.

## Dag 6
Vandaag heb ik verder gewerkt aan meerdere states (moves) te maken heb nu 9 states, ik heb er vandaag dus 5 bij gemaakt verder heb ik alle horizontale turns werkend gekregen en een paar andere kleine dingen. En heb ik geconceptualiseerd op hoe ik mijn blog wil maken en ben hier opgekomen:
![alt text](/img/image.png)

## Dag 7
TODO:
* Verticale turns maken
* UI ontwerpen![alt text](/img/image-1.png)
* UI maken

Wat heb ik vandaag gedaan?
Presentatie en veel geleerd van waar andere mensen aan hadden gewerkt en dan vooral de scroll animatie en :has en concept begonnen.

Hoelang duurde het?
De hele dag dat ik les had

Wat ga morgen doen?
Concept uitgewerkt hebben

Peter-Paul Koch | Browser & support detection
Html = Structuur
Css = Styling
Js = in theorie geen onderwerp in het web, maar in praktijk wel doordat de code in de Js engine.

Js engine voor de taal die bij de DOM moet kunnen gebruiken en bij node wordt Js echt als programmeertaal gebruikt.

Accesability object model = AOM die reageert op op de accesibilty featrues bijvoorbeel arial-

Parser = een stukje programma die een string mee neemt, lees dus de text en zet dit om die het web gebruikt. Dit heb je voor HTML, CSS en JS.

Layout zorgt ervoor dat de web snapt wat hij moet laten zien.

Maak gebruik van query containers om de layout niet te vaak te laten veranderen.

Rendering engine is het centrale systeem van de browser het is alles minus de interface en javascript engine, AOM en DOM, voorbeeld blink.

Js engine is apart, omdat uit de geschiedenis de gedachte was dat er de js engine verwisseld kan worden.

Core vs DOM = Js core is wat js een programmeertaal maakt en zit in een jS rendering engine, DOM is hoe je objecten in de html wijzigen etc. 

Render blocking is het wachten met de html omdat je wacht op css of js

do it now
<script src>

do it later
<script defer src>

I dont care when you do it, just not now
<script async src>

Backward compatibility
Als het ooit ondersteund is door de browser, moet het voor altijd ondersteund worden.


Haal doctype maar eens weg dan krijg je explorer 6.


[form object].elements
<body bgcolor="...">

<frameset> , <iframe> komt uit frameset

Korte geschiedenis
transport ... protocol = vooral voor foutcontrole, UDP doet geen foutcontrole

Mosaic 1993 > Netscape 1994 was hetzelfde als mosaic maar dan commercieel. > Internet Explorer 1995 en die was gratis > Opera 1995 was toen beter in CSS, maar waren niet helemaal cijfer en was betaald > IE 5 Mac 2000 > Konqueror werd later Safari> Safari 2003 heeft als rendering engine webkit > Firefox 2004 is een soort opvolger netscape 4 > Safari IOS 2007 eerst mobiel ecosysteem > Chrome 2008 apple wilde niks toevoegen aan webkit en was google hun eigen rendering engine gestart, wat blink was > Flow 2020 heeft een eigen rendering engine > ladybird 2024 > Igalia spaans opensource bedrijf, heeft grid bedacht, zijn geen browser maken maar heeft er wel veel verstand van. 

worldwideweb.cern.ch laat de eerste website zien