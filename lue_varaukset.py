#Käytän koodissa sanakirjoja dict, se on helpompi ymmärtää koodissa, koska kaikki
#indeksi viittaulset on korvattu avainsanoilla jotka ovat selkeämpiä.
from datetime import datetime

# Muuntaa varausrivin listasta sanakirjaksi
def muunna_varaustiedot(rivi: list) -> dict:
    jono = [item.strip() for item in rivi]

    varaus_id = int(jono[0])
    nimi = jono[1]
    sahkoposti = jono[2]
    puhelin = jono[3]
    varauksen_pvm = datetime.strptime(jono[4], "%Y-%m-%d").date()
    varauksen_klo = datetime.strptime(jono[5], "%H:%M").time()
    varauksen_kesto = int(jono[6])
    hinta = float(jono[7])
    varaus_vahvistettu = (jono[8] == "True")
    varattu_tila = jono[9]
    varaus_luotu = datetime.strptime(jono[10], "%Y-%m-%d %H:%M:%S")

    # Palautetaan sanakirja
    return {
        "varausId": varaus_id,
        "nimi": nimi,
        "sähköposti": sahkoposti,
        "puhelin": puhelin,
        "varauksenPvm": varauksen_pvm,
        "varauksenKlo": varauksen_klo,
        "varauksenKesto": varauksen_kesto,
        "hinta": hinta,
        "varausVahvistettu": varaus_vahvistettu,
        "varattuTila": varattu_tila,
        "varausLuotu": varaus_luotu,
    }

# Lukee varaukset tiedostosta
def hae_varaukset(varaustiedosto: str) -> list:
    varaukset = []
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset


# Pääohjelma
def main():
    varausdata = hae_varaukset("varaukset.txt")
    # Tulostetaan vahvistetut varaukset
    print("1) Vahvistetut varaukset")
    for merkinta in varausdata:
        if merkinta["varausVahvistettu"] is True:
            print(
                f'- {merkinta["nimi"]}, {merkinta["varattuTila"]}, '
                f'{merkinta["varauksenPvm"].strftime("%d.%m.%Y")}, '
                f'klo {merkinta["varauksenKlo"].strftime("%H.%M")}'
            )
    print()
    # Tulostetaan pitkät varaukset
    print("2) Pitkät varaukset (> 3 h)")
    for merkinta in varausdata:
        if merkinta["varauksenKesto"] >= 3:
            print(
                f'- {merkinta["nimi"]}, '
                f'{merkinta["varauksenPvm"].strftime("%d.%m.%Y")} klo {merkinta["varauksenKlo"].strftime("%H.%M")}'
                f' kesto {merkinta["varauksenKesto"]} h, {merkinta["varattuTila"]}'
            )
    print()
    # Tulostetaan varausten vahvistusstatus
    print("3) Varausten vahvistusstatus")
    for merkinta in varausdata:
        if merkinta["varausVahvistettu"]:
            print(f'{merkinta["nimi"]} -> Vahvistettu')
        else:
            print(f'{merkinta["nimi"]} -> Ei vahvistettu')
    print()
    # Tulostetaan yhteenveto vahvistuksista
    print("4) Yhteenveto Vahvistuksista")
    tunnistetut = 0
    tunnistamattomat = 0

    for merkinta in varausdata:
        if merkinta["varausVahvistettu"]:
            tunnistetut += 1
        else:
            tunnistamattomat += 1

    print(f'- Vahvistettuja varauksia: {tunnistetut} kpl')
    print(f'- Ei-vahvistettuja varauksia: {tunnistamattomat} kpl')
    print()
    # Tulostetaan vahvistettujen varausten kokonaistulot
    print("5) Vahvistettujen varausten kokonaistulot")
    summa_rahana = 0.0

    for merkinta in varausdata:
        if merkinta["varausVahvistettu"]:
            yksikkohinta = merkinta["hinta"]
            tunnit = merkinta["varauksenKesto"]
            summa_rahana += yksikkohinta * tunnit

    print(f'Vahvistettujen varausten kokonaistulot: {summa_rahana} €')


if __name__ == "__main__":
    main()