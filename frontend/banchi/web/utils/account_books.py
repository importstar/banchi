def get_display_names(account_books, excluse_none_parent=False):
    account_book_dict = {
        account_book.id: account_book for account_book in account_books
    }

    account_book_display_names = {}
    parents = dict()

    for account_book in account_books:
        if account_book.parent:
            parents[account_book.id] = account_book.parent.id

    # print(account_book_dict)
    for account_book in account_books:
        if excluse_none_parent and account_book.parent is None:
            continue

        account_book_id = account_book.id

        account_book_display_names[account_book.id] = account_book.name
        while account_book_id in parents:
            account_book_display_names[account_book.id] = "{} > {}".format(
                account_book_dict[parents[account_book_id]].name,
                account_book_display_names[account_book.id],
            )
            account_book_id = parents[account_book_id]

    return account_book_display_names
