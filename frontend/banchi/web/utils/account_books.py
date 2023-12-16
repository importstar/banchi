def get_display_names(account_books):
    account_book_display_names = {
        account_book.id: account_book.name for account_book in account_books
    }

    for account_book in account_books:
        account_book_display_names[account_book.id] = get_nested_display_names(
            account_book, account_book_display_names
        )

    return account_book_display_names


def get_nested_display_names(account_book, account_book_display_names):
    if account_book.parent:
        return f"{get_nested_display_names(account_book.parent, account_book_display_names)} > {account_book.name}"

    return account_book.name
