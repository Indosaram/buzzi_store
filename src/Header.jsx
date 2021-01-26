import React from "react";
import { AppBar, Toolbar } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import buzziLogo from "./buzzi-store-logo.png";

const useStyles = makeStyles((theme) => ({
  offset: theme.mixins.toolbar/2,
  logoContainer: {
    backgroundColor: 'white',
    height: 50,
    boxShadow: "None",
  },
  logo: {
    maxWidth: 120,
  },
}));

const Header = () => {
  const classes = useStyles();
  return (
    <React.Fragment>
      <AppBar className={classes.logoContainer} position="fixed">
        <Toolbar>
          {/* <img src="buzzi-store-logo.png" alt="Buzzi store logo" /> */}
          <a href="/">
            <img
              className={classes.logo}
              src={buzziLogo}
              alt="Buzzi store logo"
            />
          </a>
        </Toolbar>
      </AppBar>
      <Toolbar id="back-to-top-anchor" />
      <div className={classes.offset} />
    </React.Fragment>
  );
};

export default Header;
