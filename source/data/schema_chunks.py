"""
GraphQL schema chunks for Kusama blockchain data
"""

SCHEMA_CHUNKS = [
    {
        'id': 'type-account',
        'content': "Account type represents a blockchain account or wallet address on Kusama. It has an 'id' field which is the account's unique address string (like 'CdwnRdmqJivB75M4advhMUdxMAaWgoRPhYQiwfSRigw18gc'). Accounts can have transfers going to them (transfersTo) and transfers coming from them (transfersFrom). Each account tracks all incoming and outgoing token movements.",
        'metadata': {
            'category': 'type',
            'graphqlType': 'Account',
            'relatedTypes': ['Transfer'],
            'examples': ['accountById(id: "CdwnRdmqJivB75M4advhMUdxMAaWgoRPhYQiwfSRigw18gc")', 'accounts { id transfersTo { amount } transfersFrom { amount } }'],
            'keywords': ['wallet', 'address', 'account', 'balance']
        }
    },
    {
        'id': 'type-transfer',
        'content': "Transfer type represents a token transfer transaction between two accounts. Fields include: 'id' (unique identifier), 'blockNumber' (which block it occurred in), 'timestamp' (when it happened), 'extrinsicHash' (transaction hash, may be null for some transfers), 'from' (sender account), 'to' (recipient account), 'amount' (tokens transferred in smallest unit), and 'fee' (transaction fee paid, may be zero for old transfers).",
        'metadata': {
            'category': 'type',
            'graphqlType': 'Transfer',
            'relatedTypes': ['Account'],
            'examples': ['transferById(id: "0x123...")', 'transfers(where: { amount_gte: 1000000000000 }) { from { id } to { id } amount timestamp }'],
            'keywords': ['transaction', 'transfer', 'payment', 'send', 'receive']
        }
    },
    {
        'id': 'query-account-by-id',
        'content': 'Query accountById(id: String!) returns a single Account by its exact address. Use this when you know the specific account address. The address must be a valid Kusama address string.',
        'metadata': {
            'category': 'query',
            'graphqlType': 'Query.accountById',
            'relatedTypes': ['Account'],
            'examples': ['accountById(id: "GcqKn3HHodwcFc3Pg3Evcbc43m7qJNMiMv744e5WMSS7TGn") { id transfersTo { amount } }'],
            'keywords': ['single account', 'specific address', 'get account']
        }
    },
    {
        'id': 'query-accounts-list',
        'content': "Query accounts returns a list of Account objects. Supports filtering with 'where' conditions, sorting with 'orderBy', pagination with 'limit' and 'offset'. Use this to search for multiple accounts or list all accounts.",
        'metadata': {
            'category': 'query',
            'graphqlType': 'Query.accounts',
            'relatedTypes': ['Account', 'AccountWhereInput', 'AccountOrderByInput'],
            'examples': ['accounts(limit: 10) { id }', 'accounts(where: { transfersFrom_some: { amount_gte: 1000000000000 } }) { id }'],
            'keywords': ['list accounts', 'multiple accounts', 'all accounts']
        }
    },
    {
        'id': 'query-transfer-by-id',
        'content': 'Query transferById(id: String!) returns a single Transfer by its unique identifier. Use this when you have a specific transfer ID.',
        'metadata': {
            'category': 'query',
            'graphqlType': 'Query.transferById',
            'relatedTypes': ['Transfer'],
            'examples': ['transferById(id: "0000000001-000001-c86bf") { amount from { id } to { id } timestamp }'],
            'keywords': ['single transfer', 'specific transaction']
        }
    },
    {
        'id': 'query-transfers-list',
        'content': "Query transfers returns a list of Transfer objects. Supports filtering with 'where' for complex conditions, 'orderBy' for sorting (e.g., by timestamp or amount), 'limit' for pagination, and 'offset' for skipping results. This is the main query for finding transactions.",
        'metadata': {
            'category': 'query',
            'graphqlType': 'Query.transfers',
            'relatedTypes': ['Transfer', 'TransferWhereInput', 'TransferOrderByInput'],
            'examples': [
                'transfers(orderBy: timestamp_DESC, limit: 10) { amount from { id } to { id } timestamp }',
                'transfers(where: { blockNumber: 17581509 }) { id amount }',
                'transfers(where: { timestamp_gte: "2024-01-01T00:00:00Z" }) { amount }'
            ],
            'keywords': ['list transfers', 'transactions', 'recent transfers', 'transaction history']
        }
    },
    {
        'id': 'filter-transfer-where',
        'content': "TransferWhereInput allows filtering transfers by: amount (amount_eq, amount_gte, amount_lte), blockNumber, timestamp (supports date comparisons), from/to accounts (can filter by nested Account properties), extrinsicHash. Use _gte for 'greater than or equal', _lte for 'less than or equal', _eq for exact match.",
        'metadata': {
            'category': 'filter',
            'graphqlType': 'TransferWhereInput',
            'relatedTypes': ['Transfer'],
            'examples': [
                'where: { amount_gte: 1000000000000 } // transfers >= 1 KSM',
                'where: { from: { id_eq: "address" } } // transfers from specific account',
                'where: { timestamp_gte: "2024-01-01T00:00:00Z", timestamp_lte: "2024-01-31T23:59:59Z" } // transfers in January 2024',
                'where: { blockNumber_eq: 17581509 } // transfers in specific block'
            ],
            'keywords': ['filter', 'where', 'conditions', 'search criteria']
        }
    },
    {
        'id': 'filter-ordering',
        'content': 'Ordering results: Use orderBy parameter with fields like timestamp_DESC (newest first), timestamp_ASC (oldest first), amount_DESC (largest first), amount_ASC (smallest first), blockNumber_DESC (recent blocks first). DESC means descending order, ASC means ascending order.',
        'metadata': {
            'category': 'filter',
            'graphqlType': 'OrderByInput',
            'relatedTypes': ['TransferOrderByInput', 'AccountOrderByInput'],
            'examples': ['orderBy: timestamp_DESC // newest transfers first', 'orderBy: amount_DESC // largest transfers first', 'orderBy: blockNumber_ASC // oldest blocks first'],
            'keywords': ['sort', 'order', 'orderBy', 'latest', 'recent', 'biggest', 'smallest']
        }
    },
    {
        'id': 'relationship-account-transfers',
        'content': "Account to Transfer relationships: Each Account has 'transfersTo' (incoming transfers where this account is the recipient) and 'transfersFrom' (outgoing transfers where this account is the sender). These fields return arrays of Transfer objects and support the same filtering and ordering as the main transfers query.",
        'metadata': {
            'category': 'relationship',
            'graphqlType': 'Account.transfersTo, Account.transfersFrom',
            'relatedTypes': ['Account', 'Transfer'],
            'examples': [
                'account { transfersTo(orderBy: timestamp_DESC, limit: 5) { amount timestamp } }',
                'account { transfersFrom(where: { amount_gte: 1000000000000 }) { to { id } amount } }'
            ],
            'keywords': ['incoming', 'outgoing', 'sent', 'received', 'account transfers']
        }
    },
    {
        'id': 'relationship-transfer-accounts',
        'content': "Transfer to Account relationships: Each Transfer has 'from' (sender Account) and 'to' (recipient Account) fields. These return the complete Account object, allowing you to access the account's ID and navigate to their other transfers.",
        'metadata': {
            'category': 'relationship',
            'graphqlType': 'Transfer.from, Transfer.to',
            'relatedTypes': ['Transfer', 'Account'],
            'examples': ['transfer { from { id } to { id } }', "transfer { from { transfersFrom(limit: 5) { amount } } } // sender's recent sends"],
            'keywords': ['sender', 'recipient', 'from account', 'to account']
        }
    },
    {
        'id': 'concept-kusama-basics',
        'content': "Kusama is Polkadot's canary network. KSM is the native token. Amounts are stored in the smallest unit (1 KSM = 1,000,000,000,000 units). Common addresses include validators like 'GcqKn3HHodwcFc3Pg3Evcbc43m7qJNMiMv744e5WMSS7TGn'. Block numbers increase over time. Timestamps are in ISO format (e.g., '2024-01-15T10:30:00Z').",
        'metadata': {
            'category': 'concept',
            'examples': ['1000000000000 units = 1 KSM', 'Block 17581509 is a specific block height', "Timestamps like '2024-01-15T10:30:00Z' for January 15, 2024"],
            'keywords': ['KSM', 'kusama', 'units', 'denomination', 'planck']
        }
    },
    {
        'id': 'concept-pagination',
        'content': "Pagination: Use 'limit' to restrict number of results (e.g., limit: 10 for top 10), 'offset' to skip results (e.g., offset: 20 to skip first 20). Combine with orderBy for consistent pagination. Maximum limit depends on query complexity.",
        'metadata': {
            'category': 'concept',
            'examples': [
                'transfers(limit: 10, offset: 0) // first page',
                'transfers(limit: 10, offset: 10) // second page',
                'transfers(orderBy: timestamp_DESC, limit: 5) // latest 5 transfers'
            ],
            'keywords': ['pagination', 'limit', 'offset', 'page', 'results per page']
        }
    },
    {
        'id': 'example-last-transaction',
        'content': 'To find the last/latest transaction for an address: Query the account by ID, then get transfersFrom or transfersTo ordered by timestamp_DESC with limit 1. This pattern works for finding the most recent activity.',
        'metadata': {
            'category': 'example',
            'examples': [
                'accountById(id: "CdwnRdmqJivB75M4advhMUdxMAaWgoRPhYQiwfSRigw18gc") { transfersFrom(orderBy: timestamp_DESC, limit: 1) { id amount to { id } timestamp blockNumber } }'
            ],
            'keywords': ['last transaction', 'latest transaction', 'most recent']
        }
    },
    {
        'id': 'example-recent-transfers',
        'content': "To find transfers in the last hour or specific time period: Use timestamp filtering with _gte (greater than or equal) for start time and _lte (less than or equal) for end time. Calculate the timestamp for 'one hour ago' from current time.",
        'metadata': {
            'category': 'example',
            'examples': [
                'transfers(where: { timestamp_gte: "2024-01-15T09:00:00Z", timestamp_lte: "2024-01-15T10:00:00Z" }, orderBy: timestamp_DESC) { id amount from { id } to { id } timestamp }'
            ],
            'keywords': ['last hour', 'recent', 'time period', 'today', 'this week']
        }
    },
    {
        'id': 'example-block-transfers',
        'content': 'To find what happened in a specific block: Query transfers with blockNumber_eq filter. Each block can contain multiple transfers. Block numbers are integers that increase with each new block.',
        'metadata': {
            'category': 'example',
            'examples': [
                'transfers(where: { blockNumber_eq: 17581509 }) { id amount from { id } to { id } extrinsicHash timestamp }'
            ],
            'keywords': ['specific block', 'block number', 'block transfers', 'block transactions']
        }
    },
    {
        'id': 'example-large-transfers',
        'content': 'To find large transfers or whale movements: Use amount_gte filter with large values. Remember amounts are in smallest units (1 KSM = 1e12 units). Combine with orderBy: amount_DESC to see biggest first.',
        'metadata': {
            'category': 'example',
            'examples': [
                'transfers(where: { amount_gte: "1000000000000000" }, orderBy: amount_DESC, limit: 10) { amount from { id } to { id } timestamp } // >= 1000 KSM'
            ],
            'keywords': ['large transfers', 'whale', 'big transactions', 'high value']
        }
    },
    {
        'id': 'example-account-activity',
        'content': 'To get all activity for an account: Query account by ID and fetch both transfersTo (received) and transfersFrom (sent). You can filter and order these separately to analyze account behavior.',
        'metadata': {
            'category': 'example',
            'examples': [
                'accountById(id: "address") { transfersTo(orderBy: timestamp_DESC, limit: 10) { amount from { id } timestamp } transfersFrom(orderBy: timestamp_DESC, limit: 10) { amount to { id } timestamp } }'
            ],
            'keywords': ['account activity', 'account history', 'all transfers', 'account analysis']
        }
    },
    {
        'id': 'example-transfer-between-accounts',
        'content': 'To find transfers between two specific accounts: Use compound where conditions with both from and to account filters. This helps track payments or interactions between specific addresses.',
        'metadata': {
            'category': 'example',
            'examples': [
                'transfers(where: { from: { id_eq: "sender_address" }, to: { id_eq: "recipient_address" } }) { amount timestamp blockNumber }'
            ],
            'keywords': ['between accounts', 'from to', 'specific sender receiver', 'payment tracking']
        }
    }
] 