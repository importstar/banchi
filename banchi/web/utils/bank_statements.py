import csv
import datetime
import decimal
import io
import re

import pdfplumber

BROUGHT_FORWARD_LABEL = "ยอดยกมา"
DATE_HEADER_LABEL = "วันที่"
ACCOUNT_NUMBER_LABEL = "เลขที่บัญชีเงินฝาก"

SCB_DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{2}$")
SCB_BALANCE_RE = re.compile(r"[\d,]+\.\d{2}")
SCB_ACCOUNT_NUMBER_RE = re.compile(r"^\d{3}-\d{6}-\d$")

SCB_CREDIT_CARD_DATE_RE = re.compile(r"^\d{2}/\d{2}$")
SCB_CREDIT_CARD_FULL_DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{2}$")
SCB_CREDIT_CARD_AMOUNT_RE = re.compile(r"^-?[\d,]+\.\d{2}$")
SCB_CREDIT_CARD_NUMBER_PATTERNS = [
    re.compile(pattern) for pattern in (r"^\d{4}$", r"^\w{2}XX$", r"^XXXX$", r"^\d{4}$")
]

TTB_CREDIT_CARD_DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
TTB_CREDIT_CARD_AMOUNT_RE = re.compile(r"^-?[\d,]+\.\d{2}$")
TTB_CREDIT_CARD_NUMBER_RE = re.compile(r"^\d{4}-\d{2}XX-XXXX-\d{4}$")

TTB_DAY_RE = re.compile(r"^\d{1,2}$")
TTB_MONTH_RE = re.compile(r"^[A-Za-z]{3}$")
TTB_YEAR_RE = re.compile(r"^\d{2}$")
TTB_TIME_RE = re.compile(r"^\d{2}:\d{2}$")
TTB_AMOUNT_RE = re.compile(r"^[+-][\d,]+\.\d{2}$")
TTB_BALANCE_RE = re.compile(r"^[\d,]+\.\d{2}$")
TTB_ACCOUNT_NUMBER_RE = re.compile(r"^\d{3}-\d-\d{5}-\d$")


class StatementParseError(Exception):
    pass


def _parse_amount(value):
    value = (value or "").strip().replace(",", "")
    if not value:
        return decimal.Decimal("0")
    return decimal.Decimal(value)


def _parse_date(date_str, time_str):
    date = datetime.datetime.strptime(date_str.strip(), "%d-%m-%y")
    if time_str and time_str.strip():
        time_of_day = datetime.datetime.strptime(time_str.strip(), "%H:%M").time()
        date = datetime.datetime.combine(date.date(), time_of_day)
    return date


def parse_kasikorn_statement(file_stream):
    """Parse a K-Bank (Kasikorn) "K-DEPOSIT STATEMENT OF SAVING ACCOUNT" CSV export."""
    text_stream = io.TextIOWrapper(file_stream, encoding="utf-8-sig")
    rows = list(csv.reader(text_stream))

    account_number = None
    header_index = None

    for index, row in enumerate(rows):
        if len(row) > 11 and row[7].strip() == ACCOUNT_NUMBER_LABEL:
            account_number = row[11].strip()
        if header_index is None and any(
            cell.strip() == DATE_HEADER_LABEL for cell in row
        ):
            header_index = index

    if header_index is None:
        raise StatementParseError("Could not find the statement's column header row")

    entries = []
    for row in rows[header_index + 1 :]:
        if len(row) < 9:
            continue

        date_str = row[1].strip()
        description = row[3].strip()
        if not date_str or description == BROUGHT_FORWARD_LABEL:
            continue

        entries.append(
            dict(
                date=_parse_date(date_str, row[2]),
                description=description,
                withdrawal=_parse_amount(row[4]),
                deposit=_parse_amount(row[6]),
                balance=_parse_amount(row[8]),
                channel=row[10].strip() if len(row) > 10 else "",
                detail=row[12].strip() if len(row) > 12 else "",
            )
        )

    if not entries:
        raise StatementParseError("No transaction rows found in the statement")

    return dict(
        account_number=account_number,
        started_date=min(entry["date"] for entry in entries),
        ended_date=max(entry["date"] for entry in entries),
        entries=entries,
    )


def parse_scb_statement(file_stream):
    """Parse a SCB (Siam Commercial Bank) "STATEMENT OF SAVING ACCOUNT" PDF export."""
    account_number = None
    blocks = []

    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            words = page.extract_words()

            if account_number is None:
                account_number = next(
                    (
                        word["text"]
                        for word in words
                        if SCB_ACCOUNT_NUMBER_RE.match(word["text"])
                    ),
                    None,
                )

            rows = {}
            for word in words:
                rows.setdefault(round(word["top"]), []).append(word)
            for row in rows.values():
                row.sort(key=lambda word: word["x0"])

            current_block = None
            for top in sorted(rows):
                row = rows[top]
                if row[0]["x0"] < 60 and SCB_DATE_RE.match(row[0]["text"]):
                    current_block = [row]
                    continue
                if current_block is None:
                    continue
                current_block.append(row)
                if any(word["text"] == "NOTE" for word in row):
                    blocks.append(current_block)
                    current_block = None

    if not blocks:
        raise StatementParseError("No transaction rows found in the statement")

    entries = []
    for block in blocks:
        first_row = block[0]
        date_str = first_row[0]["text"]
        time_str = next(word["text"] for word in first_row if 60 <= word["x0"] < 85)
        channel = next(word["text"] for word in first_row if 115 <= word["x0"] < 160)
        withdrawal_word = next(
            (word for word in first_row if 195 <= word["x0"] < 235), None
        )
        deposit_word = next(
            (word for word in first_row if 255 <= word["x0"] < 315), None
        )
        balance_word = next(word for word in first_row if 355 <= word["x0"] < 420)
        balance_match = SCB_BALANCE_RE.match(balance_word["text"])
        balance_index = next(
            index for index, word in enumerate(first_row) if word is balance_word
        )

        description_parts = [
            word["text"].removeprefix(":")
            for word in first_row[balance_index + 1 :]
            if word["text"] != "DESC"
        ]
        note_parts = []

        for row in block[1:]:
            note_index = next(
                (index for index, word in enumerate(row) if word["text"] == "NOTE"),
                None,
            )
            if note_index is None:
                description_parts.extend(word["text"] for word in row)
            else:
                note_parts.extend(
                    word["text"].removeprefix(":") for word in row[note_index + 1 :]
                )

        detail = " ".join(note_parts)
        if detail == "-":
            detail = ""

        entries.append(
            dict(
                date=datetime.datetime.strptime(
                    f"{date_str} {time_str}", "%d/%m/%y %H:%M"
                ),
                description=" ".join(description_parts),
                withdrawal=_parse_amount(
                    withdrawal_word["text"] if withdrawal_word else None
                ),
                deposit=_parse_amount(deposit_word["text"] if deposit_word else None),
                balance=_parse_amount(balance_match.group(0)),
                channel=channel,
                detail=detail,
            )
        )

    return dict(
        account_number=account_number,
        started_date=min(entry["date"] for entry in entries),
        ended_date=max(entry["date"] for entry in entries),
        entries=entries,
    )


def parse_scb_credit_card_statement(file_stream):
    """Parse a CardX (formerly SCB) "CREDIT CARD STATEMENT" PDF export."""
    card_number = None
    closing_date_str = None
    raw_entries = []

    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            words = page.extract_words()

            rows = {}
            for word in words:
                rows.setdefault(round(word["top"]), []).append(word)
            for row in rows.values():
                row.sort(key=lambda word: word["x0"])

            for top in sorted(rows):
                row = rows[top]

                if closing_date_str is None:
                    full_date_words = [
                        word for word in row if SCB_CREDIT_CARD_FULL_DATE_RE.match(word["text"])
                    ]
                    if len(full_date_words) >= 2:
                        closing_date_str = min(
                            full_date_words, key=lambda word: word["x0"]
                        )["text"]

                if card_number is None:
                    for index in range(len(row) - 3):
                        candidate = row[index : index + 4]
                        if all(
                            pattern.match(word["text"])
                            for pattern, word in zip(
                                SCB_CREDIT_CARD_NUMBER_PATTERNS, candidate
                            )
                        ):
                            card_number = " ".join(
                                word["text"] for word in candidate
                            )
                            break

                if row[0]["x0"] >= 70 or not SCB_CREDIT_CARD_DATE_RE.match(row[0]["text"]):
                    continue

                transaction_date_word = next(
                    (
                        word
                        for word in row
                        if 70 <= word["x0"] < 140
                        and SCB_CREDIT_CARD_DATE_RE.match(word["text"])
                    ),
                    None,
                )
                amount_word = next(
                    (
                        word
                        for word in row
                        if word["x0"] >= 500 and SCB_CREDIT_CARD_AMOUNT_RE.match(word["text"])
                    ),
                    None,
                )
                description = " ".join(
                    word["text"] for word in row if 140 <= word["x0"] < 400
                )

                raw_entries.append(
                    dict(
                        posting_date=row[0]["text"],
                        transaction_date=(
                            transaction_date_word["text"]
                            if transaction_date_word
                            else row[0]["text"]
                        ),
                        description=description,
                        amount=_parse_amount(amount_word["text"] if amount_word else None),
                    )
                )

    if not raw_entries:
        raise StatementParseError("No transaction rows found in the statement")
    if closing_date_str is None:
        raise StatementParseError("Could not find the statement's closing date")

    closing_date = datetime.datetime.strptime(closing_date_str, "%d/%m/%y")

    entries = []
    for raw_entry in raw_entries:
        day, month = (int(part) for part in raw_entry["transaction_date"].split("/"))
        year = (
            closing_date.year - 1 if month > closing_date.month else closing_date.year
        )
        amount = raw_entry["amount"]

        entries.append(
            dict(
                date=datetime.datetime(year, month, day),
                description=raw_entry["description"],
                withdrawal=amount if amount > 0 else decimal.Decimal("0"),
                deposit=-amount if amount < 0 else decimal.Decimal("0"),
                balance=decimal.Decimal("0"),
                channel="",
                detail=f"Posting: {raw_entry['posting_date']}",
            )
        )

    return dict(
        account_number=card_number,
        started_date=min(entry["date"] for entry in entries),
        ended_date=max(entry["date"] for entry in entries),
        entries=entries,
    )


def parse_ttb_credit_card_statement(file_stream):
    """Parse a TTB (TMBThanachart Bank) "CREDIT CARD STATEMENT" PDF export."""
    card_number = None
    entries = []

    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            words = page.extract_words()

            if card_number is None:
                card_number = next(
                    (
                        word["text"]
                        for word in words
                        if TTB_CREDIT_CARD_NUMBER_RE.match(word["text"])
                    ),
                    None,
                )

            rows = {}
            for word in words:
                rows.setdefault(round(word["top"]), []).append(word)
            for row in rows.values():
                row.sort(key=lambda word: word["x0"])

            for top in sorted(rows):
                row = rows[top]
                if row[0]["x0"] >= 90 or not TTB_CREDIT_CARD_DATE_RE.match(
                    row[0]["text"]
                ):
                    continue

                posting_date_word = next(
                    (
                        word
                        for word in row
                        if 100 <= word["x0"] < 210
                        and TTB_CREDIT_CARD_DATE_RE.match(word["text"])
                    ),
                    None,
                )
                amount_word = next(
                    (
                        word
                        for word in row
                        if word["x0"] >= 490
                        and TTB_CREDIT_CARD_AMOUNT_RE.match(word["text"])
                    ),
                    None,
                )
                description = " ".join(
                    word["text"] for word in row if 210 <= word["x0"] < 490
                )
                amount = _parse_amount(amount_word["text"] if amount_word else None)

                entries.append(
                    dict(
                        date=datetime.datetime.strptime(
                            row[0]["text"], "%d/%m/%Y"
                        ),
                        description=description,
                        withdrawal=amount if amount > 0 else decimal.Decimal("0"),
                        deposit=-amount if amount < 0 else decimal.Decimal("0"),
                        balance=decimal.Decimal("0"),
                        channel="",
                        detail=(
                            f"Posting: {posting_date_word['text']}"
                            if posting_date_word
                            else ""
                        ),
                    )
                )

    if not entries:
        raise StatementParseError("No transaction rows found in the statement")

    return dict(
        account_number=card_number,
        started_date=min(entry["date"] for entry in entries),
        ended_date=max(entry["date"] for entry in entries),
        entries=entries,
    )


def _ttb_is_anchor_row(row):
    if len(row) < 3:
        return False
    day_word, month_word, year_word = row[0], row[1], row[2]
    return (
        day_word["x0"] < 50
        and TTB_DAY_RE.match(day_word["text"])
        and month_word["x0"] < 65
        and TTB_MONTH_RE.match(month_word["text"])
        and year_word["x0"] < 80
        and TTB_YEAR_RE.match(year_word["text"])
    )


def parse_ttb_statement(file_stream):
    """Parse a TTB (TMBThanachart Bank) "Savings Account Transaction (Detailed)" PDF export."""
    account_number = None
    blocks = []
    current_block = None

    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            words = page.extract_words()

            if account_number is None:
                account_number = next(
                    (
                        word["text"]
                        for word in words
                        if TTB_ACCOUNT_NUMBER_RE.match(word["text"])
                    ),
                    None,
                )

            rows = {}
            for word in words:
                rows.setdefault(round(word["top"]), []).append(word)
            for row in rows.values():
                row.sort(key=lambda word: word["x0"])

            for top in sorted(rows):
                row = rows[top]
                if _ttb_is_anchor_row(row):
                    if current_block:
                        blocks.append(current_block)
                    current_block = [row]
                elif current_block is not None:
                    current_block.append(row)

    if current_block:
        blocks.append(current_block)

    if not blocks:
        raise StatementParseError("No transaction rows found in the statement")

    entries = []
    for block in blocks:
        first_row = block[0]
        date_str = " ".join(word["text"] for word in first_row[:3])
        time_word = next(
            (
                word
                for word in first_row
                if 78 <= word["x0"] < 105 and TTB_TIME_RE.match(word["text"])
            ),
            None,
        )
        channel_word = next(
            (word for word in first_row if 210 <= word["x0"] < 250), None
        )
        amount_word = next(
            (
                word
                for word in first_row
                if 280 <= word["x0"] < 340 and TTB_AMOUNT_RE.match(word["text"])
            ),
            None,
        )
        balance_word = next(
            (
                word
                for word in first_row
                if 370 <= word["x0"] < 430 and TTB_BALANCE_RE.match(word["text"])
            ),
            None,
        )

        description_parts = []
        detail_parts = []
        for row in block:
            for word in row:
                if 108 <= word["x0"] < 210:
                    description_parts.append(word["text"])
                elif word["x0"] >= 430:
                    detail_parts.append(word["text"])

        amount = _parse_amount(amount_word["text"] if amount_word else None)

        entries.append(
            dict(
                date=datetime.datetime.strptime(
                    f"{date_str} {time_word['text']}", "%d %b %y %H:%M"
                ),
                description=" ".join(description_parts),
                withdrawal=-amount if amount < 0 else decimal.Decimal("0"),
                deposit=amount if amount > 0 else decimal.Decimal("0"),
                balance=_parse_amount(
                    balance_word["text"] if balance_word else None
                ),
                channel=channel_word["text"] if channel_word else "",
                detail=" ".join(detail_parts),
            )
        )

    return dict(
        account_number=account_number,
        started_date=min(entry["date"] for entry in entries),
        ended_date=max(entry["date"] for entry in entries),
        entries=entries,
    )


BANK_PARSERS = {
    "kasikorn": parse_kasikorn_statement,
    "scb": parse_scb_statement,
    "scb_credit_card": parse_scb_credit_card_statement,
    "ttb_credit_card": parse_ttb_credit_card_statement,
    "ttb": parse_ttb_statement,
}

BANK_CHOICES = [
    ("kasikorn", "Kasikorn Bank (K-Bank)"),
    ("scb", "Siam Commercial Bank (SCB)"),
    ("scb_credit_card", "SCB Credit Card (CardX)"),
    ("ttb_credit_card", "TTB Credit Card"),
    ("ttb", "TTB Bank (Book Bank)"),
]


def parse_statement(bank, file_stream):
    parser = BANK_PARSERS.get(bank)
    if parser is None:
        raise StatementParseError(f"Unsupported bank: {bank}")
    return parser(file_stream)


def reconcile_statement(entries, account_book_id, transactions):
    """Match statement entries against existing account book transactions.

    Matches on same datetime (to the minute) + same money amount only, since
    statement descriptions don't correspond to account book descriptions and
    the statement's time-of-day is precise enough to disambiguate same-day,
    same-amount entries without also requiring a matching direction.
    """
    book_entries = []
    for transaction in transactions:
        value = decimal.Decimal(transaction.value)
        if transaction.from_account_book.id == account_book_id:
            book_entries.append(
                dict(transaction=transaction, amount=value, direction="withdrawal")
            )
        if transaction.to_account_book.id == account_book_id:
            book_entries.append(
                dict(transaction=transaction, amount=value, direction="deposit")
            )

    unmatched_book_entries = list(book_entries)
    matched = []
    missing_in_account_book = []

    for entry in entries:
        if entry["withdrawal"] > 0:
            amount = entry["withdrawal"]
        elif entry["deposit"] > 0:
            amount = entry["deposit"]
        else:
            continue

        entry_minute = entry["date"].replace(second=0, microsecond=0)

        match = next(
            (
                candidate
                for candidate in unmatched_book_entries
                if candidate["amount"] == amount
                and candidate["transaction"].date.replace(second=0, microsecond=0)
                == entry_minute
            ),
            None,
        )

        if match:
            unmatched_book_entries.remove(match)
            matched.append(dict(statement_entry=entry, book_entry=match))
        else:
            missing_in_account_book.append(entry)

    return dict(
        matched=matched,
        missing_in_account_book=missing_in_account_book,
        extra_in_account_book=unmatched_book_entries,
    )
