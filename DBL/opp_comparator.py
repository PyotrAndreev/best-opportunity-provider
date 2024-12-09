# TODO: connect config

# Compares links by netloc+path (scheme (http/https/etc) ignored)
def compare_links(l1: str, l2: str) -> bool:
    from urllib.parse import urlparse

    url1 = urlparse(l1)
    url2 = urlparse(l2)
    return url1[1:3] == url2[1:3]


# Compare opportunity by LINK (STD v2)
def opportunity_cmp(opp1, opp2) -> bool:
    return compare_links(opp1['link'], opp2['link'])
