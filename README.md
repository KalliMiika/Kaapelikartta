# Kaapelikartta

<dl>
	<dd>
		Kaapelikartta -sovelluksen tavoite on ylläpitää tietokantaa Helsingin Kaupungin
		Liikennevalojenohjauksen verkosta ja tarjota helppokäyttöinen graafinen
		käyttöliittymä tietokannassa olevan datan selaamiseen.
		Käytännössä siis ylläpidetään tietoa Liikennevalojenohjauskojeista ja niiden sijainneista.
		Kojeiden välillä menevistä Kaapeleista ja kaapeleiden sisällä olevien säikeiden datasta.
		Tavoite olisi luoda jonkinnäköinen karttanäkymä johon kojeet ja kaapelit voitaisiin piirtää
		ja näitä klikkaamalla saataisiin esille tarkempaa tietoa.
		Ohjelman käyttäminen tulee vaatimaan kirjautumisen ja kaikki muutokset logataan ja niihin
		liitetään käyttäjän nimi ja päivämäärä.
	</dd>
</dl>
	
***

### Käyttöohje: (Vain tähän mennessä toteutetuille toiminnallisuuksille)

<dl>
	<dt>
		Ohjausreittien katselmointi
	</dt>
	<dd>
		Ohjausreitit listataan yläpalkin "List routes" linkin kautta. Tietyn reitin tarkempi katselmointi tapahtuu
		edellä mainitun listauksen yhteydessä olevista view-nappuloista.
	</dd>
	<dt>
		Ohjausreittien lisäys
	</dt>
	<dd>
		Ohjausreitit "lisätään" epäsuorasti. Käyttäjä voi merkata säikeiden data kenttään mitä informaatiota säikeen sisällä
		kulkee, jonka perusteella selvitetään että mitä reittiä kyseinen informaatio kulkee kaapelikartassa, mitä kaapeleita
		pitkin ja minkä risteyskojeiden kautta.
	</dd>
	<dt>
		Tietokohteiden katselmointi
	</dt>
	<dd>
		Risteyskojeiden ja Kaapeleiden listaukseen löytyy linkit yläpalkista. Yksittäisiä kaapeleita pääsee katselemaan
		kaapelien listauksesta löytyvien view-nappuloiden kautta. Säikeet listataan kaapelikohtaisesti yksittäisen kaapelin 
		katselmoinnin yhteydessä.
	</dd>
	<dt>
		Tietokohteiden lisäys
	</dt>
	<dd>
		Risteyskojeiden (Controller) ja Kaapeleiden (Cable) listauksien takaa löytyy
		linkit kojeiden ja kaapeleiden lisäys lomakkeisiin.
		Risteyskojeille annetaan nimi ja x- ja y- koordinaatit.
	</dd>	
	<dd>
		Kaapeleille annetaan nimi, alku- ja loppupäässä olevat risteyskojeet
		sekä kaapelin tyyppi, joka määrittää sisällä kulkevien säikeiden lukumäärän.
		Säikeet luodaan automaattisesti kaapelin luonnin yhteydessä, määrä riippuu
		kaapelin tyypistä.
	</dd>	
	<dt>
		Tietokohteiden muokkaus
	</dt>
	<dd>
		Risteyskojeiden muokkaus tapahtuu niiden listauksesta löytyvän Edit-nappulan kautta.
		Kaikkia risteyskojeille asetettuja arvoja voidaan muokata jälkikäteen.
	</dd>
	<dd>
		Kaapeleiden muokkaus tapahtuu niiden listauksesta löytyvän Edit-nappulan kautta.
		Kaikkia muita kaapelille asetettuja arvoja voidaan muokata jälkikäteen paitsi kaapelin
		tyyppiä.
	</dd>
	<dd>
		Säiden muokkaus tapahtuu kaapelikohtaisesti. Tietyn kaapelin säikeitä pääsee muokkaamaan
		menemällä kaapelien listaukseen ja painamalla view-nappia oikean kaapelin kohalta.
		Seuraavasta kaapeli näkymästä voi sitten valita haluamasta säikeen ja avata muokkauslomakkeen
		painamalla Edit-nappia. Kaikkia säikeiden arvoja paitsi sitä kaapelia minkä sisällä se menee
		voidaan muokata jälkikäteen.
	</dd>
</dl>

### Toimintoja:

<dl>
	<dt>
		- Kirjautuminen
	</dt>
	<dt>
		- Risteyskojeiden lisäys, muokkaus ja poisto
	</dt>
	<dt>
		- Kaapeleiden lisäys, muokkaus ja poisto
	</dt>
	<dd>
		(Ajatus olisi että kaapelia luodessa määritetään sen sisällä kulkevien
		säikeiden lukumäärä, jotai ei voida muokata enään jälkikäteen ja tämän
		lukumäärän pohjalta luotaisiin sopiva määrä uusia säikeitä)
	</dd>
	<dt>
		- Säikeiden muokkaus (Ei manuaalista lisäystä tai poistoa)
	</dt>
	<dt>
		- Risteyskeiden katselu
	</dt>
	<dd>
		(Näyttää että mihin kaapelista A tulevat säikeet on kytketty Risteyskojeen sisällä,
		ja mihin säikeeseen ne jatkavat kaapelissa B poistuessaan kaapista.)
	</dd>
	<dt>
		- Kaapeleiden katselu
	</dt>
	<dd>
		(Näyttää kaikki kaapelin sisällä kulkevat säikeet, ja mitä dataa niiden on tarkoitus
		kuljettaa)
	</dd>
	<dt>
		- Tietyn reitin katselu (säikeiden "data" kenttä)
	</dt>
	<dd>
		(Hakusanalla voidaan näyttää tietty ohjausreitti, mistä data lähtee, minkä risteyskojeiden
		kautta se kulkee ja mitä kaapeleita pitkin ja missä säikeessä se kulkee minkäkin kaapelin
		sisällä)
	</dd>
	<dt>
		- Muutoslogin katselu
	</dt>
</dl>
	
***
	
## Linkkejä

<dl>
	<dt>HEROKU</dt>
</dl>

#### [Linkki herokuun](https://kaapelikartta.herokuapp.com/)
	Testitunnukset: 
		Käyttäjänimi: testi1
		Salasana: testi2
<dl>
	<dt>Omalle koneelle</dt>
</dl>

* [Asennusohjeet](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/asennusohje.md)

<dl>
	<dt>Tietokanta</dt>
</dl>	

* [Tietorakenteet sanallisesti](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/Tietokanta.md)
* [Tietokantakaavio](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Tietokantakaavio.jpg)
* [Tietokantakaavio ilman muutoslogia](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Tietokantakaavio2.jpg)
* [Create Table -Lauseet](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/CreateTableLauseet.txt)

<dl>
	<dt>User Stories</dt>
</dl>

* [Kaapelikartta](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/Kaapelikartta.md)
* [Risteyskoje](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/Controller.md)
* [Kaapeli](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/Cable.md)
* [Säie](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/Thread.md)
* [Ristikytkentä](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/Cross-connection.md)
* [Käyttäjät](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/Users.md)
* [Muutoslogi](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/Changelog.md)

<dl>
	<dt>Misc</dt>
</dl>

* [TODO-Lista](https://github.com/KalliMiika/Kaapelikartta/blob/master/documentation/todo.md)

<dl>
	<dt>Kaapelikartta -sovelluksen elementtejä havainnollistavia paint piirroksia</dt>
</dl>

 * [Kaapeli](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Cable.png)
 * [Säie](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Thread.png)
 * [Ristikytkentä](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Cross-connection.png)
