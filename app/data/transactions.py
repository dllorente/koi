from app.data.accounts import get_accounts_by_user_id
from app.schemas.transaction import TransactionListResponse, TransactionPublic

DEMO_TRANSACTIONS=[
  {
    "transaction_id": "tx-001",
    "account_id": "acc-001",
    "booking_date": "2026-04-16",
    "amount": -52.35,
    "currency": "EUR",
    "description": "Supermercado Carrefour",
    "category": "groceries"
  },
  {
    "transaction_id": "tx-002",
    "account_id": "acc-001",
    "booking_date": "2026-04-15",
    "amount": -18.5,
    "currency": "EUR",
    "description": "Cafetería Madrid Centro",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-003",
    "account_id": "acc-001",
    "booking_date": "2026-04-14",
    "amount": 2200.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-004",
    "account_id": "acc-002",
    "booking_date": "2026-04-13",
    "amount": 150.0,
    "currency": "EUR",
    "description": "Transferencia interna",
    "category": "transfer"
  },
  {
    "transaction_id": "tx-005",
    "account_id": "acc-002",
    "booking_date": "2026-04-10",
    "amount": -600.0,
    "currency": "EUR",
    "description": "Alquiler vivienda",
    "category": "housing"
  },
  {
    "transaction_id": "tx-006",
    "account_id": "acc-003",
    "booking_date": "2026-04-16",
    "amount": -35.9,
    "currency": "EUR",
    "description": "Gasolinera Repsol",
    "category": "transport"
  },
  {
    "transaction_id": "tx-007",
    "account_id": "acc-003",
    "booking_date": "2026-04-14",
    "amount": 1900.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-008",
    "account_id": "acc-004",
    "booking_date": "2026-04-15",
    "amount": -72.1,
    "currency": "EUR",
    "description": "Farmacia",
    "category": "health"
  },
  {
    "transaction_id": "tx-009",
    "account_id": "acc-005",
    "booking_date": "2026-04-12",
    "amount": -12.4,
    "currency": "EUR",
    "description": "Netflix Subscription",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-010",
    "account_id": "acc-006",
    "booking_date": "2026-04-11",
    "amount": -45.0,
    "currency": "EUR",
    "description": "Restaurante La Tagliatella",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-011",
    "account_id": "acc-007",
    "booking_date": "2026-04-14",
    "amount": 2100.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-012",
    "account_id": "acc-008",
    "booking_date": "2026-04-09",
    "amount": -22.15,
    "currency": "EUR",
    "description": "Uber Trip",
    "category": "transport"
  },
  {
    "transaction_id": "tx-013",
    "account_id": "acc-009",
    "booking_date": "2026-04-08",
    "amount": -89.99,
    "currency": "EUR",
    "description": "ZARA Moda",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-014",
    "account_id": "acc-010",
    "booking_date": "2026-04-07",
    "amount": -30.0,
    "currency": "EUR",
    "description": "Cines Yelmo",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-015",
    "account_id": "acc-011",
    "booking_date": "2026-04-06",
    "amount": -120.0,
    "currency": "EUR",
    "description": "Gimnasio mensual",
    "category": "health"
  },
  {
    "transaction_id": "tx-016",
    "account_id": "acc-012",
    "booking_date": "2026-04-05",
    "amount": 500.0,
    "currency": "EUR",
    "description": "Transferencia de ahorro",
    "category": "transfer"
  },
  {
    "transaction_id": "tx-017",
    "account_id": "acc-013",
    "booking_date": "2026-04-14",
    "amount": 1850.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-018",
    "account_id": "acc-014",
    "booking_date": "2026-04-04",
    "amount": -15.2,
    "currency": "EUR",
    "description": "Starbucks Coffee",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-019",
    "account_id": "acc-015",
    "booking_date": "2026-04-03",
    "amount": -250.0,
    "currency": "EUR",
    "description": "Apple Store Online",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-020",
    "account_id": "acc-016",
    "booking_date": "2026-04-02",
    "amount": -65.4,
    "currency": "EUR",
    "description": "IKEA Montaje",
    "category": "housing"
  },
  {
    "transaction_id": "tx-021",
    "account_id": "acc-017",
    "booking_date": "2026-04-14",
    "amount": 2300.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-022",
    "account_id": "acc-018",
    "booking_date": "2026-04-01",
    "amount": -40.0,
    "currency": "EUR",
    "description": "Suscripción Gym",
    "category": "health"
  },
  {
    "transaction_id": "tx-023",
    "account_id": "acc-019",
    "booking_date": "2026-03-31",
    "amount": -5.5,
    "currency": "EUR",
    "description": "Parking Centro",
    "category": "transport"
  },
  {
    "transaction_id": "tx-024",
    "account_id": "acc-020",
    "booking_date": "2026-03-30",
    "amount": -110.0,
    "currency": "EUR",
    "description": "Factura Endesa",
    "category": "housing"
  },
  {
    "transaction_id": "tx-025",
    "account_id": "acc-021",
    "booking_date": "2026-04-14",
    "amount": 2050.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-026",
    "account_id": "acc-022",
    "booking_date": "2026-03-29",
    "amount": -45.6,
    "currency": "EUR",
    "description": "Lidl Supermercado",
    "category": "groceries"
  },
  {
    "transaction_id": "tx-027",
    "account_id": "acc-023",
    "booking_date": "2026-04-14",
    "amount": 1950.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-028",
    "account_id": "acc-024",
    "booking_date": "2026-03-28",
    "amount": -18.9,
    "currency": "EUR",
    "description": "Mc Donalds",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-029",
    "account_id": "acc-025",
    "booking_date": "2026-03-27",
    "amount": -95.0,
    "currency": "EUR",
    "description": "Amazon.es",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-030",
    "account_id": "acc-026",
    "booking_date": "2026-03-26",
    "amount": 1000.0,
    "currency": "EUR",
    "description": "Bonus trimestral",
    "category": "income"
  },
  {
    "transaction_id": "tx-031",
    "account_id": "acc-027",
    "booking_date": "2026-04-14",
    "amount": 2100.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-032",
    "account_id": "acc-028",
    "booking_date": "2026-03-25",
    "amount": -9.99,
    "currency": "EUR",
    "description": "Spotify Premium",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-033",
    "account_id": "acc-029",
    "booking_date": "2026-03-24",
    "amount": -62.0,
    "currency": "EUR",
    "description": "Mercadona",
    "category": "groceries"
  },
  {
    "transaction_id": "tx-034",
    "account_id": "acc-030",
    "booking_date": "2026-03-23",
    "amount": -200.0,
    "currency": "EUR",
    "description": "Seguro Coche",
    "category": "transport"
  },
  {
    "transaction_id": "tx-035",
    "account_id": "acc-031",
    "booking_date": "2026-04-14",
    "amount": 2400.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-036",
    "account_id": "acc-032",
    "booking_date": "2026-03-22",
    "amount": -34.5,
    "currency": "EUR",
    "description": "Pizzería Roma",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-037",
    "account_id": "acc-033",
    "booking_date": "2026-04-14",
    "amount": 2600.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-038",
    "account_id": "acc-034",
    "booking_date": "2026-03-21",
    "amount": -450.0,
    "currency": "EUR",
    "description": "Vuelo Iberia",
    "category": "transport"
  },
  {
    "transaction_id": "tx-039",
    "account_id": "acc-035",
    "booking_date": "2026-03-20",
    "amount": -78.2,
    "currency": "EUR",
    "description": "El Corte Inglés",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-040",
    "account_id": "acc-036",
    "booking_date": "2026-03-19",
    "amount": -55.0,
    "currency": "EUR",
    "description": "Factura Movistar",
    "category": "housing"
  },
  {
    "transaction_id": "tx-041",
    "account_id": "acc-037",
    "booking_date": "2026-04-14",
    "amount": 2250.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-042",
    "account_id": "acc-038",
    "booking_date": "2026-03-18",
    "amount": -12.5,
    "currency": "EUR",
    "description": "Estanco",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-043",
    "account_id": "acc-039",
    "booking_date": "2026-03-17",
    "amount": -28.9,
    "currency": "EUR",
    "description": "Burger King",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-044",
    "account_id": "acc-040",
    "booking_date": "2026-03-16",
    "amount": -150.0,
    "currency": "EUR",
    "description": "Reparación Caldera",
    "category": "housing"
  },
  {
    "transaction_id": "tx-045",
    "account_id": "acc-041",
    "booking_date": "2026-04-14",
    "amount": 1980.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-046",
    "account_id": "acc-042",
    "booking_date": "2026-03-15",
    "amount": -42.1,
    "currency": "EUR",
    "description": "Gasolinera Cepsa",
    "category": "transport"
  },
  {
    "transaction_id": "tx-047",
    "account_id": "acc-043",
    "booking_date": "2026-03-14",
    "amount": -18.0,
    "currency": "EUR",
    "description": "Peluquería Paco",
    "category": "health"
  },
  {
    "transaction_id": "tx-048",
    "account_id": "acc-044",
    "booking_date": "2026-03-13",
    "amount": -33.5,
    "currency": "EUR",
    "description": "Decathlon",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-049",
    "account_id": "acc-045",
    "booking_date": "2026-04-14",
    "amount": 2150.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-050",
    "account_id": "acc-046",
    "booking_date": "2026-03-12",
    "amount": -75.0,
    "currency": "EUR",
    "description": "Entradas Concierto",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-051",
    "account_id": "acc-047",
    "booking_date": "2026-03-11",
    "amount": -54.2,
    "currency": "EUR",
    "description": "Ahorramas",
    "category": "groceries"
  },
  {
    "transaction_id": "tx-052",
    "account_id": "acc-048",
    "booking_date": "2026-03-10",
    "amount": -22.0,
    "currency": "EUR",
    "description": "Tapas Bar",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-053",
    "account_id": "acc-049",
    "booking_date": "2026-04-14",
    "amount": 2500.0,
    "currency": "EUR",
    "description": "Nómina abril",
    "category": "income"
  },
  {
    "transaction_id": "tx-054",
    "account_id": "acc-050",
    "booking_date": "2026-03-09",
    "amount": -8.5,
    "currency": "EUR",
    "description": "Quiosco",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-055",
    "account_id": "acc-001",
    "booking_date": "2026-03-08",
    "amount": -12.3,
    "currency": "EUR",
    "description": "App Store",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-056",
    "account_id": "acc-002",
    "booking_date": "2026-03-07",
    "amount": -14.2,
    "currency": "EUR",
    "description": "Peaje Autopista",
    "category": "transport"
  },
  {
    "transaction_id": "tx-057",
    "account_id": "acc-003",
    "booking_date": "2026-03-06",
    "amount": -65.0,
    "currency": "EUR",
    "description": "Compra Farmacia",
    "category": "health"
  },
  {
    "transaction_id": "tx-058",
    "account_id": "acc-004",
    "booking_date": "2026-03-05",
    "amount": -24.9,
    "currency": "EUR",
    "description": "KFC Online",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-059",
    "account_id": "acc-005",
    "booking_date": "2026-03-04",
    "amount": -115.0,
    "currency": "EUR",
    "description": "Zapatos Nike",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-060",
    "account_id": "acc-006",
    "booking_date": "2026-03-03",
    "amount": -42.0,
    "currency": "EUR",
    "description": "Sushi Takeaway",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-061",
    "account_id": "acc-007",
    "booking_date": "2026-03-02",
    "amount": -85.5,
    "currency": "EUR",
    "description": "Factura Agua",
    "category": "housing"
  },
  {
    "transaction_id": "tx-062",
    "account_id": "acc-008",
    "booking_date": "2026-03-01",
    "amount": -15.0,
    "currency": "EUR",
    "description": "Metro Madrid",
    "category": "transport"
  },
  {
    "transaction_id": "tx-063",
    "account_id": "acc-009",
    "booking_date": "2026-02-28",
    "amount": -31.2,
    "currency": "EUR",
    "description": "Libros Amazon",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-064",
    "account_id": "acc-010",
    "booking_date": "2026-02-27",
    "amount": -45.0,
    "currency": "EUR",
    "description": "Cena Italiana",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-065",
    "account_id": "acc-011",
    "booking_date": "2026-02-26",
    "amount": -58.9,
    "currency": "EUR",
    "description": "Gasolina 95",
    "category": "transport"
  },
  {
    "transaction_id": "tx-066",
    "account_id": "acc-012",
    "booking_date": "2026-02-25",
    "amount": 200.0,
    "currency": "EUR",
    "description": "Venta Wallapop",
    "category": "income"
  },
  {
    "transaction_id": "tx-067",
    "account_id": "acc-013",
    "booking_date": "2026-02-24",
    "amount": -12.0,
    "currency": "EUR",
    "description": "HBO Max",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-068",
    "account_id": "acc-014",
    "booking_date": "2026-02-23",
    "amount": -95.0,
    "currency": "EUR",
    "description": "Seguro de Hogar",
    "category": "housing"
  },
  {
    "transaction_id": "tx-069",
    "account_id": "acc-015",
    "booking_date": "2026-02-22",
    "amount": -145.0,
    "currency": "EUR",
    "description": "Gafas de sol",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-070",
    "account_id": "acc-016",
    "booking_date": "2026-02-21",
    "amount": -22.5,
    "currency": "EUR",
    "description": "Prensa y revistas",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-071",
    "account_id": "acc-017",
    "booking_date": "2026-02-20",
    "amount": -180.0,
    "currency": "EUR",
    "description": "Mantenimiento coche",
    "category": "transport"
  },
  {
    "transaction_id": "tx-072",
    "account_id": "acc-018",
    "booking_date": "2026-02-19",
    "amount": -30.0,
    "currency": "EUR",
    "description": "Regalo cumpleaños",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-073",
    "account_id": "acc-019",
    "booking_date": "2026-02-18",
    "amount": -7.2,
    "currency": "EUR",
    "description": "Panadería",
    "category": "groceries"
  },
  {
    "transaction_id": "tx-074",
    "account_id": "acc-020",
    "booking_date": "2026-02-17",
    "amount": -55.0,
    "currency": "EUR",
    "description": "Factura Teléfono",
    "category": "housing"
  },
  {
    "transaction_id": "tx-075",
    "account_id": "acc-021",
    "booking_date": "2026-02-16",
    "amount": -48.0,
    "currency": "EUR",
    "description": "Entradas Cine",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-076",
    "account_id": "acc-022",
    "booking_date": "2026-02-15",
    "amount": -19.9,
    "currency": "EUR",
    "description": "Pizza Hut",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-077",
    "account_id": "acc-023",
    "booking_date": "2026-02-14",
    "amount": -65.0,
    "currency": "EUR",
    "description": "Cena San Valentín",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-078",
    "account_id": "acc-024",
    "booking_date": "2026-02-13",
    "amount": -32.5,
    "currency": "EUR",
    "description": "Juguetería",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-079",
    "account_id": "acc-025",
    "booking_date": "2026-02-12",
    "amount": -14.8,
    "currency": "EUR",
    "description": "Café y tostada",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-080",
    "account_id": "acc-026",
    "booking_date": "2026-02-11",
    "amount": -89.0,
    "currency": "EUR",
    "description": "Ropa Deporte",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-081",
    "account_id": "acc-027",
    "booking_date": "2026-02-10",
    "amount": -110.0,
    "currency": "EUR",
    "description": "Revisión Gas",
    "category": "housing"
  },
  {
    "transaction_id": "tx-082",
    "account_id": "acc-028",
    "booking_date": "2026-02-09",
    "amount": -25.0,
    "currency": "EUR",
    "description": "Lavandería",
    "category": "housing"
  },
  {
    "transaction_id": "tx-083",
    "account_id": "acc-029",
    "booking_date": "2026-02-08",
    "amount": -42.6,
    "currency": "EUR",
    "description": "Supermercado Dia",
    "category": "groceries"
  },
  {
    "transaction_id": "tx-084",
    "account_id": "acc-030",
    "booking_date": "2026-02-07",
    "amount": 150.0,
    "currency": "EUR",
    "description": "Regalo familiar",
    "category": "income"
  },
  {
    "transaction_id": "tx-085",
    "account_id": "acc-031",
    "booking_date": "2026-02-06",
    "amount": -12.9,
    "currency": "EUR",
    "description": "Amazon Prime",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-086",
    "account_id": "acc-032",
    "booking_date": "2026-02-05",
    "amount": -35.0,
    "currency": "EUR",
    "description": "Taxi Aeropuerto",
    "category": "transport"
  },
  {
    "transaction_id": "tx-087",
    "account_id": "acc-033",
    "booking_date": "2026-02-04",
    "amount": -8.4,
    "currency": "EUR",
    "description": "Desayuno",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-088",
    "account_id": "acc-034",
    "booking_date": "2026-02-03",
    "amount": -120.0,
    "currency": "EUR",
    "description": "Hotel Noche",
    "category": "transport"
  },
  {
    "transaction_id": "tx-089",
    "account_id": "acc-035",
    "booking_date": "2026-02-02",
    "amount": -22.1,
    "currency": "EUR",
    "description": "Papelería",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-090",
    "account_id": "acc-036",
    "booking_date": "2026-02-01",
    "amount": -55.0,
    "currency": "EUR",
    "description": "Factura Luz",
    "category": "housing"
  },
  {
    "transaction_id": "tx-091",
    "account_id": "acc-037",
    "booking_date": "2026-01-31",
    "amount": -6.5,
    "currency": "EUR",
    "description": "Parking",
    "category": "transport"
  },
  {
    "transaction_id": "tx-092",
    "account_id": "acc-038",
    "booking_date": "2026-01-30",
    "amount": -45.9,
    "currency": "EUR",
    "description": "Mango Moda",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-093",
    "account_id": "acc-039",
    "booking_date": "2026-01-29",
    "amount": -15.2,
    "currency": "EUR",
    "description": "Heladería",
    "category": "restaurants"
  },
  {
    "transaction_id": "tx-094",
    "account_id": "acc-040",
    "booking_date": "2026-01-28",
    "amount": -75.0,
    "currency": "EUR",
    "description": "Fontanero",
    "category": "housing"
  },
  {
    "transaction_id": "tx-095",
    "account_id": "acc-041",
    "booking_date": "2026-01-27",
    "amount": -38.4,
    "currency": "EUR",
    "description": "Gasolinera",
    "category": "transport"
  },
  {
    "transaction_id": "tx-096",
    "account_id": "acc-042",
    "booking_date": "2026-01-26",
    "amount": -14.0,
    "currency": "EUR",
    "description": "Corte de pelo",
    "category": "health"
  },
  {
    "transaction_id": "tx-097",
    "account_id": "acc-043",
    "booking_date": "2026-01-25",
    "amount": -52.0,
    "currency": "EUR",
    "description": "H&M Online",
    "category": "shopping"
  },
  {
    "transaction_id": "tx-098",
    "account_id": "acc-044",
    "booking_date": "2026-01-24",
    "amount": -9.5,
    "currency": "EUR",
    "description": "Revistas",
    "category": "leisure"
  },
  {
    "transaction_id": "tx-099",
    "account_id": "acc-045",
    "booking_date": "2026-01-23",
    "amount": -44.2,
    "currency": "EUR",
    "description": "Supermercado",
    "category": "groceries"
  },
  {
    "transaction_id": "tx-100",
    "account_id": "acc-046",
    "booking_date": "2026-01-22",
    "amount": -30.0,
    "currency": "EUR",
    "description": "Cena Pizza",
    "category": "restaurants"
  }
]

#Filtra el dataset de transacciones por cuenta.
def get_transactions_by_account_id(account_id: str) -> list[dict]:
    return [
        tx for tx in DEMO_TRANSACTIONS
        if tx["account_id"] == account_id
    ]

#Hace una unión lógica entre cuentas y transacciones
def get_transactions_by_user_id(user_id: str) -> list[dict]:
    accounts = get_accounts_by_user_id(user_id)
    account_ids = {account["account_id"] for account in accounts}

    transactions = [
        tx for tx in DEMO_TRANSACTIONS
        if tx["account_id"] in account_ids
    ]

    return sorted(
        transactions,
        key=lambda tx: tx["booking_date"],
        reverse=True,
    )

#Convierte los movimientos del usuario en respuesta pública tipada y limita resultados
def get_public_transactions_by_user_id(user_id: str, limit: int = 10) -> TransactionListResponse:
    transactions = get_transactions_by_user_id(user_id)[:limit]

    items = [
        TransactionPublic(
            transaction_id=tx["transaction_id"],
            account_id=tx["account_id"],
            booking_date=tx["booking_date"],
            amount=tx["amount"],
            currency=tx["currency"],
            description=tx["description"],
            category=tx["category"],
        )
        for tx in transactions
    ]

    return TransactionListResponse(
        items=items,
        count=len(items),
    )


def get_public_transactions_by_account_id(account_id: str, limit: int = 10) -> TransactionListResponse:
    transactions = sorted(
        get_transactions_by_account_id(account_id),
        key=lambda tx: tx["booking_date"],
        reverse=True,
    )[:limit]

    items = [
        TransactionPublic(
            transaction_id=tx["transaction_id"],
            account_id=tx["account_id"],
            booking_date=tx["booking_date"],
            amount=tx["amount"],
            currency=tx["currency"],
            description=tx["description"],
            category=tx["category"],
        )
        for tx in transactions
    ]

    return TransactionListResponse(
        items=items,
        count=len(items),
    )