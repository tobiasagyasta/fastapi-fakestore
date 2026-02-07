from app.domain.products.entity import Product


def product_to_response(product: Product) -> dict[str, object]:
    return {
        "id": product.id,
        "title": product.title,
        "price": product.price,
        "description": product.description,
        "category": product.category,
        "image": product.image,
    }
