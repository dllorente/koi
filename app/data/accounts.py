from app.schemas.accounts import (
    AccountBalanceItem,
    AccountPublic,
    BalanceSummary,
    BalanceSummaryDetailed,
)

DEMO_ACCOUNTS =[
  {
    "account_id": "acc-001",
    "user_id": "u001",
    "iban": "ES9121000418450200051332",
    "alias": "Cuenta principal",
    "balance": 2450.75,
    "currency": "EUR"
  },
  {
    "account_id": "acc-002",
    "user_id": "u001",
    "iban": "ES2100491500051234567891",
    "alias": "Cuenta ahorro",
    "balance": 10840.2,
    "currency": "EUR"
  },
  {
    "account_id": "acc-003",
    "user_id": "u002",
    "iban": "ES7921000813610123456789",
    "alias": "Cuenta nómina",
    "balance": 3210.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-004",
    "user_id": "u002",
    "iban": "ES5501825002370201234567",
    "alias": "Cuenta diaria",
    "balance": 980.4,
    "currency": "EUR"
  },
  {
    "account_id": "acc-005",
    "user_id": "u003",
    "iban": "ES1221000105450200012345",
    "alias": "Cuenta principal",
    "balance": 1540.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-006",
    "user_id": "u003",
    "iban": "ES4421000206450200067890",
    "alias": "Cuenta ahorro",
    "balance": 22300.5,
    "currency": "EUR"
  },
  {
    "account_id": "acc-007",
    "user_id": "u004",
    "iban": "ES3321000307450200011223",
    "alias": "Cuenta nómina",
    "balance": 4120.65,
    "currency": "EUR"
  },
  {
    "account_id": "acc-008",
    "user_id": "u004",
    "iban": "ES6621000408450200044556",
    "alias": "Cuenta diaria",
    "balance": 120.3,
    "currency": "EUR"
  },
  {
    "account_id": "acc-009",
    "user_id": "u005",
    "iban": "ES8821000509450200077889",
    "alias": "Cuenta principal",
    "balance": 5600.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-010",
    "user_id": "u005",
    "iban": "ES1121000610450200099001",
    "alias": "Gastos ocio",
    "balance": 890.15,
    "currency": "EUR"
  },
  {
    "account_id": "acc-011",
    "user_id": "u006",
    "iban": "ES2221000711450200022334",
    "alias": "Cuenta principal",
    "balance": 3100.45,
    "currency": "EUR"
  },
  {
    "account_id": "acc-012",
    "user_id": "u006",
    "iban": "ES5521000812450200055667",
    "alias": "Cuenta ahorro",
    "balance": 15000.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-013",
    "user_id": "u007",
    "iban": "ES7721000913450200088990",
    "alias": "Cuenta nómina",
    "balance": 2750.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-014",
    "user_id": "u007",
    "iban": "ES9921001014450200011224",
    "alias": "Cuenta diaria",
    "balance": 430.2,
    "currency": "EUR"
  },
  {
    "account_id": "acc-015",
    "user_id": "u008",
    "iban": "ES1021001115450200033445",
    "alias": "Cuenta principal",
    "balance": 6200.8,
    "currency": "EUR"
  },
  {
    "account_id": "acc-016",
    "user_id": "u008",
    "iban": "ES2021001216450200055668",
    "alias": "Vacaciones",
    "balance": 2400.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-017",
    "user_id": "u009",
    "iban": "ES3021001317450200077881",
    "alias": "Cuenta nómina",
    "balance": 1980.5,
    "currency": "EUR"
  },
  {
    "account_id": "acc-018",
    "user_id": "u009",
    "iban": "ES4021001418450200099002",
    "alias": "Inversión",
    "balance": 12500.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-019",
    "user_id": "u010",
    "iban": "ES5021001519450200022335",
    "alias": "Cuenta principal",
    "balance": 850.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-020",
    "user_id": "u010",
    "iban": "ES6021001620450200044557",
    "alias": "Reserva fondo",
    "balance": 5000.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-021",
    "user_id": "u011",
    "iban": "ES7021001721450200066778",
    "alias": "Cuenta principal",
    "balance": 3420.15,
    "currency": "EUR"
  },
  {
    "account_id": "acc-022",
    "user_id": "u011",
    "iban": "ES8021001822450200088992",
    "alias": "Ahorro",
    "balance": 9200.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-023",
    "user_id": "u012",
    "iban": "ES9021001923450200011226",
    "alias": "Cuenta nómina",
    "balance": 2150.3,
    "currency": "EUR"
  },
  {
    "account_id": "acc-024",
    "user_id": "u012",
    "iban": "ES1121002024450200033448",
    "alias": "Gastos casa",
    "balance": 670.45,
    "currency": "EUR"
  },
  {
    "account_id": "acc-025",
    "user_id": "u013",
    "iban": "ES2221002125450200055660",
    "alias": "Cuenta principal",
    "balance": 4800.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-026",
    "user_id": "u013",
    "iban": "ES3321002226450200077883",
    "alias": "Cuenta ahorro",
    "balance": 18500.25,
    "currency": "EUR"
  },
  {
    "account_id": "acc-027",
    "user_id": "u014",
    "iban": "ES4421002327450200099005",
    "alias": "Cuenta nómina",
    "balance": 3300.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-028",
    "user_id": "u014",
    "iban": "ES5521002428450200022339",
    "alias": "Suscripciones",
    "balance": 150.75,
    "currency": "EUR"
  },
  {
    "account_id": "acc-029",
    "user_id": "u015",
    "iban": "ES6621002529450200044551",
    "alias": "Cuenta principal",
    "balance": 7200.4,
    "currency": "EUR"
  },
  {
    "account_id": "acc-030",
    "user_id": "u015",
    "iban": "ES7721002630450200066774",
    "alias": "Ahorro infantil",
    "balance": 3000.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-031",
    "user_id": "u016",
    "iban": "ES8821002731450200088996",
    "alias": "Cuenta principal",
    "balance": 2100.2,
    "currency": "EUR"
  },
  {
    "account_id": "acc-032",
    "user_id": "u016",
    "iban": "ES9921002832450200011228",
    "alias": "Gastos varios",
    "balance": 540.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-033",
    "user_id": "u017",
    "iban": "ES1021002933450200033441",
    "alias": "Cuenta nómina",
    "balance": 2890.6,
    "currency": "EUR"
  },
  {
    "account_id": "acc-034",
    "user_id": "u017",
    "iban": "ES2021003034450200055663",
    "alias": "Viajes",
    "balance": 1200.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-035",
    "user_id": "u018",
    "iban": "ES3021003135450200077885",
    "alias": "Cuenta principal",
    "balance": 4300.75,
    "currency": "EUR"
  },
  {
    "account_id": "acc-036",
    "user_id": "u018",
    "iban": "ES4021003236450200099007",
    "alias": "Cuenta ahorro",
    "balance": 11000.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-037",
    "user_id": "u019",
    "iban": "ES5021003337450200022331",
    "alias": "Cuenta nómina",
    "balance": 3600.25,
    "currency": "EUR"
  },
  {
    "account_id": "acc-038",
    "user_id": "u019",
    "iban": "ES6021003438450200044553",
    "alias": "Seguro",
    "balance": 800.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-039",
    "user_id": "u020",
    "iban": "ES7021003539450200066775",
    "alias": "Cuenta principal",
    "balance": 520.4,
    "currency": "EUR"
  },
  {
    "account_id": "acc-040",
    "user_id": "u020",
    "iban": "ES8021003640450200088997",
    "alias": "Emergencias",
    "balance": 4000.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-041",
    "user_id": "u021",
    "iban": "ES9021003741450200011221",
    "alias": "Cuenta nómina",
    "balance": 2950.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-042",
    "user_id": "u021",
    "iban": "ES1121003842450200033442",
    "alias": "Ahorro coche",
    "balance": 6500.8,
    "currency": "EUR"
  },
  {
    "account_id": "acc-043",
    "user_id": "u022",
    "iban": "ES2221003943450200055665",
    "alias": "Cuenta principal",
    "balance": 1800.35,
    "currency": "EUR"
  },
  {
    "account_id": "acc-044",
    "user_id": "u022",
    "iban": "ES3321004044450200077887",
    "alias": "Gastos hijos",
    "balance": 420.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-045",
    "user_id": "u023",
    "iban": "ES4421004145450200099009",
    "alias": "Cuenta nómina",
    "balance": 3100.9,
    "currency": "EUR"
  },
  {
    "account_id": "acc-046",
    "user_id": "u023",
    "iban": "ES5521004246450200022332",
    "alias": "Inversión Bolsa",
    "balance": 25000.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-047",
    "user_id": "u024",
    "iban": "ES6621004347450200044554",
    "alias": "Cuenta principal",
    "balance": 1100.15,
    "currency": "EUR"
  },
  {
    "account_id": "acc-048",
    "user_id": "u024",
    "iban": "ES7721004448450200066776",
    "alias": "Ahorro reforma",
    "balance": 8700.0,
    "currency": "EUR"
  },
  {
    "account_id": "acc-049",
    "user_id": "u025",
    "iban": "ES8821004549450200088998",
    "alias": "Cuenta nómina",
    "balance": 4100.5,
    "currency": "EUR"
  },
  {
    "account_id": "acc-050",
    "user_id": "u025",
    "iban": "ES9921004650450200011222",
    "alias": "Gastos compartidos",
    "balance": 630.2,
    "currency": "EUR"
  }
]

def get_accounts_by_user_id(user_id: str) -> list[dict]:
    return [account for account in DEMO_ACCOUNTS if account["user_id"] == user_id]

def get_public_accounts_by_user_id(user_id: str) -> list[AccountPublic]:
    accounts = get_accounts_by_user_id(user_id)
    return [
        AccountPublic(
            account_id=account["account_id"],
            iban=account["iban"],
            alias=account["alias"],
            balance=account["balance"],
            currency=account["currency"],
        )
        for account in accounts
    ]

#Calcula la suma de balances de todas las cuentas del usuario.
def get_total_balance_by_user_id(user_id: str) -> float:
    accounts = get_accounts_by_user_id(user_id)
    return round(sum(account["balance"] for account in accounts), 2)

#Construye un resumen agregado simple usando BalanceSummary
def get_balance_summary_by_user_id(user_id: str) -> BalanceSummary:
    accounts = get_accounts_by_user_id(user_id)
    currency = accounts[0]["currency"] if accounts else "EUR"

    return BalanceSummary(
        user_id=user_id,
        currency=currency,
        total_balance=round(sum(account["balance"] for account in accounts), 2),
        account_count=len(accounts),
    )

def get_detailed_balance_summary_by_user_id(user_id: str) -> BalanceSummaryDetailed:
    accounts = get_accounts_by_user_id(user_id)
    currency = accounts[0]["currency"] if accounts else "EUR"

    return BalanceSummaryDetailed(
        user_id=user_id,
        currency=currency,
        total_balance=round(sum(account["balance"] for account in accounts), 2),
        account_count=len(accounts),
        accounts=[
            AccountBalanceItem(
                account_id=account["account_id"],
                alias=account["alias"],
                balance=account["balance"],
                currency=account["currency"],
            )
            for account in accounts
        ],
    )