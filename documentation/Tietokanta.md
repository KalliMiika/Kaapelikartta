# Tietokohteet tarkemmin

<dl>
	<dt>
		Risteyskoje (Controller)
	</dt>
	<dd>
		Risteyskoje on sellainen harmaa kaappi minkä voi huomata risteyksissä missä on liikennevalot. Tässä tietokannassa 
    risteyskojeesta tallennetaan vain sen nimi ja koordinaatit joiden perusteella se voidaan asettaa karttanäkymään about siihen
    missä se sijaitsee todellisuudessa.
	</dd>
	<dt>
		Kaapeli (Cable)
	</dt>
	<dd>
		Risteyskojeet ovat yhteydessä toisiinsa kaapeleiden välityksellä. Risteyskojeeseen voi tulla useampi kaapeli, mutta Kaapelin
    molemmissa päissä on aina, poikkeuksetta yksi risteyskoje (eli 2 / kaapeli koska molemmissa päissä on yksi).
    Kaapeihin tallennetaan niiden risteyskojeiden id:t (Controller_a_id ja Controller_b_id) joihin se on yhteydessä, ja kaapelin nimi
    ja tyyppi.
	</dd>
	<dt>
		Säie (Thread)
	</dt>
	<dd>
    Kaapeleiden sisällä kulkee säikeitä joiden lukumäärä riippuu kaapelin tyypistä (vaihtelee 20-600 välillä). Säikeet ovat aika eksoottinen
    tietotyyppi tässä tietokannassa, mutta niiden eksoottisuus vastaa todellisuutta. Kaapeli kulkee kahden risteyskojeen välillä, luonnollisesti
    säie joka kulkee kyseisen kaapelin sisällä kulkee myös näiden kojeiden välillä. Säikeet on numeroitu kaapelin sisällä, ja säikeet liitetään
    risteyskojeen sisällä olevaan liitintauluun, joiden liittimet ovat myös numeroitu. Lähtökohtaisesti säie on liitetty saman numeroiseen
    liittimeen, kuin mikä säikeen numero on, ja säikeellä on sama numero kaapelin molemmissa päissä, mutta molempiin tapauksiin löytyy poikkeuksia,
    jonka takia eksoottinen tietorakenne. Esimerkkitilanne: Raksamies x vetää kaivurilla kaapelin poikki, mutta ei hätää, äkkiähän nuo säikeet juottaa
    yhteen, paitsi että nyt ku säie alkaa risteyskojeesta x numerona 5, niin se päättyy risteyskojeessa y numerona 428. hyvin juotettu.
	</dd>
  <dd>
    Säikeen numero a (number_a) viittaa siihen numeroon, mikä säikeellä on kaapelin risteyskojeen A (controller_a_id) päässä.
    Säikeen numero b (number_b) viittaa siihen numeroon, mikä säikeellä on kaapelin risteyskojeen B (controller_b_id) päässä.
    Säikeen liitin a (socket_a) viittaa sen liittimen numeroon, johon säie on liitetty risteyskojeen A (controller_a_id) päässä.
    Säikeen liitin b (socket_b) viittaa sen liittimen numeroon, johon säie on liitetty risteyskojeen B (controller_b_id) päässä.
    Data kenttä sisältää tiedon siitä, että mitä informaatiota kyseisen säikeen sisällä kulkee.
  </dd>
	<dt>
		Ristikytkentä (Cross-connection)
	</dt>
  <dd>
    Ristikytkentä tietorakennetta käytetään kolmeen eri tarkoitukseen. Aioin alunperin tehdä 2 eri taulua, mutta yhdellä taululla voi todella
    näppärästi saada esitettyä kaikki 3 eri tilannetta.
    Säikeet voidaan liittää risteyskojeen sisällä 4 eri tapaa. Joko säie tulee kaapelista ja päätyy kaappiin, tai lähtee kaapin laitteesta ja 
    menee kaapeliin (tavallaan sama tilanne, erona käytännössä että onko säie input vai output), säie saatetaan ristikytkeä suoraan kaapelista A
    johonkin kaapelin B säikeeseen, tai säiettä ei välttämättä kytketä mihinkään vaan se päättyy johonkin risteyskojeen liittimeen.
  </dd>
  <dd>
    Controller_id viittaa siihen risteyskojeeseen, jossa kytkentä tapahtuu
    thread_a_id viittaa toiseen säikeeseen (ei tule sekoittaa säikeen ja kaapelin a ja b merkkauksiin)
    thread_b_id viittaa toiseen säikeeseen (ei tule sekoittaa säikeen ja kaapelin a ja b merkkauksiin)
    käytännössä, kun halutaan selvittää että miten thread_a_id on esimerkiksi liitetty risteyskojeeseen, niin se selvitetään tutkimalla
    säikeen a kaapelin (cable_id) risteyskojeita, joista voidaan päätellä, että kumpi pää kaapelista on kiinni ristikytkentään
    liittyvässä risteyskojeessa, jonka kautta tiedetään, että kiinnostaako meitä säikeen socket_a vai socket_b.
    device_a viittaa siihen risteyskojeen sisällä olevaan laitteeseen, johon säie a (thread_a_id) on kytketty.
    device_b viittaa siihen risteyskojeen sisällä olevaan laitteeseen, johon säie b (thread_b_id) on kytketty.
  </dd>
  <dd>
    Ristikytkentä taululla voidaan siis mallintaa kaikkia yllä olevia tilanteita. Jos säie päättyy risteyskojeen liitintauluun, niin sille ei ole 
    ristikytkentä riviä lainkaan. Jos säie on ristikytketty suoraan kaapelista A kaapeliin B, niin laite kentät ovat tyhjät, jos säie_a ja device_a
    kentillä on arvot ja vastaavilla b kentillä ei, tarkoittaa se sitä, että säie a tulee kaapelista x ja päättyy laitteeseen device_a, säikeille jotka
    alkavat risteyskojeen laitteesta ja jatkavat kaapeliin, merkitään a kentät tyhjiksi ja täytetään b kentät. Jotkin ohjausreitit tulevat
    kaapelista X, liittyvät laitteeseen a, ja poistuvat saman laitteen eri portista kaapeliin Y, näissä tapauksissa kaikki kentät täytetään.
  </dd>
</dl>
