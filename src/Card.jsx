import React from "react";
import PropTypes from "prop-types";
import Box from "@material-ui/core/Box";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import CardActions from "@material-ui/core/CardActions";
import Snackbar from "@material-ui/core/Snackbar";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import { Typography, Link } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import ShareIcon from "@material-ui/icons/Share";
import MuiAlert from "@material-ui/lab/Alert";
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
    paddingTop: "100%", // 16:9
  },
  title: {
    height: 62,
  },
  title__text: {
    height: 62,
    fontSize: 14,
    color: "black",
    fontFamily: "paybooc-Bold",
    fontWeight: 800,
    overflow: "hidden",
    margin: 0,
  },
  date: {},
  date__text: {
    fontSize: 11,
    fontFamily: "paybooc-Medium",
    color: "gray",
  },
  description: {},
  description__text: {
    fontSize: 12,
    color: "gray",
    textOverflow: "ellipsis",
    fontFamily: "paybooc-Medium",
  },
  hitsAndUps: {
    fontSize: 12,
    fontWeight: 600,
    fontFamily: "paybooc-Medium",
  },
  hitsAndUps__hit: {
    color: "gray",
    marginRight: 5,
  },
  hitsAndUps__up: {
    color: "gray",
    marginRight: 5,
    borderRadius: 3,
  },
  shopInfo: {
    fontSize: 12,
    fontFamily: "paybooc-Medium",
    margin: "10px auto",
    height: 15,
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
    fontSize: 11,
  },
  shareButton: {
    marginLeft: "auto",
    marginRight: 8,
    marginBottom: 8,
  },
  prodDetail: {},
  prodDetail__text: {
    fontSize: 12,
    fontFamily: "paybooc-Medium",
  },
});

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

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
  origin_url,
  origin,
  shop,
}) {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);

  const handleClick = () => {
    navigator.clipboard.writeText(link);
    setOpen(true);
  };

  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }

    setOpen(false);
  };

  return (
    <MuiThemeProvider theme={theme}>
      <Card className={{ root: classes.card }} elevation="10">
        <CardMedia className={classes.media} image={thumbnail} title={title} />
        <CardContent>
          <div className={classes.title} href={link}>
            <Box component="div">
              <Typography className={classes.title__text}>
                <Link target="_blank" href={origin_url}>
                  {title}
                </Link>
              </Typography>
            </Box>
          </div>
          <div className={classes.date}>
            <Box component="div">
              <Typography className={classes.date__text}>{date}</Typography>
            </Box>
          </div>
          <div className={classes.hitsAndUps}>
            <Box component="span" className={classes.hitsAndUps__hit}>
              조회수: {hit}
            </Box>
          </div>
          <div className={classes.hitsAndUps}>
            <Box component="span" className={classes.hitsAndUps__up}>
              추천: {up}
            </Box>
          </div>
          <div className={classes.shopInfo}>
            <Box component="span" className={classes.shopInfo__origin}>
              {origin}
            </Box>
            <Box component="span" className={classes.shopInfo__shop}>
              {shop}
            </Box>
          </div>
          <div className={classes.description}>
            <Box component="div">
              <Typography noWrap className={classes.description__text}>
                {description}
              </Typography>
            </Box>
          </div>
          <div className={classes.prodDetail}>
            <Typography className={classes.prodDetail__text}>
              {price} / {shipping}
            </Typography>
          </div>
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
            🎁 Go!
          </Button>
          <IconButton
            className={classes.shareButton}
            aria-label="share"
            onClick={handleClick}
          >
            <ShareIcon />
          </IconButton>
          <Snackbar open={open} autoHideDuration={3000} onClose={handleClose}>
            <Alert onClose={handleClose} severity="success">
              주소가 복사됐어요!
            </Alert>
          </Snackbar>
        </CardActions>
      </Card>
    </MuiThemeProvider>
  );
}

ProductCard.propTypes = {
  title: PropTypes.string.isRequired,
  date: PropTypes.string.isRequired,
  hit: PropTypes.string.isRequired,
  up: PropTypes.string.isRequired,
  price: PropTypes.string.isRequired,
  shipping: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  thumbnail: PropTypes.string.isRequired,
  link: PropTypes.string.isRequired,
  origin_url: PropTypes.string.isRequired,
  origin: PropTypes.string.isRequired,
  shop: PropTypes.string.isRequired,
};

export default ProductCard;
