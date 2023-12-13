def get_display_names(account_books):
    account_book_display_names = {
        account_book.id: account_book.name for account_book in account_books
    }

    for account_book in account_books:
        # account_book_display_names[account_book.id] = get_nested_name(account_book)
        if account_book.parent:
            account_book_display_names[
                account_book.id
            ] = f"{account_book_display_names[account_book.parent.id]} > {account_book_display_names[account_book.id]}"

    return account_book_display_names
