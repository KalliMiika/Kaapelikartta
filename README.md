Linkki herokuun: https://kaapelikartta.herokuapp.com/

Kaapelikartta -sovelluksen tavoite on ylläpitää tietokantaa Helsingin Kaupungin
Liikennevalojenohjauksen verkosta ja tarjota helppokäyttöinen graafinen
käyttöliittymä tietokannassa olevan datan selaamiseen.
Käytännössä siis ylläpidetään tietoa Liikennevalojenohjauskojuista ja niiden sijainneista.
Kojujen välillä menevistä Kaapeleista ja kaapeleiden sisällä olevien säikeiden datasta.
Tavoite olisi luoda jonkinnäköinen karttanäkymä johon kojut ja kaapelit voitaisiin piirtää
ja näitä klikkaamalla saataisiin esille tarkempaa tietoa.
Ohjelman käyttäminen tulee vaatimaan kirjautumisen ja kaikki muutokset logataan ja niihin
liitetään käyttäjän nimi ja päivämäärä.
	
Toimintoja:

	Kirjautuminen
	Risteyskojujen lisäys, muokkaus ja poisto
	Kaapeleiden lisäys, muokkaus ja poisto
		(Ajatus olisi että kaapelia luodessa määritetään sen sisällä kulkevien
		säikeiden lukumäärä, jotai ei voida muokata enään jälkikäteen ja tämän
		lukumäärän pohjalta luotaisiin sopiva määrä uusia säikeitä)
	Säikeiden muokkaus (Ei manuaalista lisäystä tai poistoa)
	Risteyskojujen katselu
		(Näyttää että mihin kaapelista A tulevat säikeet on kytketty kaapin sisällä,
		ja mihin säikeeseen ne jatkavat kaapelissa B poistuessaan kaapista.)
	Kaapeleiden katselu
		(Näyttää kaikki kaapelin sisällä kulkevat säikeet, ja mitä dataa niiden on tarkoitus
		kuljettaa)
	Tietyn reitin katselu (säikeiden "data" kenttä)
		(Hakusanalla voidaan näyttää tietty ohjausreitti, mistä data lähtee, minkä risteyskojujen
		kautta se kulkee ja mitä kaapeleita pitkin ja missä säikeessä se kulkee minkäkin kaapelin
		sisällä)
	Muutoslogin katselu

Linkkejä:
	Tietokantakaavio: https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/Dokumentaatio/Tietokantakaavio.jpg
	Kaapelikartta sovelluksen elementtejä havainnollistavia paint piirroksia:
		Kaapeli: https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/Dokumentaatio/Kaapeli.png
		Säie: https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/Dokumentaatio/S%C3%A4ie.png
		Ristikytkentä: https://raw.githubusercontent.com/KalliMiika/Kaapelikartta/master/Dokumentaatio/Ristikytkent%C3%A4.png
