import React from "react";
import { Grid } from "@material-ui/core";
import "./App.css";
import Header from "./Header";
import ProductCard from "./Card";
import useScrollTrigger from "@material-ui/core/useScrollTrigger";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";
import PropTypes from "prop-types";
import Fab from "@material-ui/core/Fab";
import Zoom from "@material-ui/core/Zoom";
import { makeStyles } from "@material-ui/core/styles";
import productsData from "../script/productsData.json";

const useStyles = makeStyles((theme) => ({
  root: {
    position: "fixed",
    bottom: theme.spacing(2),
    right: theme.spacing(2),
  },
}));

function ScrollTop(props) {
  const { children } = props;
  const classes = useStyles();
  // Note that you normally won't need to set the window ref as useScrollTrigger
  // will default to window.
  // This is only being set here because the demo is in an iframe.
  const trigger = useScrollTrigger({
    disableHysteresis: true,
    threshold: 100,
  });

  const handleClick = (event) => {
    const anchor = (event.target.ownerDocument || document).querySelector(
      "#back-to-top-anchor"
    );

    if (anchor) {
      anchor.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  };

  return (
    <Zoom in={trigger}>
      <div onClick={handleClick} role="presentation" className={classes.root}>
        {children}
      </div>
    </Zoom>
  );
}

ScrollTop.propTypes = {
  children: PropTypes.element.isRequired,
};

class App extends React.Component {
  state = {
    isLoading: true,
    products: [],
  };

  getProducts = () => {
    const { products } = productsData;
    this.setState({ products, isLoading: false });
  };

  async componentDidMount() {
    this.getProducts();
  }

  render() {
    const { isLoading, products } = this.state;
    return (
      <section className="container">
        {isLoading ? (
          <div className="loader">
            <span className="loader__text">Loading...</span>
          </div>
        ) : (
          <Grid container direction="column" className="app">
            <Grid item className="app__header">
              <Header />
            </Grid>
            <Grid item container className="app__cards">
              <Grid item xs={1} lg={2} />
              <Grid item xs={10} lg={8}>
                <Grid container spacing={4}>
                  {products.map((product) => (
                    <Grid item xs={12} sm={6} lg={4}>
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
                    </Grid>
                  ))}
                </Grid>
              </Grid>
              <Grid item xs={1} lg={2} />
            </Grid>
          </Grid>
        )}

        <ScrollTop>
          <Fab color="secondary" size="small" aria-label="scroll back to top">
            <KeyboardArrowUpIcon />
          </Fab>
        </ScrollTop>
      </section>
    );
  }
}

export default App;
