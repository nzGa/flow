#!/usr/bin/env python3
"""Generate a Flow CSV import covering the last six months of sample activity.

Columns match the in-app CSV template (see csvImportTemplateUrl in
lib/constants.dart and test/import/valid-1.csv). Amounts use a dot decimal
and no thousands separator. Dates are YYYY-MM-DD; times are 24-hour HH:MM:SS.

Currency is not a CSV column — pick it in the import wizard:
  Principal, Efectivo, Ahorros → ARS
  Dólares → USD  (change this account after the first pick, which
                  applies ARS to every account)

Import erases existing data. Regenerating:

  python3 scripts/generate_sample_csv.py
  python3 scripts/generate_sample_csv.py --today 2026-09-14
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")

HEADERS = [
    "flow_title",
    "flow_notes",
    "flow_account_name",
    "flow_amount",
    "flow_date_of_transaction",
    "flow_time_of_transaction_optional",
    "flow_date_of_transaction_iso_8601",
    "flow_category_optional",
]

PRINCIPAL = "Principal"
EFECTIVO = "Efectivo"
AHORROS = "Ahorros"
DOLARES = "Dólares"

# Spanish names matching assets/l10n/es_ES.json so icons resolve when the
# app locale is Spanish.
NOMINA = "Nómina"
ALQUILER = "Alquiler"
COMPRA = "Compra"
COMER_FUERA = "Comer fuera"
BEBIDAS = "Bebidas"
TRANSPORTE = "Transporte"
GASOLINA = "Gasolina"
COMPRAS = "Compras"
ENTRETENIMIENTO = "Entretenimiento"
SUSCRIPCIONES = "Suscripciones online"
SUMINISTROS = "Suministros"
SALUD = "Salud"
FITNESS = "Fitness"
BELLEZA = "Belleza"
AFICIONES = "Aficiones"
MASCOTAS = "Cuidado de mascotas"
VIAJES = "Viajes"
REGALOS = "Regalos"
DONACIONES = "Donaciones"
EDUCACION = "Educación"
DISPOSITIVOS = "Dispositivos"
SERVICIOS = "Servicios"
SEGUROS = "Seguros"
IMPUESTOS = "Impuestos"
HIGIENE = "Higiene"
APERITIVOS = "Aperitivos"

DEFAULT_OUTPUT = Path("docs/sample_import.csv")


def money(rng: random.Random, low: float, high: float, ndigits: int = 2) -> float:
    return round(rng.uniform(low, high), ndigits)


def chance(rng: random.Random, probability: float) -> bool:
    return rng.random() < probability


def pick(rng: random.Random, items: list[T]) -> T:
    return items[rng.randint(0, len(items) - 1)]


def spend_account(
    ledger: Ledger,
    rng: random.Random,
    amount: float,
    prefer_cash_odds: float,
) -> str:
    cost = abs(amount)
    if chance(rng, prefer_cash_odds) and ledger.balances[EFECTIVO] >= cost:
        return EFECTIVO
    return PRINCIPAL


def at_time(
    rng: random.Random,
    day: date,
    hour_start: int = 8,
    hour_end: int = 21,
) -> datetime:
    hour = rng.randint(hour_start, hour_end)
    return datetime.combine(
        day,
        time(hour, rng.randint(0, 59), rng.randint(0, 59)),
    )


class Ledger:
    """Collects CSV rows and keeps running balances so transfers stay sane."""

    def __init__(self) -> None:
        self.rows: list[tuple[datetime, int, list[str]]] = []
        self._seq = 0
        self.balances: dict[str, float] = {
            PRINCIPAL: 0.0,
            EFECTIVO: 0.0,
            AHORROS: 0.0,
            DOLARES: 0.0,
        }

    def add(
        self,
        when: datetime,
        account: str,
        amount: float,
        title: str,
        category: str = "",
        notes: str = "",
    ) -> None:
        amount = round(amount, 2)
        self.rows.append(
            (
                when,
                self._seq,
                [
                    title,
                    notes,
                    account,
                    f"{amount:.2f}",
                    when.strftime("%Y-%m-%d"),
                    when.strftime("%H:%M:%S"),
                    "",
                    category,
                ],
            )
        )
        self._seq += 1
        self.balances[account] = round(self.balances[account] + amount, 2)

    def transfer(
        self,
        when: datetime,
        source: str,
        target: str,
        amount: float,
        title: str,
        notes: str = "",
    ) -> None:
        amount = round(amount, 2)
        if amount <= 0:
            return
        self.add(when, source, -amount, title, notes=notes)
        self.add(when, target, amount, title, notes=notes)

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        ordered = [row for _, _, row in sorted(self.rows, key=lambda item: (item[0], item[1]))]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(HEADERS)
            writer.writerows(ordered)


def seed_opening_balances(ledger: Ledger, start: date) -> None:
    opening = datetime.combine(start, time(9, 0, 0))
    ledger.add(opening, PRINCIPAL, 2_100_000.00, "Saldo inicial")
    ledger.add(opening, EFECTIVO, 68_500.00, "Saldo inicial")
    ledger.add(opening, AHORROS, 1_800_000.00, "Saldo inicial")
    ledger.add(opening, DOLARES, 2_400.00, "Saldo inicial")


def add_recurring(ledger: Ledger, rng: random.Random, day: date) -> None:
    dom = day.day
    month = day.month

    if dom == 1:
        ledger.add(
            datetime.combine(day, time(8, 15, 0)),
            PRINCIPAL,
            -850_000.00,
            "Alquiler departamento",
            ALQUILER,
            "Palermo, CABA",
        )
        ledger.add(
            datetime.combine(day, time(8, 20, 0)),
            PRINCIPAL,
            -55_000.00,
            "Smart Fit",
            FITNESS,
        )

    if dom == 2:
        ledger.add(
            datetime.combine(day, time(0, 5, 12)),
            PRINCIPAL,
            -2_499.00,
            "iCloud+",
            SUSCRIPCIONES,
        )

    if dom == 5:
        ledger.add(
            datetime.combine(day, time(0, 8, 40)),
            PRINCIPAL,
            -12_999.00,
            "Netflix",
            SUSCRIPCIONES,
        )

    if dom == 6:
        ledger.add(
            datetime.combine(day, time(10, 0, 0)),
            PRINCIPAL,
            -45_000.00,
            "Fibertel internet",
            SUMINISTROS,
        )

    if dom == 9:
        ledger.add(
            datetime.combine(day, time(0, 3, 21)),
            PRINCIPAL,
            -7_999.00,
            "Spotify",
            SUSCRIPCIONES,
        )

    if dom == 10:
        ledger.add(
            datetime.combine(day, time(11, 30, 0)),
            PRINCIPAL,
            -8_000.00,
            "Donación mensual",
            DONACIONES,
            "Cruz Roja Argentina",
        )

    if dom == 12:
        ledger.add(
            datetime.combine(day, time(0, 12, 0)),
            PRINCIPAL,
            -24_900.00,
            "ChatGPT Plus",
            SUSCRIPCIONES,
        )

    if dom == 18:
        ledger.add(
            datetime.combine(day, time(9, 45, 0)),
            PRINCIPAL,
            -28_400.00,
            "Personal móvil",
            SUMINISTROS,
        )

    if dom == 20:
        # Winter (Jun–Aug) AC/heating bump; milder in autumn/spring.
        low, high = (62_000, 95_000) if month in {6, 7, 8} else (38_000, 58_000)
        ledger.add(
            datetime.combine(day, time(14, 10, 0)),
            PRINCIPAL,
            -money(rng, low, high, 0),
            "Edenor luz",
            SUMINISTROS,
        )

    if dom == 22:
        ledger.add(
            datetime.combine(day, time(13, 0, 0)),
            PRINCIPAL,
            -18_500.00,
            "AySA agua",
            SUMINISTROS,
        )

    if dom == 14 and month in {4, 7}:
        ledger.add(
            datetime.combine(day, time(10, 0, 0)),
            PRINCIPAL,
            -86_000.00,
            "Seguro del auto",
            SEGUROS,
        )

    if month == 6 and dom == 30:
        ledger.add(
            datetime.combine(day, time(9, 10, 0)),
            PRINCIPAL,
            1_600_000.00,
            "Aguinaldo (1er semestre)",
            NOMINA,
        )

    if month == 8 and dom == 11:
        ledger.add(
            datetime.combine(day, time(16, 0, 0)),
            PRINCIPAL,
            -52_000.00,
            "Monotributo",
            IMPUESTOS,
        )


def add_payday(ledger: Ledger, rng: random.Random, day: date) -> None:
    salary = round(3_200_000 * rng.uniform(0.992, 1.008), 2)
    ledger.add(
        datetime.combine(day, time(9, 15, 0)),
        PRINCIPAL,
        salary,
        "Sueldo",
        NOMINA,
    )

    if chance(rng, 0.35):
        ledger.add(
            at_time(rng, day, 11, 16),
            PRINCIPAL,
            money(rng, 180_000, 420_000, 0),
            pick(rng, ["Freelance diseño", "Hora extra", "Proyecto puntual"]),
            SERVICIOS,
        )

    if ledger.balances[PRINCIPAL] >= 480_000:
        ledger.transfer(
            datetime.combine(day, time(12, 30, 0)),
            PRINCIPAL,
            EFECTIVO,
            80_000.00,
            "Extracción cajero",
        )

    savings = min(200_000.00, max(0.0, ledger.balances[PRINCIPAL] - 1_200_000))
    if savings >= 50_000:
        ledger.transfer(
            datetime.combine(day, time(12, 35, 0)),
            PRINCIPAL,
            AHORROS,
            round(savings, 2),
            "Ahorro mensual",
        )


def add_usd_activity(ledger: Ledger, rng: random.Random, day: date) -> None:
    if day.day == 15 and day.month in {4, 6, 8}:
        ledger.add(
            datetime.combine(day, time(17, 40, 0)),
            DOLARES,
            money(rng, 280, 450, 2),
            "Freelance USD",
            SERVICIOS,
            "Cliente en el exterior",
        )

    if day.month == 5 and day.day == 8:
        ledger.add(
            datetime.combine(day, time(21, 12, 0)),
            DOLARES,
            -14.99,
            "Steam",
            AFICIONES,
        )

    if day.month == 7 and day.day == 3:
        ledger.add(
            datetime.combine(day, time(11, 5, 0)),
            DOLARES,
            -89.00,
            "Cursor Pro",
            SUSCRIPCIONES,
        )


def add_winter_trip(ledger: Ledger, rng: random.Random, day: date) -> None:
    # Vacaciones de invierno ~ last week of July.
    if day.month != 7 or day.day != 20:
        return

    ledger.add(
        datetime.combine(day, time(6, 40, 0)),
        PRINCIPAL,
        -186_000.00,
        "Flybondi AEP–BRC",
        VIAJES,
    )
    ledger.add(
        datetime.combine(day, time(18, 20, 0)),
        PRINCIPAL,
        -420_000.00,
        "Airbnb Bariloche",
        VIAJES,
        "5 noches",
    )

    for offset, title, amount, category in (
        (1, "Cena El Boliche de Alberto", -48_000.00, COMER_FUERA),
        (1, "Cerro Catedral day pass", -62_000.00, ENTRETENIMIENTO),
        (2, "Almuerzo Puerto Moreno", -32_500.00, COMER_FUERA),
        (2, "Souvenirs centro cívico", -27_800.00, COMPRAS),
        (3, "Chocolate Rapa Nui", -18_400.00, APERITIVOS),
        (3, "Taxi Bariloche", -9_600.00, TRANSPORTE),
        (4, "Cena El Boliche de Alberto", -51_200.00, COMER_FUERA),
        (5, "Flybondi BRC–AEP", -186_000.00, VIAJES),
    ):
        trip_day = day + timedelta(days=offset)
        ledger.add(at_time(rng, trip_day, 10, 22), PRINCIPAL, amount, title, category)


def add_daily_spend(ledger: Ledger, rng: random.Random, day: date) -> None:
    weekend = day.weekday() >= 5

    if chance(rng, 0.55 if weekend else 0.62):
        cafe = pick(
            rng,
            [
                ("Café Martínez", -6_200.00),
                ("Havanna café", -7_400.00),
                ("Starbucks", -8_100.00),
                ("Cuervo café", -5_800.00),
                ("Ninina", -9_200.00),
            ],
        )
        account = spend_account(ledger, rng, cafe[1], 0.45)
        ledger.add(at_time(rng, day, 8, 11), account, cafe[1], cafe[0], BEBIDAS)

    if chance(rng, 0.40 if weekend else 0.16):
        shop = pick(rng, ["Carrefour", "Coto", "Disco", "Jumbo", "Día"])
        ledger.add(
            at_time(rng, day, 11, 19),
            PRINCIPAL,
            -money(rng, 38_000, 98_000, 0),
            shop,
            COMPRA,
        )

    if chance(rng, 0.48 if weekend else 0.22):
        place = pick(
            rng,
            [
                "Guerrín",
                "El Club de la Milanesa",
                "Mostaza",
                "Burger King",
                "Siga la Vaca",
                "Don Julio (barra)",
                "PedidosYa",
                "Rappi",
            ],
        )
        amount = -money(rng, 16_000, 58_000, 0)
        account = spend_account(ledger, rng, amount, 0.3)
        ledger.add(
            at_time(rng, day, 12, 22),
            account,
            amount,
            place,
            COMER_FUERA,
        )

    if chance(rng, 0.18):
        snack = pick(rng, ["Kiosco", "Medialunas", "Heladería Chungo", "Panadería"])
        amount = -money(rng, 3_500, 12_000, 0)
        account = spend_account(ledger, rng, amount, 0.7)
        ledger.add(
            at_time(rng, day, 16, 19),
            account,
            amount,
            snack,
            APERITIVOS,
        )

    if chance(rng, 0.22 if weekend else 0.55):
        ride = pick(rng, ["SUBE subte", "Colectivo", "Uber", "Cabify", "BA Taxi"])
        amount = (
            -money(rng, 1_200, 2_400, 0)
            if ride in {"SUBE subte", "Colectivo"}
            else -money(rng, 6_500, 18_500, 0)
        )
        cash_odds = 0.0 if ride == "Uber" else 0.55
        account = spend_account(ledger, rng, amount, cash_odds)
        ledger.add(at_time(rng, day, 7, 23), account, amount, ride, TRANSPORTE)

    if chance(rng, 0.07):
        ledger.add(
            at_time(rng, day, 10, 18),
            PRINCIPAL,
            -money(rng, 38_000, 58_000, 0),
            pick(rng, ["YPF", "Shell", "Axion"]),
            GASOLINA,
        )

    if chance(rng, 0.28 if weekend else 0.06):
        fun = pick(
            rng,
            [
                ("Cinemark", -14_500.00),
                ("Hoyts", -15_800.00),
                ("Partido River", -42_000.00),
                ("Steam oferta", -8_999.00),
                ("Recital Niceto", -28_000.00),
                ("Museo MALBA", -6_000.00),
            ],
        )
        ledger.add(at_time(rng, day, 15, 22), PRINCIPAL, fun[1], fun[0], ENTRETENIMIENTO)

    if chance(rng, 0.10):
        ledger.add(
            at_time(rng, day, 12, 20),
            PRINCIPAL,
            -money(rng, 18_000, 95_000, 0),
            pick(rng, ["Mercado Libre", "Zara", "Falabella", "Easy", "Uniqlo"]),
            COMPRAS,
        )

    if chance(rng, 0.03):
        ledger.add(
            at_time(rng, day, 10, 18),
            PRINCIPAL,
            -money(rng, 8_500, 32_000, 0),
            pick(rng, ["Farmacity", "Dr. Ahorro", "OSDE copago"]),
            SALUD,
        )

    if chance(rng, 0.035):
        ledger.add(
            at_time(rng, day, 11, 19),
            PRINCIPAL,
            -money(rng, 12_000, 38_000, 0),
            pick(rng, ["Corte de pelo", "Manicura", "Farmacia dermocosmética"]),
            BELLEZA,
        )

    if chance(rng, 0.05):
        ledger.add(
            at_time(rng, day, 14, 21),
            PRINCIPAL,
            -money(rng, 9_000, 46_000, 0),
            pick(rng, ["Guitar Center strings", "Libros Gandhi", "Lego"]),
            AFICIONES,
        )

    if chance(rng, 0.03):
        ledger.add(
            at_time(rng, day, 11, 17),
            PRINCIPAL,
            -money(rng, 14_000, 52_000, 0),
            pick(rng, ["Pet shop", "Alimento Royal Canin", "Veterinaria"]),
            MASCOTAS,
        )

    if chance(rng, 0.015):
        ledger.add(
            at_time(rng, day, 10, 16),
            PRINCIPAL,
            -money(rng, 6_000, 22_000, 0),
            pick(rng, ["Farmacity higiene", "Supermercado limpieza"]),
            HIGIENE,
        )

    if chance(rng, 0.012):
        ledger.add(
            at_time(rng, day, 19, 21),
            PRINCIPAL,
            -money(rng, 18_000, 85_000, 0),
            pick(rng, ["Curso Udemy", "Clases de inglés"]),
            EDUCACION,
        )

    if chance(rng, 0.006):
        ledger.add(
            at_time(rng, day, 12, 20),
            PRINCIPAL,
            -money(rng, 120_000, 480_000, 0),
            pick(rng, ["Auriculares Sony", "Mouse Logitech", "SSD"]),
            DISPOSITIVOS,
        )

    if day.month == 5 and day.day == 20:
        ledger.add(
            at_time(rng, day, 16, 18),
            PRINCIPAL,
            -42_000.00,
            "Regalo mamá",
            REGALOS,
            "Día de la Madre",
        )

    if day.month == 8 and day.day == 8:
        ledger.add(
            at_time(rng, day, 15, 18),
            PRINCIPAL,
            -38_500.00,
            "Regalo papá",
            REGALOS,
            "Día del Padre",
        )

    if day.weekday() == 4 and chance(rng, 0.4):
        if ledger.balances[PRINCIPAL] >= 240_000:
            ledger.transfer(
                at_time(rng, day, 12, 14),
                PRINCIPAL,
                EFECTIVO,
                40_000.00,
                "Extracción efectivo",
            )


def window_start(today: date) -> date:
    """Inclusive start: the same day-of-month six calendar months earlier."""
    month = today.month - 6
    year = today.year
    if month <= 0:
        month += 12
        year -= 1
    return date(year, month, min(today.day, _days_in_month(year, month)))


def generate(today: date, seed: int) -> Ledger:
    start = window_start(today)
    rng = random.Random(seed)
    ledger = Ledger()
    seed_opening_balances(ledger, start)

    cursor = start
    while cursor <= today:
        add_recurring(ledger, rng, cursor)
        if cursor.day == 25:
            add_payday(ledger, rng, cursor)
        add_usd_activity(ledger, rng, cursor)
        add_winter_trip(ledger, rng, cursor)
        add_daily_spend(ledger, rng, cursor)
        cursor += timedelta(days=1)

    return ledger


def _days_in_month(year: int, month: int) -> int:
    if month == 12:
        nxt = date(year + 1, 1, 1)
    else:
        nxt = date(year, month + 1, 1)
    return (nxt - timedelta(days=1)).day


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="Inclusive end date (default: today). Window is ~6 months back.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="RNG seed. Defaults to YYYYMMDD of --today for a stable snapshot.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"CSV path (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    seed = args.seed if args.seed is not None else int(args.today.strftime("%Y%m%d"))
    ledger = generate(args.today, seed)
    ledger.write(args.output)
    start = window_start(args.today)
    print(
        f"Wrote {len(ledger.rows)} transactions to {args.output} "
        f"({start.isoformat()}..{args.today.isoformat()}, seed={seed})"
    )
    print("Balances:", ledger.balances)


if __name__ == "__main__":
    main()
