import React from "react";
import LazyLoad from "react-lazyload";
import PropTypes from "prop-types";

import { Grid } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import useScrollTrigger from "@material-ui/core/useScrollTrigger";
import Zoom from "@material-ui/core/Zoom";
import Fab from "@material-ui/core/Fab";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";

import Footer from "./Footer";
import ProductCard from "./Card";
import productsData from "./productsData.json";

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

const Loading = () => <div className="loading">Loading...</div>;

const Home = ({ category }) => {
  const { products } = productsData;
  return (
    <React.Fragment>
      <Grid item xs={false} sm={2} />
      <Grid item xs={12} sm={8}>
        <Grid container spacing={1}>
          {products.map((product) => {
            if (product.category === category) {
              return (
                <Grid item xs={6} md={4}>
                  <LazyLoad key={product.id} placeholder={<Loading />}>
                    <ProductCard
                      key={product.id}
                      title={product.title}
                      date={product.date}
                      hit={product.hit}
                      up={product.up}
                      price={product.price}
                      shipping={product.shipping}
                      description={product.description}
                      thumbnail={product.thumbnail}
                      link={product.link}
                      origin_url={product.origin_url}
                      origin={product.origin}
                      shop={product.shop}
                    />
                  </LazyLoad>
                </Grid>
              );
            }
            if (category === "전체보기") {
              return (
                <Grid item xs={6} md={4}>
                  <LazyLoad key={product.id} placeholder={<Loading />}>
                    <ProductCard
                      key={product.id}
                      title={product.title}
                      date={product.date}
                      hit={product.hit}
                      up={product.up}
                      price={product.price}
                      shipping={product.shipping}
                      description={product.description}
                      thumbnail={product.thumbnail}
                      link={product.link}
                      origin_url={product.origin_url}
                      origin={product.origin}
                      shop={product.shop}
                    />
                  </LazyLoad>
                </Grid>
              );
            } else {
              return null;
            }
          })}
        </Grid>
      </Grid>
      <Grid item xs={false} sm={2} />
      <Grid item className="app__footer">
        <Footer />
      </Grid>
      <ScrollTop>
        <Fab color="secondary" size="small" aria-label="scroll back to top">
          <KeyboardArrowUpIcon />
        </Fab>
      </ScrollTop>
    </React.Fragment>
  );
};

Home.propTypes = {
  category: PropTypes.string.isRequired,
};

export default Home;
