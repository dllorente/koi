from app.schemas.bizum import BizumEventPublic, BizumListResponse

DEMO_BIZUM_EVENTS =[
  {
    "bizum_id": "bz-001",
    "user_id": "u001",
    "booking_date": "2026-04-16",
    "amount": -15.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Carlos Ruiz",
    "concept": "Cena",
    "status": "completed"
  },
  {
    "bizum_id": "bz-002",
    "user_id": "u001",
    "booking_date": "2026-04-15",
    "amount": 25.5,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Lucía Martín",
    "concept": "Entradas cine",
    "status": "completed"
  },
  {
    "bizum_id": "bz-003",
    "user_id": "u001",
    "booking_date": "2026-04-12",
    "amount": -8.75,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Pablo Gómez",
    "concept": "Café",
    "status": "completed"
  },
  {
    "bizum_id": "bz-004",
    "user_id": "u002",
    "booking_date": "2026-04-16",
    "amount": 40.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Marina López",
    "concept": "Regalo compartido",
    "status": "completed"
  },
  {
    "bizum_id": "bz-005",
    "user_id": "u003",
    "booking_date": "2026-04-14",
    "amount": -12.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Sergio Díaz",
    "concept": "Taxi",
    "status": "completed"
  },
  {
    "bizum_id": "bz-006",
    "user_id": "u004",
    "booking_date": "2026-04-17",
    "amount": -20.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Elena Vega",
    "concept": "Gasolina",
    "status": "completed"
  },
  {
    "bizum_id": "bz-007",
    "user_id": "u005",
    "booking_date": "2026-04-16",
    "amount": 10.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Javier Cobo",
    "concept": "Cañas",
    "status": "completed"
  },
  {
    "bizum_id": "bz-008",
    "user_id": "u006",
    "booking_date": "2026-04-15",
    "amount": -50.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Marta Hierro",
    "concept": "Reserva casa rural",
    "status": "completed"
  },
  {
    "bizum_id": "bz-009",
    "user_id": "u007",
    "booking_date": "2026-04-14",
    "amount": 15.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Adrián Pardo",
    "concept": "Lotería",
    "status": "completed"
  },
  {
    "bizum_id": "bz-010",
    "user_id": "u008",
    "booking_date": "2026-04-13",
    "amount": -30.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Hugo Rojo",
    "concept": "Compra cumple",
    "status": "completed"
  },
  {
    "bizum_id": "bz-011",
    "user_id": "u009",
    "booking_date": "2026-04-12",
    "amount": 5.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Clara Valls",
    "concept": "Helado",
    "status": "completed"
  },
  {
    "bizum_id": "bz-012",
    "user_id": "u010",
    "booking_date": "2026-04-11",
    "amount": -22.5,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Raúl Mas",
    "concept": "Cena pizza",
    "status": "completed"
  },
  {
    "bizum_id": "bz-013",
    "user_id": "u011",
    "booking_date": "2026-04-10",
    "amount": 12.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Julia Ibáñez",
    "concept": "Uber vuelta",
    "status": "completed"
  },
  {
    "bizum_id": "bz-014",
    "user_id": "u012",
    "booking_date": "2026-04-09",
    "amount": -10.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Óscar Luna",
    "concept": "Padel",
    "status": "completed"
  },
  {
    "bizum_id": "bz-015",
    "user_id": "u013",
    "booking_date": "2026-04-08",
    "amount": 100.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Nerea Vidal",
    "concept": "Boda regalo",
    "status": "completed"
  },
  {
    "bizum_id": "bz-016",
    "user_id": "u014",
    "booking_date": "2026-04-07",
    "amount": -18.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Sergio Pino",
    "concept": "Hamburguesas",
    "status": "completed"
  },
  {
    "bizum_id": "bz-017",
    "user_id": "u015",
    "booking_date": "2026-04-06",
    "amount": 25.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Irene Lozano",
    "concept": "Flores",
    "status": "completed"
  },
  {
    "bizum_id": "bz-018",
    "user_id": "u016",
    "booking_date": "2026-04-05",
    "amount": -45.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Manuel Jurado",
    "concept": "Entrada concierto",
    "status": "completed"
  },
  {
    "bizum_id": "bz-019",
    "user_id": "u017",
    "booking_date": "2026-04-04",
    "amount": 7.5,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Paula Calvo",
    "concept": "Desayuno",
    "status": "completed"
  },
  {
    "bizum_id": "bz-020",
    "user_id": "u018",
    "booking_date": "2026-04-03",
    "amount": -12.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Andrés Flores",
    "concept": "Cervezas tarde",
    "status": "completed"
  },
  {
    "bizum_id": "bz-021",
    "user_id": "u019",
    "booking_date": "2026-04-02",
    "amount": 15.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "David Llorente",
    "concept": "Bizum pendiente",
    "status": "completed"
  },
  {
    "bizum_id": "bz-022",
    "user_id": "u020",
    "booking_date": "2026-04-01",
    "amount": -35.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Fernanda Morales",
    "concept": "Cena tailandés",
    "status": "completed"
  },
  {
    "bizum_id": "bz-023",
    "user_id": "u021",
    "booking_date": "2026-03-31",
    "amount": 20.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Jose Antonio Pascual",
    "concept": "Material oficina",
    "status": "completed"
  },
  {
    "bizum_id": "bz-024",
    "user_id": "u022",
    "booking_date": "2026-03-30",
    "amount": -9.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Elena Garrido",
    "concept": "Cine",
    "status": "completed"
  },
  {
    "bizum_id": "bz-025",
    "user_id": "u023",
    "booking_date": "2026-03-29",
    "amount": 14.5,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Ricardo Sanz",
    "concept": "Almuerzo",
    "status": "completed"
  },
  {
    "bizum_id": "bz-026",
    "user_id": "u024",
    "booking_date": "2026-03-28",
    "amount": -5.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Beatriz Soler",
    "concept": "Cafés",
    "status": "completed"
  },
  {
    "bizum_id": "bz-027",
    "user_id": "u025",
    "booking_date": "2026-03-27",
    "amount": 50.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Marcos Ruiz",
    "concept": "Deuda",
    "status": "completed"
  },
  {
    "bizum_id": "bz-028",
    "user_id": "u001",
    "booking_date": "2026-03-26",
    "amount": -11.2,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Lucía Méndez",
    "concept": "Glovo compartido",
    "status": "completed"
  },
  {
    "bizum_id": "bz-029",
    "user_id": "u002",
    "booking_date": "2026-03-25",
    "amount": -22.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Sonia Ortega",
    "concept": "Teatro",
    "status": "completed"
  },
  {
    "bizum_id": "bz-030",
    "user_id": "u003",
    "booking_date": "2026-03-24",
    "amount": 18.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Pablo Narváez",
    "concept": "Libro",
    "status": "completed"
  },
  {
    "bizum_id": "bz-031",
    "user_id": "u004",
    "booking_date": "2026-03-23",
    "amount": -30.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Marta Hierro",
    "concept": "Vinos",
    "status": "completed"
  },
  {
    "bizum_id": "bz-032",
    "user_id": "u005",
    "booking_date": "2026-03-22",
    "amount": -15.5,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Adrián Pardo",
    "concept": "Bolos",
    "status": "completed"
  },
  {
    "bizum_id": "bz-033",
    "user_id": "u006",
    "booking_date": "2026-03-21",
    "amount": 40.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Isabel Conde",
    "concept": "Regalo mamá",
    "status": "completed"
  },
  {
    "bizum_id": "bz-034",
    "user_id": "u007",
    "booking_date": "2026-03-20",
    "amount": -6.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Hugo Rojo",
    "concept": "Cerveza",
    "status": "completed"
  },
  {
    "bizum_id": "bz-035",
    "user_id": "u008",
    "booking_date": "2026-03-19",
    "amount": 12.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Clara Valls",
    "concept": "Bus",
    "status": "completed"
  },
  {
    "bizum_id": "bz-036",
    "user_id": "u009",
    "booking_date": "2026-03-18",
    "amount": -25.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Raúl Mas",
    "concept": "Sushi",
    "status": "completed"
  },
  {
    "bizum_id": "bz-037",
    "user_id": "u010",
    "booking_date": "2026-03-17",
    "amount": 9.5,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Julia Ibáñez",
    "concept": "Tapa",
    "status": "completed"
  },
  {
    "bizum_id": "bz-038",
    "user_id": "u011",
    "booking_date": "2026-03-16",
    "amount": -50.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Óscar Luna",
    "concept": "Fútbol 7 alquiler",
    "status": "completed"
  },
  {
    "bizum_id": "bz-039",
    "user_id": "u012",
    "booking_date": "2026-03-15",
    "amount": 15.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Nerea Vidal",
    "concept": "Flores cumple",
    "status": "completed"
  },
  {
    "bizum_id": "bz-040",
    "user_id": "u013",
    "booking_date": "2026-03-14",
    "amount": -22.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Sergio Pino",
    "concept": "Comida",
    "status": "completed"
  },
  {
    "bizum_id": "bz-041",
    "user_id": "u014",
    "booking_date": "2026-03-13",
    "amount": 30.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Irene Lozano",
    "concept": "Regalo despedida",
    "status": "completed"
  },
  {
    "bizum_id": "bz-042",
    "user_id": "u015",
    "booking_date": "2026-03-12",
    "amount": -4.5,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Manuel Jurado",
    "concept": "Caña",
    "status": "completed"
  },
  {
    "bizum_id": "bz-043",
    "user_id": "u016",
    "booking_date": "2026-03-11",
    "amount": 25.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Paula Calvo",
    "concept": "Manicura",
    "status": "completed"
  },
  {
    "bizum_id": "bz-044",
    "user_id": "u017",
    "booking_date": "2026-03-10",
    "amount": -15.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Andrés Flores",
    "concept": "Kebab",
    "status": "completed"
  },
  {
    "bizum_id": "bz-045",
    "user_id": "u018",
    "booking_date": "2026-03-09",
    "amount": 10.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "David Llorente",
    "concept": "Aparcamiento",
    "status": "completed"
  },
  {
    "bizum_id": "bz-046",
    "user_id": "u019",
    "booking_date": "2026-03-08",
    "amount": -30.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Fernanda Morales",
    "concept": "Gasolina viaje",
    "status": "completed"
  },
  {
    "bizum_id": "bz-047",
    "user_id": "u020",
    "booking_date": "2026-03-07",
    "amount": 15.5,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Jose Antonio Pascual",
    "concept": "Comida oficina",
    "status": "completed"
  },
  {
    "bizum_id": "bz-048",
    "user_id": "u021",
    "booking_date": "2026-03-06",
    "amount": -20.0,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Elena Garrido",
    "concept": "Teatro entradas",
    "status": "completed"
  },
  {
    "bizum_id": "bz-049",
    "user_id": "u022",
    "booking_date": "2026-03-05",
    "amount": 8.0,
    "currency": "EUR",
    "direction": "received",
    "counterparty": "Ricardo Sanz",
    "concept": "Hielo y vasos",
    "status": "completed"
  },
  {
    "bizum_id": "bz-050",
    "user_id": "u023",
    "booking_date": "2026-03-04",
    "amount": -12.5,
    "currency": "EUR",
    "direction": "sent",
    "counterparty": "Beatriz Soler",
    "concept": "Burger",
    "status": "completed"
  }
]

#Filtra todos los eventos Bizum del usuario y los ordena de más recientes a más antiguos.
def get_bizum_events_by_user_id(user_id: str) -> list[dict]:
    events = [
        event for event in DEMO_BIZUM_EVENTS
        if event["user_id"] == user_id
    ]

    return sorted(
        events,
        key=lambda event: event["booking_date"],
        reverse=True,
    )

#Devuelve la actividad Bizum general del cliente autenticado en formato público
def get_public_bizum_events_by_user_id(user_id: str, limit: int = 10) -> BizumListResponse:
    events = get_bizum_events_by_user_id(user_id)[:limit]

    items = [
        BizumEventPublic(
            bizum_id=event["bizum_id"],
            booking_date=event["booking_date"],
            amount=event["amount"],
            currency=event["currency"],
            direction=event["direction"],
            counterparty=event["counterparty"],
            concept=event["concept"],
            status=event["status"],
        )
        for event in events
    ]

    return BizumListResponse(
        items=items,
        count=len(items),
    )

#Filtra solo los Bizum recibidos.
def get_received_bizum_events_by_user_id(user_id: str, limit: int = 10) -> BizumListResponse:
    events = [
        event for event in get_bizum_events_by_user_id(user_id)
        if event["direction"] == "received"
    ][:limit]

    items = [
        BizumEventPublic(
            bizum_id=event["bizum_id"],
            booking_date=event["booking_date"],
            amount=event["amount"],
            currency=event["currency"],
            direction=event["direction"],
            counterparty=event["counterparty"],
            concept=event["concept"],
            status=event["status"],
        )
        for event in events
    ]

    return BizumListResponse(
        items=items,
        count=len(items),
    )