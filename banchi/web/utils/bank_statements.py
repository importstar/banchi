import csv
import datetime
import decimal
import io

BROUGHT_FORWARD_LABEL = "ยอดยกมา"
DATE_HEADER_LABEL = "วันที่"
ACCOUNT_NUMBER_LABEL = "เลขที่บัญชีเงินฝาก"


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
