from app.core.passwords import verify_password
from app.schemas.user import UserPublic
from sqlmodel import Session, select
from app.db.models import User

DEMO_USERS = [
    {
        "user_id": "u001",
        "full_name": "David Llorente Raposo",
        "email": "davidllorenten@example.com",
        "password": "koi1234",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$y27Qf6z8x8kA69OZ+8Ha7w$LfwNq+fcUNxon3qdAtgMTdg/IzTOqr0OLBfqLFem7Hc",
    },
    {
        "user_id": "u002",
        "full_name": "Fernanda Morales Barba",
        "email": "ferMor@example.com",
        "password": "koi1876",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$walDvSW2xtU6/kUD5O0Zag$a/PhW4tqS0hizJEaoQrSu6cnk0ncoIZM6qTetFNQmOU",
    },
    {
        "user_id": "u003",
        "full_name": "Jose Antonio Pascual Llorente",
        "email": "JAPascual@example.com",
        "password": "koi9821",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$etL2p/2lK5g0VRygTKAmvg$NKtmQE3KU+HAQoBksScva7sBVP+Sh/HYNOl4tSAPCk8",
    },
    {
        "user_id": "u004",
        "full_name": "Elena Garrido Vega",
        "email": "egarrido@example.com",
        "password": "koi4432",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$tUmKSaEoRgiAFcTPTFg8iQ$L+kBLgKrz3lXH8x3xpL12weK+nGGAPUF+VtS56NfBJc",
    },
    {
        "user_id": "u005",
        "full_name": "Ricardo Sanz Ocaña",
        "email": "rsanz@example.com",
        "password": "koi5567",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$s/kuYcpt5t2vVxqgRxKtGg$ARGGXfaFK7Gy1e04wy1gBkNuGkZRNpsux4UIY7uTEWY",
    },
    {
        "user_id": "u006",
        "full_name": "Beatriz Soler Maza",
        "email": "bsoler@example.com",
        "password": "koi6678",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$vxw9hJQi+orKhL/PfL5T9A$F950F7IahZiHXLm19QifiTWcfnxShs0kQZUOPcqdAc8",
    },
    {
        "user_id": "u007",
        "full_name": "Marcos Ruiz Peña",
        "email": "mruiz@example.com",
        "password": "koi7789",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$caI54J/348wuY9qJ/cPBIw$fBzi8e8tT4/jULxQf4fzInNwKTURTc7ZW5u9fReCWrk",
    },
    {
        "user_id": "u008",
        "full_name": "Lucía Méndez Vila",
        "email": "lmendez@example.com",
        "password": "koi8890",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$zl8h5wi+BgrV5yoWwBxisw$OgSgTz0nULANkUW7r02U1kcFvp6wy7xDpFmyHIgiwdA",
    },
    {
        "user_id": "u009",
        "full_name": "Javier Cobo Arce",
        "email": "jcobo@example.com",
        "password": "koi9901",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$IA+JwW7ieU2ZAQ5y9nQPXQ$PfklQBZxrBV/sNxRf9YhGUrZ4G6zOv+Vgrm4E5jBTJo",
    },
    {
        "user_id": "u010",
        "full_name": "Sonia Ortega Gil",
        "email": "sortega@example.com",
        "password": "koi1012",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$QhdtuASTx4XTpmKcMLnh5g$X6Qohuei831y7uXSocC6MRCOj/NfgOKzlFszaGvz1Ro",
    },
    {
        "user_id": "u011",
        "full_name": "Pablo Narváez Diez",
        "email": "pnarvaez@example.com",
        "password": "koi1123",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$RxfosHo2imxB40t/2NJ77g$at5f4hr2Q8Q2nR4VgWQLKOnK1iw4BpVvbfNzYcUKjmk",
    },
    {
        "user_id": "u012",
        "full_name": "Marta Hierro Rivas",
        "email": "mhierro@example.com",
        "password": "koi1235",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$g4OaGv5HJIgGPYtjN47rKA$gcCsBdWc4sd5af/9wCwuW6l8LdHPvQAZtGVk4VcMzeA",
    },
    {
        "user_id": "u013",
        "full_name": "Adrián Pardo Cano",
        "email": "apardo@example.com",
        "password": "koi1346",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$1F6IQgsq4V1GlRKJqe2zcA$8cQk/64kQHVXJFJSlXLEz3yDyz6Ldw01u5l2Q0bjGYo",
    },
    {
        "user_id": "u014",
        "full_name": "Isabel Conde Marín",
        "email": "iconde@example.com",
        "password": "koi1457",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$SAvhxWPl0xIDjPqBHd7rog$pLM67eS4QnC8vJiaHO0J95UvsZHV8XxN3Ni7GuIhLEQ",
    },
    {
        "user_id": "u015",
        "full_name": "Hugo Rojo Santos",
        "email": "hrojo@example.com",
        "password": "koi1568",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$CnyegIiDq9bA/3EQC4jyXQ$/aLBeqZUE6ZqgyXdJuGXZVMgkmV5oJ2PHkAkhdHdsuE",
    },
    {
        "user_id": "u016",
        "full_name": "Clara Valls Esteve",
        "email": "cvalls@example.com",
        "password": "koi1679",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$1w+RS6qKRpI5EKvxDyUDxQ$bpHsg1Vx3kyJ1a3Ug6qihTceFB6DzcF3V5CG7ZJRZyA",
    },
    {
        "user_id": "u017",
        "full_name": "Raúl Mas Ferrer",
        "email": "rmas@example.com",
        "password": "koi1780",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$uYhnwgmrssS7P7WWBmT7zg$kgUvDEFu6KV5WzH5C3LLdgSwmn/tACRhqjPpuyD/ibs",
    },
    {
        "user_id": "u018",
        "full_name": "Julia Ibáñez Guerra",
        "email": "jibanez@example.com",
        "password": "koi1891",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$FLZsu+QIfOdZ7ZpgZ7r3pA$wcYa4TvqpLWRwZ5R0IcIRSkqIkgPaSzjlJOOGWtytS0",
    },
    {
        "user_id": "u019",
        "full_name": "Óscar Luna Mora",
        "email": "oluna@example.com",
        "password": "koi1902",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$162sDWoeQw+gSL4UIddFoQ$dqUaAj3W+Lvpc4lmmY56YJoLtHDEEwHWwg9Dt2wti08",
    },
    {
        "user_id": "u020",
        "full_name": "Nerea Vidal Bosch",
        "email": "nvidal@example.com",
        "password": "koi2013",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$NB1NVDp66VAN1CC731U/Qw$L4VXX0kvPSRGqd9nEtvB07Kut/JeE9DinqyBaQe83eI",
    },
    {
        "user_id": "u021",
        "full_name": "Sergio Pino Moya",
        "email": "spino@example.com",
        "password": "koi2124",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$GOPnvzCHSFOOw02kVuWc8g$LgWo1Xwv6RzdtmNMYdriaA0hGznIGXCEDlax+jAzplM",
    },
    {
        "user_id": "u022",
        "full_name": "Irene Lozano Cruz",
        "email": "ilozano@example.com",
        "password": "koi2235",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$1eIwv1D6hMEKoRtwFnLlPg$fuUu2TvFLRSXCnTYQkBCRuuo9i+JDDEupQ8Xwld4NFI",
    },
    {
        "user_id": "u023",
        "full_name": "Manuel Jurado Rey",
        "email": "mjurado@example.com",
        "password": "koi2346",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$Hqs/cEyjP8zh2HBqPGikXw$dUyv7u1NoGkBPNFBsEUAy7J4j5ItuvB7/xNfpirrwSw",
    },
    {
        "user_id": "u024",
        "full_name": "Paula Calvo Soria",
        "email": "pcalvo@example.com",
        "password": "koi2457",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$0O9fDNslNI2AkdlyLzaXMg$L4g3MN7aDPTvElP7rLpy8W3q7E1hVLS5ZgqQwWH77gM",
    },
    {
        "user_id": "u025",
        "full_name": "Andrés Flores Gila",
        "email": "aflores@example.com",
        "password": "koi2568",
        "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$CZu9aywHKEaT2vqw7avwyA$thx6t+h6fHQBZBMgKpw+Mm6B+y6dYMTzkdlT71F5pkE",
    },
]


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = session.exec(select(User).where(User.email == email)).first()

    if user and verify_password(password, user.password_hash):
        return user

    return None


def get_user_by_id(session: Session, user_id: str) -> UserPublic | None:
    user = session.get(User, user_id)

    if user is None:
        return None

    return UserPublic(
        user_id=user.user_id,
        full_name=user.full_name,
        email=user.email,
    )
