import React from "react";
import { Toolbar, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  offset: theme.mixins.toolbar,
  root: {
    flexGrow: 1,
    fontFamily: "paybooc-Medium",
  },
  footer: {
    backgroundColor: "white",
    minHeight: 30,
    boxShadow: "None",
    alignItems: "center",
    position: "static",
  },
  footer__text: {
    marginLeft: "auto",
    marginRight: "auto",
    background: "linear-gradient(to right, #f50057, #8ca6ce)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    fontWeight: 800,
  },
}));

const Footer = () => {
  const classes = useStyles();
  return (
    <React.Fragment>
      <div className={classes.offset} />
      <div className={classes.root}>
        <Toolbar className={classes.footer}>
          <Typography className={classes.footer__text}>
            ⓒ버찌스토어. 2021.
          </Typography>
        </Toolbar>
      </div>
    </React.Fragment>
  );
};

export default Footer;
