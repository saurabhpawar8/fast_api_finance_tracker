def extractTransactionData(df):
    transactions = []
    for _, row in df.iterrows():
        transaction = {
            "category": row[0],
            "date": row[1].date(),
            "transaction_type": row[2],
            "amount": row[3],
            "account_name": row[4],
            "remarks": row[5],
        }
        transactions.append(transaction)
    return transactions
