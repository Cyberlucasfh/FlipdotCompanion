# Steuerung einer Flipdotmatrix mit Raspberry Pi

[TOC]

## Vorraussetzungen
Der Versuchsaufbau in welchem dieses Programm getestet wurde sieht wie folgt aus: 
LAWO MAX16510-02.00, Verbunden mit einem USB-IBIS Wagenbus-Schnittstellenwandler (V1) an einen Raspberry Pi 3B

### Packages für  Linux/Python
* openmeteo-requests [Link](https://open-meteo.com/en/docs)

### Verbauter Wandler
[Ibis Wandler](https://ibis-wandler.de)

## VDV 300 und Datenformat
Die Kommunikation erfolgt über so genannte Telegramme aus der Norm VDV 300. Meine Anzeige versteht das Format
DS21T (Zieltext) und DS001 (Liniennummer). Zur Kommunikation werden Byte Sequenzen über eine Comport Schnittstelle gesendet. 
Die Telegramme haben dabei folgendes Format: 

### DS001
```byte
lXXX\r<P>
```

XXX Steht dabei für Liniennummer.<p>
Anschließend Folgt ein Carriage Return und zum Schluss eine Prüfsumme, das sogennate Parity Byte.

### DS21T
```
aA1A3Eine Zeile\n\n\n\r<P>
```
```
aA1A3Obere Zeile\nUntere Zeile\n\n\r<P>
```
```
aA14A8Takt1 Zeile 1<LF>Takt1 Zeile 2<LF><LF>Takt2 Zeile1<LF>Takt2 Zeile2<LF><LF>      <CR><2E>
```
* aA = Datensatzkennung 
* 1 = Adresse (1=Front, 2=Seite)
* 4 = Längenbyte
* A3 = Taktzeit