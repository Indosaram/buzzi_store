import React from "react";
import ProductCard from "./Card";
import productsData from "./productsData.json";

class Content extends React.Component {
  state = {
    isLoading: true,
    products: [],
  };

  getProducts = async () => {
    const {
      data: { products },
    } = productsData;

    this.setState({ products: products, isLoading: false });
  };

  async componentDidMount() {
    this.getProducts();

    return (
      <section className="container">
        {this.isLoading ? (
          <div className="loader">
            <span className="loader__text">Loading...</span>
          </div>
        ) : (
          <div className="products">
            {this.products.map((product) => (
              <ProductCard
                key={product.id}
                title={product.title}
                hit={product.hit}
                price={product.price}
                shipping={product.shipping}
                description={product.description}
                thumbnail={product.thumbnail}
                link={product.link}
                origin={product.origin}
                shop={product.shop}
              />
            ))}
          </div>
        )}
      </section>
    );
  }
}

export default Content;
