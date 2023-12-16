def get_display_names(account_books):
    account_book_display_names = {
        account_book.id: account_book.name for account_book in account_books
    }

    parents = dict()

    for account_book in account_books:
        if account_book.parent:
            parents[account_book.id] = account_book.parent.id

    for account_book in account_books:
        account_book_id = account_book.id
        while account_book_id in parents:
            account_book_display_names[account_book.id] = "{} > {}".format(
                account_book_display_names[parents[account_book_id]],
                account_book_display_names[account_book.id],
            )
            account_book_id = parents[account_book_id]

    return account_book_display_names
