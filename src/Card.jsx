import React from "react";
import Box from "@material-ui/core/Box";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import CardActions from "@material-ui/core/CardActions";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import { Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import ShareIcon from "@material-ui/icons/Share";
import PropTypes from "prop-types";
import { MuiThemeProvider, createMuiTheme } from "@material-ui/core/styles";

const theme = createMuiTheme({
  typography: {
    fontFamily: "paybooc-Medium",
  },
});

const useStyles = makeStyles({
  card: {
    minWidth: 300,
    heigth: 550,
    backgroundColor: "#050505",
  },
  media: {
    height: 0,
    paddingTop: "56.25%", // 16:9
  },
  title: {
    height: 28,
  },
  title__text: {
    fontSize: 20,
    fontFamily: "paybooc-Bold",
    fontWeight: 800,
    textOverflow: "ellipsis",
    margin: 0,
  },
  date:{

  },
  date__text:{
    fontSize: 14,
    fontFamily: "paybooc-Medium",
    color: "gray",
  },
  description: {},
  description__text: {
    fontSize: 16,
    color: "gray",
    textOverflow: "ellipsis",
  },
  shopInfo: {
    fontSize: 14,
    fontFamily: "paybooc-Medium",
  },
  shopInfo__hit: {
    color: "gray",
    marginRight: 5,
  },
  shopInfo__up: {
    color: "gray",
    marginRight: 5,
    borderRadius: 3,
  },
  shopInfo__origin: {
    backgroundColor: "#FE6B8B",
    marginRight: 5,
    padding: 5,
    borderRadius: 3,
  },
  shopInfo__shop: {
    backgroundColor: "#FF8E53",
    marginRight: 5,
    padding: 5,
    borderRadius: 3,
  },
  buyButton: {
    background: "linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)",
    border: 0,
    borderRadius: 3,
    boxShadow: "0 3px 5px 2px rgba(255, 105, 135, .3)",
    color: "white",
    height: 48,
    padding: "0 30px",
    marginLeft: 8,
    marginBottom: 8,
  },
  shareButton: {
    marginLeft: "auto",
    marginRight: 8,
    marginBottom: 8,
  },
});

function ProductCard({
  title,
  date,
  hit,
  up,
  price,
  shipping,
  description,
  thumbnail,
  link,
  origin,
  shop,
}) {
  const classes = useStyles();

  return (
    <MuiThemeProvider theme={theme}>
      <Card className={{ root: classes.card }} elevation="10">
        <CardMedia className={classes.media} image={thumbnail} title={title} />
        <CardContent>
          <div className={classes.title} href={link}>
            <Box component="div">
              <Typography noWrap className={classes.title__text}>
                {title}
              </Typography>
            </Box>
          </div>
          <p className={classes.date}>
            <Box component="div" className={classes.date__text}>
              <Typography>{date}</Typography>
            </Box>
          </p>
          <p className={classes.shopInfo}>
            <Box component="span" className={classes.shopInfo__hit}>
              조회수: {hit}
            </Box>
            <Box component="span" className={classes.shopInfo__up}>
              추천: {up}
            </Box>
            <Box component="span" className={classes.shopInfo__origin}>
              {origin}
            </Box>
            <Box component="span" className={classes.shopInfo__shop}>
              {shop}
            </Box>
          </p>
          <div className={classes.description}>
            <Box component="div" className={classes.description__text}>
              <Typography noWrap>{description}</Typography>
            </Box>
          </div>
          <p className={classes.prodDetail}>
            <Typography>
              {price} / {shipping}
            </Typography>
          </p>
        </CardContent>
        <CardActions disableSpacing>
          <Button
            className={classes.buyButton}
            target="_blank"
            href={link}
            variant="contained"
            color="primary"
            size="large"
          >
            🎁 구경하기
          </Button>
          <IconButton className={classes.shareButton} aria-label="share">
            <ShareIcon />
          </IconButton>
        </CardActions>
      </Card>
    </MuiThemeProvider>
  );
}

ProductCard.propTypes = {
  title: PropTypes.string.isRequired,
  date: PropTypes.string.isRequired,
  hit: PropTypes.number.isRequired,
  up: PropTypes.number.isRequired,
  price: PropTypes.string.isRequired,
  shipping: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  thumbnail: PropTypes.string.isRequired,
  link: PropTypes.string.isRequired,
  origin: PropTypes.string.isRequired,
  shop: PropTypes.string.isRequired,
};

export default ProductCard;
