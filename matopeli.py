#---Matopeli by Lotta Rantala---
import pygame
import random as r
import os
pygame.font.init()

#aloitusasetelmat
mato = {
    "osat" : [(440, 240), (440, 260), (440, 280)],
    "pituus" : 3,
    "suunta" : None,
    "ruoka" : [(200, 80)],
    "pisteet" : 0,
    "päällä" : True
}

#sailytetaan kuvat täällä, helppo päästä käsiksi
kuvat = {
    "paa" : None,
    "vartalo" : None,
    "ruoka" : None,
    "tausta" : None
}

LEVEYS = KORKEUS = 500
#yksi käärmeen "osa" on 20x20
K_LEVEYS, K_KORKEUS = 20, 20
#peliruutu
WIN = pygame.display.set_mode((LEVEYS, KORKEUS))
pygame.display.set_caption("matopeli by Lotta")
fontti = pygame.font.SysFont("KiwiMaru-Light", 30)
FPS = 4

def lataa_kuvat(kuvat):
    #ladataan kuvat ja skaalataan ne sopivan kokoisiksi
    paa = pygame.image.load(os.path.join("kuvat", "kaarmeen_paa.png"))
    kuvat["paa"] = pygame.transform.scale(paa, (K_LEVEYS, K_KORKEUS))
    vartalo = pygame.image.load(os.path.join("kuvat", "kaarmeen_vartalo.png"))
    kuvat["vartalo"] = pygame.transform.scale(vartalo, (K_LEVEYS, K_KORKEUS))
    ruoka = pygame.image.load(os.path.join("kuvat", "hamppari.png"))
    kuvat["ruoka"] = pygame.transform.scale(ruoka, (K_LEVEYS, K_KORKEUS))
    tausta = pygame.image.load(os.path.join("kuvat", "tausta.png"))
    kuvat["tausta"] = pygame.transform.scale(tausta, (LEVEYS, KORKEUS))

def piirra_ikkuna():
    WIN.blit(kuvat["tausta"], (0, 0))
    #ensin piirretään ruoka
    if len(mato["ruoka"]) != 0:
        WIN.blit(kuvat["ruoka"], (mato["ruoka"][0]))
    #muut listan osat ovat osa vartaloa
    for i in range(1, len(mato["osat"])):
        WIN.blit(kuvat["vartalo"], (mato["osat"][i]))    
    #piirtää pään siihen missä sen kuuluu olla; edessä
    WIN.blit(kuvat["paa"], (mato["osat"][0]))
    #pisteet
    teksti = fontti.render("Pisteet: " +str(mato["pisteet"]), 1, (255, 255, 255))
    WIN.blit(teksti, (10, 10))
    pygame.display.update()

def aseta_suunta(suunta):
    mato["suunta"] = suunta
    return mato["suunta"]

def madon_liike(mato):
    #madon liike: eteen lisätään osa, ja takaa poistetaan osa ellei mato ole syönyt jotain
    x, y = mato["osat"][0]
    if mato["suunta"] == "vasen":
        mato["osat"].insert(0, (x-20, y))
    elif mato["suunta"] == "oikea":
        mato["osat"].insert(0, (x+20, y))
    elif mato["suunta"] == "ylos":
        mato["osat"].insert(0, (x, y-20))
    elif mato["suunta"] == "alas":
        mato["osat"].insert(0, (x, y+20))

    #madon pituus pysyy samana ellei mato ole syönyt jotain
    if len(mato["osat"]) > mato["pituus"]:
        mato["osat"].pop()

def tarkista_tormays(mato):
    paa_x, paa_y = mato["osat"][0]
    #tarkistaa onko mato mennyt rajojen ulkopuolelle pituussuunnassa
    if paa_y < 0 or paa_y + 20 > KORKEUS:
        mato["päällä"] = False
    #tarkistaa onko mato mennyt rajojen ulkopuolelle leveyssuunnassa
    if paa_x < 0 or paa_x + 20 > LEVEYS:
        mato["päällä"] = False
    #tarkistaa osuuko pää muuhun kehoon
    if (paa_x, paa_y) in mato["osat"][1:]:
        mato["päällä"] = False
    #tarkistaa osuuko pää ruokaan eli syökö mato
    if len(mato["ruoka"]) != 0:
        if (paa_x, paa_y) == mato["ruoka"][0]:
            #pituus kasvaa
            mato["pituus"] += 1
            #poistetaan ruoka
            mato["ruoka"].pop(0)
            mato["pisteet"] += 1

def luo_ruoka():
    #jos ruudussa ei ole ruokaa, luodaan uusi ruoka
    if len(mato["ruoka"]) == 0:
        x_koordinaatti = r.randrange(0, LEVEYS - 20, 20)
        y_koordinaatti = r.randrange(0, KORKEUS - 20, 20)
        #ei luo ruokaa käärmeen alle
        if (x_koordinaatti, y_koordinaatti) not in mato["osat"]:
            mato["ruoka"].append((x_koordinaatti, y_koordinaatti))
        return mato["ruoka"]

def havio():
    havio_fontti = pygame.font.SysFont("KiwiMaru-Light", 40)
    teksti_1 = havio_fontti.render("Hävisit pelin noob :(", 1, (255, 255, 255))
    teksti_2 = havio_fontti.render("Sait " +str(mato["pisteet"]) + " pistettä", 1, (255, 255, 255))
    WIN.blit(teksti_1, (130, 160))
    WIN.blit(teksti_2, (150, 200))
    pygame.display.update()
    pygame.time.delay(5000)
    #laitetaan oletusasetukset ja aloitetaan peli uudestaan
    mato["osat"] = [(440, 240), (440, 260), (440, 280)]
    mato["pituus"] = 3
    mato["suunta"] = None
    mato["ruoka"] = [(200, 80)]
    mato["pisteet"] = 0
    mato["päällä"] = True
    main()

def main():
    kello = pygame.time.Clock()
    while mato["päällä"]:
        #asetetaan FPS, jottei mato kulje liian lujaa
        kello.tick(FPS)
        for event in pygame.event.get():
            #jos painetaan raksia, peli pysähtyy
            if event.type == pygame.QUIT:
                mato["päällä"] = False
                pygame.quit()
            #jos nappia painetaan
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    aseta_suunta("vasen")
                elif event.key == pygame.K_d:
                    aseta_suunta("oikea")
                elif event.key == pygame.K_w:
                    aseta_suunta("ylos")
                elif event.key == pygame.K_s:
                    aseta_suunta("alas")
        luo_ruoka()
        tarkista_tormays(mato)
        madon_liike(mato)
        piirra_ikkuna()
    havio()

if __name__ == "__main__":
    lataa_kuvat(kuvat)
    main()