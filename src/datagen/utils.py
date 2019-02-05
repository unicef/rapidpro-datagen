def permute_email(*emails):
    for base in emails:
        address, domain = base.split('@')
        for i in range(1, len(address)):
            a = list(address)
            a.insert(i, '.')
            yield f'{"".join(a)}@{domain}'

