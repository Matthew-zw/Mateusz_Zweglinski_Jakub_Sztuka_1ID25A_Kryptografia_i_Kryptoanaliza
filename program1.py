# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import argparse
import sys

def wczytaj_plik(nazwa_pliku):
    """Wczytuje zawartość pliku."""
    try:
        with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
            return plik.read()
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {nazwa_pliku}")
        sys.exit(1)
    except Exception as e:
        print(f"Wystąpił błąd podczas odczytu pliku {nazwa_pliku}: {e}")
        sys.exit(1)

def zapisz_plik(nazwa_pliku, zawartosc):
    """Zapisuje zawartość do pliku."""
    try:
        with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
            plik.write(zawartosc)
    except Exception as e:
        print(f"Wystąpił błąd podczas zapisu do pliku {nazwa_pliku}: {e}")
        sys.exit(1)

def wczytaj_klucz(nazwa_pliku):
    """Wczytuje klucz podstawieniowy z pliku."""
    mapa_podstawien = {}
    try:
        with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
            for linia in plik:
                if len(linia.strip()) == 0:
                    continue
                czesci = linia.split()
                if len(czesci) != 2:
                    print(f"Błąd: Nieprawidłowy format klucza w pliku {nazwa_pliku}. Oczekiwano dwóch kolumn.")
                    sys.exit(1)
                mapa_podstawien[czesci[0].upper()] = czesci[1].upper()
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku klucza {nazwa_pliku}")
        sys.exit(1)
    except Exception as e:
        print(f"Wystąpił błąd podczas odczytu pliku klucza {nazwa_pliku}: {e}")
        sys.exit(1)
    return mapa_podstawien

def przygotuj_tekst(tekst):
    """Konwertuje tekst do wielkich liter i usuwa znaki niebędące literami."""
    przygotowany_tekst = ""
    for znak in tekst:
        if 'A' <= znak.upper() <= 'Z':
            przygotowany_tekst += znak.upper()
    return przygotowany_tekst

def szyfruj(tekst, klucz):
    """Szyfruje tekst przy użyciu podanego klucza."""
    szyfrogram = ""
    for znak in tekst:
        szyfrogram += klucz.get(znak, znak)
    return szyfrogram

def deszyfruj(szyfrogram, klucz):
    """Deszyfruje tekst przy użyciu odwróconego klucza."""
    odwrocony_klucz = {v: k for k, v in klucz.items()}
    tekst_jawny = ""
    for znak in szyfrogram:
        tekst_jawny += odwrocony_klucz.get(znak, znak)
    return tekst_jawny

def main():
    """Główna funkcja programu."""
    parser = argparse.ArgumentParser(description="Program do szyfrowania i deszyfrowania tekstu za pomocą szyfru podstawieniowego.")
    
    parser.add_argument('-i', '--input', required=True, help="Nazwa pliku wejściowego.")
    parser.add_argument('-o', '--output', required=True, help="Nazwa pliku wyjściowego.")
    parser.add_argument('-k', '--key', required=True, help="Nazwa pliku z kluczem.")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', action='store_true', help="Tryb szyfrowania.")
    group.add_argument('-d', '--decrypt', action='store_true', help="Tryb deszyfrowania.")

    args = parser.parse_args()

    tekst_wejsciowy = wczytaj_plik(args.input)
    klucz = wczytaj_klucz(args.key)
    
    przetworzony_tekst = przygotuj_tekst(tekst_wejsciowy)

    if args.encrypt:
        wynik = szyfruj(przetworzony_tekst, klucz)
        print("Szyfrowanie zakończone pomyślnie.")
    elif args.decrypt:
        wynik = deszyfruj(przetworzony_tekst, klucz)
        print("Deszyfrowanie zakończone pomyślnie.")

    zapisz_plik(args.output, wynik)
    print(f"Wynik został zapisany do pliku: {args.output}")

if __name__ == "__main__":
    main()