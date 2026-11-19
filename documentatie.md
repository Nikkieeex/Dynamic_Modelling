#### Overzicht (delete later)

workshops die wij moeten verwerken in project:

- differentiaalvergelijkingen
- ODE-solvers
- niet-lineaire regressie methoden
- modelvergelijking met AIC en BIC criteria


Trellobord:
- workshops uitwerken
- Muis 34 en 43 hebben op dag 11 een volume van 0, dit moet eruit 
  
#### Achtergrond
[Tumor growth kinetics of human LM2-4LUC+ triple negative breast carcinoma cells](https://zenodo.org/records/3574531) 
Ik heb hier de dataset gebruikt van; Vaghi C, Rodallec A, Fanciullino R, Ciccolini J, Mochel JP, et al. (2020) Population modeling of 
tumor growth curves and the reduced Gompertz model improve prediction of the age of experimental tumors, PLoS Comput Biol, 16, p. e1007178. https://doi.org/10.1371/journal.pcbi.1007178
Het bestaat uit 66 muizen (ID 0 tot en met 65), met per muis tussen de 5 en 15 metingen.

LM2-4 is een menselijke borstkankercellijn die sterk uitzaait. De lijn is afgeleid van MDA-MB-231, een triple-negatieve borstkankerlijn. Triple-negatief betekent dat de cellen geen oestrogeenreceptor, geen progesteronreceptor en geen HER2 hebben. Dit type borstkanker is agressief en reageert niet op hormoontherapie of anti-HER2-medicijnen. LM2-4 is geselecteerd op het vermogen om vanuit de borsttumor spontaan uit te zaaien, net als bij mensen. Daardoor is het een model voor gevorderde, uitgezaaide borstkanker. De toevoeging LUC+ betekent dat de cellen het enzym luciferase maken, waardoor tumoren licht geven en in een levende muis te volgen zijn.

#### Differentiaalvergelijking

#### ODE-Solvers

Een differentiaalvergelijking zegt alleen hoe snel het volume verandert. Een solver rekent daaruit stap voor stap de hele curve V(t) uit.

Euler berekent per stap één helling aan het begin van de stap. Runge-Kutta
(RK4) berekent per stap vier hellingen en neemt daar een gewogen gemiddelde
van, waardoor het veel nauwkeuriger is.
Beide solvers zijn getest met exponentiële groei (c = 0,08) op muis 0. RK4
had met een stapgrootte van 1 dag een eindfout van 0,000353 mm³. Euler bleef
met een stapgrootte van 0,1 dag zichtbaar onder de exacte oplossing.

Het rekenwerk is dus goed, maar het exponentiële model beschrijft de groei
verkeerd. Daarom moeten andere modellen worden geprobeerd die de groei wel kunnen laten afremmen.

#### Optimalisatie 

Ik de code van workshop 3 van Brightspace gebruiken en aanpassen aan ons tumormodel. 

Ik koppel mijn eigen Runge-Kutta solver aan een MSE-functie, die berekent hoe ver de modelcurve van de metingen van muis 33 afligt. Daarna laat ik de zoekmethodes uit de workshop (random search en direct search) zelf de waarden voor alpha en beta zoeken waarbij de MSE het laagst is. Als startwaarden gebruik ik de waarden uit workshop 1, omdat die al redelijk in de buurt lijken te zitten.

Met de startwaarden uit workshop 1 is de MSE 7061. Random search en direct search vinden bijna dezelfde waarden, namelijk alpha ≈ 1.23 en beta ≈ 0.042, allebei met een MSE van 5600. Daardoor ligt de oranje lijn precies onder de groene lijn. De startwaarden uit workshop 1 zaten dus in de buurt, maar de zoekmethodes vinden een betere fit. De nieuwe curve volgt vooral het begin en het eind van de metingen beter. De punten rond dag 20 en dag 26 liggen duidelijk naast de curve.