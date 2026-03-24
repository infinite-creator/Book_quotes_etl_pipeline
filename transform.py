def transform_quotes(quotes: list[dict]) -> list[dict]:
    transformed_quotes = []
    seen = set()
    
    for quote in quotes:
        text = quote["quote"].strip()
        author = quote["author"].strip()
        tags = ", ".join(tag.strip() for tag in quote["tags"])
        
        unique_key = (text, author)
        
        if unique_key in seen:
            continue
        
        seen.add(unique_key)
        
        transformed_quote = {
            "quote": text,
            "author": author,
            "tags": tags
        }
        transformed_quotes.append(transformed_quote)
        
    return transformed_quotes
