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

#### [Linkki herokuun](https://kaapelikartta.herokuapp.com/)
	Testitunnukset: 
		Käyttäjänimi: testi1
		Salasana: testi2

* [Tietokantakaavio](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Tietokantakaavio.jpg)
* [Tietokantakaavio ilman muutoslogia](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Tietokantakaavio2.jpg)

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
	<dt>Kaapelikartta -sovelluksen elementtejä havainnollistavia paint piirroksia</dt>
</dl>

 * [Kaapeli](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Cable.png)
 * [Säie](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Thread.png)
 * [Ristikytkentä](https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/documentation/Cross-connection.png)
